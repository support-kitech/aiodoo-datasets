"""CLI command implementations for the Validation Framework."""

import json
import sys
import logging

from validation.cli.configuration import parse_args, build_options
from validation.core.manager import ValidationManager
from validation.reports.console_reporter import ConsoleReporter
from validation.reports.json_reporter import JsonReporter
from validation.reports.markdown_reporter import MarkdownReporter
from validation.reports.ci_reporter import CIReporter

logger = logging.getLogger(__name__)


class Commands:
    """Validation CLI command handlers."""

    @staticmethod
    def run(argv: list[str] | None = None) -> int:
        """Main CLI entrypoint. Returns exit code."""
        args = parse_args(argv)

        if args.command == "validate-all":
            return Commands.validate_all(args)
        elif args.command == "validate-dataset":
            return Commands.validate_dataset(args)
        elif args.command == "validate-record":
            return Commands.validate_record(args)
        else:
            logger.error("Unknown command. Use --help for usage.")
            return 1

    @staticmethod
    def validate_all(args) -> int:
        """Validate all datasets in the directory."""
        options = build_options(args)
        manager = ValidationManager()
        result = manager.validate(args.dir, options)

        reporter = Commands._get_reporter(options.report_format.value)
        reporter.report(result.report, args.dir)

        return 0 if result.success else 1

    @staticmethod
    def validate_dataset(args) -> int:
        """Validate a single JSONL file."""
        options = build_options(args)
        manager = ValidationManager()
        result = manager.validate_file(args.file, options)

        from validation.builders.report_builder import ReportBuilder

        report = ReportBuilder.build((result,), options)
        reporter = Commands._get_reporter(getattr(args, "format", "console"))
        reporter.report(report, args.file.parent)

        return 0 if result.status.value == "passed" else 1

    @staticmethod
    def validate_record(args) -> int:
        """Validate a single record from a JSONL file."""
        jsonl_path = args.file
        line_num = args.line

        try:
            with open(jsonl_path, encoding="utf-8") as f:
                for i, line in enumerate(f):
                    if i == line_num:
                        record = json.loads(line.strip())
                        manager = ValidationManager()
                        result = manager.validate_record(record, jsonl_path.name)
                        logger.info("Record %d: %s (%d issues)", line_num, result.status.value, len(result.issues))
                        for issue in result.issues:
                            logger.info("  [%s] %s: %s", issue.severity.value, issue.rule_id, issue.message)
                        return 0 if result.status.value == "passed" else 1

            logger.error("Line %d not found in %s", line_num, jsonl_path)
            return 1
        except Exception as e:
            logger.error("Error: %s", e)
            return 1

    @staticmethod
    def _get_reporter(fmt: str):
        reporters = {
            "console": ConsoleReporter,
            "json": JsonReporter,
            "markdown": MarkdownReporter,
            "ci": CIReporter,
        }
        return reporters.get(fmt, ConsoleReporter)()


def main() -> None:
    """CLI entrypoint."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )
    sys.exit(Commands.run())


if __name__ == "__main__":
    main()

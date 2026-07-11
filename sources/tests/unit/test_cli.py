"""Unit tests for the Sources CLI."""

import json
from pathlib import Path
from unittest.mock import Mock, patch


from sources.cli.arguments import build_parser
from sources.cli.commands import CliCommands
from sources.pipeline.pipeline_options import PipelineOptions
from sources.pipeline.pipeline_result import PipelineResult
from sources.pipeline.pipeline_statistics import PipelineStatistics
from sources.exceptions import SourcesError


def test_parser_default_args():
    """Test standard parser defaults."""
    parser = build_parser()
    args = parser.parse_args(["summary"])
    assert args.command == "summary"
    assert args.config == Path("config/sources.yaml")
    assert not args.json


@patch("sources.cli.commands.sys.exit")
@patch("builtins.print")
def test_cli_summary_success(mock_print, mock_exit):
    """Test human readable summary command."""
    mock_manager = Mock()
    mock_stats = PipelineStatistics()
    mock_result = PipelineResult(
        success=True,
        context=Mock(repositories=[]),
        cache_validation=None,
        statistics=mock_stats,
        warnings=(),
        errors=()
    )
    mock_manager.load.return_value = mock_result
    
    cli = CliCommands(mock_manager, Path("config.yaml"), as_json=False)
    cli.summary(PipelineOptions())
    
    mock_manager.load.assert_called_once()
    mock_print.assert_any_call("=== Sources Framework Summary ===")
    mock_exit.assert_called_with(0)


@patch("sources.cli.commands.sys.exit")
@patch("builtins.print")
def test_cli_scan_json_error(mock_print, mock_exit):
    """Test JSON output format for errors."""
    mock_manager = Mock()
    mock_result = PipelineResult(
        success=False,
        context=None,
        cache_validation=None,
        statistics=PipelineStatistics(),
        warnings=(),
        errors=("Configuration missing",)
    )
    mock_manager.load.return_value = mock_result
    
    cli = CliCommands(mock_manager, Path("config.yaml"), as_json=True)
    cli.scan(PipelineOptions())
    
    mock_manager.load.assert_called_once()
    output = mock_print.call_args[0][0]
    data = json.loads(output)
    assert data["success"] is False
    assert "Configuration missing" in data["errors"]
    mock_exit.assert_called_with(1)


@patch("sources.cli.main.sys.exit")
@patch("builtins.print")
def test_main_catch_sources_error(mock_print, mock_exit):
    """Test main block catches SourcesError."""
    from sources.cli.main import main
    
    with patch("sys.argv", ["aiodoo-sources", "scan"]), \
         patch("sources.cli.main.RepositoryManager") as mock_mgr_cls:
             
        mock_mgr = Mock()
        mock_mgr.load.side_effect = SourcesError("Fatal crash")
        mock_mgr_cls.return_value = mock_mgr
        
        main()
        
        mock_print.assert_called_with("✗ Fatal Sources Framework Error: Fatal crash")
        mock_exit.assert_called_with(4)

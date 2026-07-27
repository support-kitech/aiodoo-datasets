#!/usr/bin/env python3
"""
Print JSONL structure like Linux tree.

Examples:
    python jsonl_tree.py approval_dataset.jsonl
    python jsonl_tree.py approval_dataset.jsonl -L 3
    python jsonl_tree.py approval_dataset.jsonl -L 5
    python jsonl_tree.py coding_v1_0.jsonl -L 4
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def print_tree(obj, prefix="", depth=0, max_depth=3):
    if depth >= max_depth:
        return

    if isinstance(obj, dict):
        items = list(obj.items())

        for i, (key, value) in enumerate(items):
            last = i == len(items) - 1
            branch = "└── " if last else "├── "

            if isinstance(value, dict):
                print(f"{prefix}{branch}{key}/ ({len(value)} keys)")
                print_tree(
                    value,
                    prefix + ("    " if last else "│   "),
                    depth + 1,
                    max_depth,
                )

            elif isinstance(value, list):
                print(f"{prefix}{branch}{key}[] ({len(value)} items)")
                if value:
                    print_tree(
                        value[0],
                        prefix + ("    " if last else "│   "),
                        depth + 1,
                        max_depth,
                    )

            else:
                print(
                    f"{prefix}{branch}{key}: {type(value).__name__}"
                )

    elif isinstance(obj, list):
        if obj:
            print(f"{prefix}[] ({len(obj)} items)")
            print_tree(obj[0], prefix + "    ", depth + 1, max_depth)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("jsonl")
    parser.add_argument(
        "-L",
        "--level",
        type=int,
        default=3,
        help="Maximum tree depth",
    )
    parser.add_argument(
        "-n",
        "--records",
        type=int,
        default=1,
        help="Number of records to inspect",
    )

    args = parser.parse_args()

    path = Path(args.jsonl)

    with path.open("r", encoding="utf-8") as f:
        for idx, line in enumerate(f):
            if idx >= args.records:
                break

            print("=" * 80)
            print(f"Record {idx + 1}")
            print("=" * 80)

            obj = json.loads(line)

            print_tree(obj, max_depth=args.level)
            print()


if __name__ == "__main__":
    main()

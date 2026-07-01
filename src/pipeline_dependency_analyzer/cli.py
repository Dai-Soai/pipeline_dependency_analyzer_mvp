from __future__ import annotations

import argparse
import sys

from pipeline_dependency_analyzer.analyzer import analyze_dependencies
from pipeline_dependency_analyzer.loader import PipelineLoadError, load_pipeline_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pipeline-dependency",
        description="Analyze RADAR Services pipeline dependencies.",
    )

    subparsers = parser.add_subparsers(dest="command")

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze pipeline dependency relationships.",
    )
    analyze_parser.add_argument(
        "pipeline_dir",
        help="Directory containing *.pipeline.yaml files.",
    )

    return parser


def print_dependency_result(result) -> None:
    print(f"Dependency analysis: {'passed' if result.ok else 'failed'}")
    print(f"Pipelines: {len(result.nodes)}")
    print(f"Issues: {len(result.issues)}")

    if result.ok:
        print("Execution order:")
        for index, node in enumerate(result.nodes, start=1):
            print(f"{index}. {node.pipeline_id}")
    else:
        print("Issues:")
        for issue in result.issues:
            print(f"- {issue.code}: {issue.message}")


def run_analyze_command(args: argparse.Namespace) -> int:
    try:
        nodes = load_pipeline_dir(args.pipeline_dir)
    except PipelineLoadError as exc:
        print(f"Dependency analysis failed to start: {exc}", file=sys.stderr)
        return 1

    result = analyze_dependencies(nodes)
    print_dependency_result(result)

    return 0 if result.ok else 1


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "analyze":
        return run_analyze_command(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

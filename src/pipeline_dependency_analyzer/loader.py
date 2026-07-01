from pathlib import Path
from typing import Any

import yaml

from pipeline_dependency_analyzer.contract import DependencyNode


class PipelineLoadError(Exception):
    pass


def load_yaml_file(path: str | Path) -> dict[str, Any]:
    pipeline_path = Path(path)

    if not pipeline_path.exists():
        raise PipelineLoadError(f"Pipeline file not found: {pipeline_path}")

    if not pipeline_path.is_file():
        raise PipelineLoadError(f"Pipeline path is not a file: {pipeline_path}")

    payload = yaml.safe_load(pipeline_path.read_text(encoding="utf-8"))

    if payload is None:
        raise PipelineLoadError(f"Pipeline file is empty: {pipeline_path}")

    if not isinstance(payload, dict):
        raise PipelineLoadError(
            f"Pipeline YAML root must be a dictionary: {pipeline_path}"
        )

    return payload


def node_from_payload(payload: dict[str, Any]) -> DependencyNode:
    pipeline_id = payload.get("pipeline_id")

    if not isinstance(pipeline_id, str) or not pipeline_id.strip():
        raise PipelineLoadError("Missing or invalid pipeline_id")

    depends_on = payload.get("depends_on", [])

    if depends_on is None:
        depends_on = []

    if not isinstance(depends_on, list):
        raise PipelineLoadError("depends_on must be a list")

    dependencies = []

    for item in depends_on:
        if not isinstance(item, str) or not item.strip():
            raise PipelineLoadError("depends_on items must be non-empty strings")
        dependencies.append(item)

    return DependencyNode(
        pipeline_id=pipeline_id,
        dependencies=dependencies,
    )


def load_pipeline_file(path: str | Path) -> DependencyNode:
    payload = load_yaml_file(path)
    return node_from_payload(payload)


def load_pipeline_dir(directory: str | Path) -> list[DependencyNode]:
    pipeline_dir = Path(directory)

    if not pipeline_dir.exists():
        raise PipelineLoadError(f"Pipeline directory not found: {pipeline_dir}")

    if not pipeline_dir.is_dir():
        raise PipelineLoadError(f"Pipeline path is not a directory: {pipeline_dir}")

    return [
        load_pipeline_file(path)
        for path in sorted(pipeline_dir.glob("*.pipeline.yaml"))
    ]

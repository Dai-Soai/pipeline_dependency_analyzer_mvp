from pathlib import Path

import pytest

from pipeline_dependency_analyzer.loader import (
    PipelineLoadError,
    load_pipeline_dir,
    load_pipeline_file,
    load_yaml_file,
    node_from_payload,
)


def test_load_yaml_file(tmp_path: Path):
    file = tmp_path / "sample.pipeline.yaml"
    file.write_text(
        """
pipeline_id: workflow
depends_on:
  - prepare
""",
        encoding="utf-8",
    )

    payload = load_yaml_file(file)

    assert payload["pipeline_id"] == "workflow"
    assert payload["depends_on"] == ["prepare"]


def test_node_from_payload():
    node = node_from_payload(
        {
            "pipeline_id": "workflow",
            "depends_on": ["prepare", "database"],
        }
    )

    assert node.pipeline_id == "workflow"
    assert node.dependencies == ["prepare", "database"]


def test_node_from_payload_defaults_dependencies():
    node = node_from_payload({"pipeline_id": "database"})

    assert node.pipeline_id == "database"
    assert node.dependencies == []


def test_load_pipeline_file(tmp_path: Path):
    file = tmp_path / "workflow.pipeline.yaml"
    file.write_text(
        """
pipeline_id: workflow
depends_on:
  - prepare
""",
        encoding="utf-8",
    )

    node = load_pipeline_file(file)

    assert node.pipeline_id == "workflow"
    assert node.dependencies == ["prepare"]


def test_load_pipeline_dir(tmp_path: Path):
    (tmp_path / "a.pipeline.yaml").write_text(
        "pipeline_id: a\ndepends_on: []\n",
        encoding="utf-8",
    )
    (tmp_path / "b.pipeline.yaml").write_text(
        "pipeline_id: b\ndepends_on:\n  - a\n",
        encoding="utf-8",
    )

    nodes = load_pipeline_dir(tmp_path)

    assert len(nodes) == 2
    assert nodes[0].pipeline_id == "a"
    assert nodes[1].pipeline_id == "b"


def test_load_missing_file():
    with pytest.raises(PipelineLoadError, match="Pipeline file not found"):
        load_pipeline_file("missing.pipeline.yaml")


def test_node_from_payload_rejects_missing_pipeline_id():
    with pytest.raises(PipelineLoadError, match="Missing or invalid pipeline_id"):
        node_from_payload({})


def test_node_from_payload_rejects_invalid_depends_on():
    with pytest.raises(PipelineLoadError, match="depends_on must be a list"):
        node_from_payload(
            {
                "pipeline_id": "workflow",
                "depends_on": "prepare",
            }
        )


def test_load_sample_pipeline_dir():
    nodes = load_pipeline_dir("examples/pipelines")

    ids = [node.pipeline_id for node in nodes]

    assert ids == ["database", "prepare", "workflow"]

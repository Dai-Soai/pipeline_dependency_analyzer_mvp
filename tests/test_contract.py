from pipeline_dependency_analyzer import (
    DependencyIssue,
    DependencyNode,
    DependencyResult,
)


def test_dependency_node():
    node = DependencyNode(
        pipeline_id="workflow",
        dependencies=["database", "prepare"],
    )

    assert node.pipeline_id == "workflow"
    assert len(node.dependencies) == 2


def test_dependency_issue():
    issue = DependencyIssue(
        code="cycle",
        message="Circular dependency detected.",
    )

    assert issue.code == "cycle"


def test_dependency_result_success():
    result = DependencyResult(ok=True)

    assert result.ok is True
    assert result.nodes == []
    assert result.issues == []


def test_dependency_result_contains_node():
    node = DependencyNode("workflow")

    result = DependencyResult(
        ok=True,
        nodes=[node],
    )

    assert result.nodes[0].pipeline_id == "workflow"

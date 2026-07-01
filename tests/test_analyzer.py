from pipeline_dependency_analyzer.analyzer import analyze_dependencies
from pipeline_dependency_analyzer.contract import DependencyNode


def test_analyze_dependencies_passes():
    nodes = [
        DependencyNode("database"),
        DependencyNode("prepare", ["database"]),
        DependencyNode("workflow", ["prepare"]),
    ]

    result = analyze_dependencies(nodes)

    assert result.ok is True
    assert [node.pipeline_id for node in result.nodes] == [
        "database",
        "prepare",
        "workflow",
    ]
    assert result.issues == []


def test_analyze_dependencies_detects_missing_dependency():
    nodes = [
        DependencyNode("workflow", ["missing"]),
    ]

    result = analyze_dependencies(nodes)

    assert result.ok is False
    assert len(result.issues) == 1
    assert result.issues[0].code == "missing_dependency"


def test_analyze_dependencies_detects_cycle():
    nodes = [
        DependencyNode("a", ["b"]),
        DependencyNode("b", ["a"]),
    ]

    result = analyze_dependencies(nodes)

    assert result.ok is False
    assert len(result.issues) == 1
    assert result.issues[0].code == "cycle_detected"

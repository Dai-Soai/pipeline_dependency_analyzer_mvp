from pipeline_dependency_analyzer.contract import DependencyNode
from pipeline_dependency_analyzer.graph import (
    build_dependency_graph,
    detect_cycles,
    find_missing_dependencies,
    get_all_pipeline_ids,
    get_dependencies,
    graph_has_cycles,
    graph_has_node,
)


def test_build_dependency_graph():
    nodes = [
        DependencyNode("database"),
        DependencyNode("prepare", ["database"]),
        DependencyNode("workflow", ["prepare"]),
    ]

    graph = build_dependency_graph(nodes)

    assert graph == {
        "database": [],
        "prepare": ["database"],
        "workflow": ["prepare"],
    }


def test_get_all_pipeline_ids():
    nodes = [
        DependencyNode("database"),
        DependencyNode("prepare", ["database"]),
    ]

    assert get_all_pipeline_ids(nodes) == {"database", "prepare"}


def test_find_missing_dependencies():
    nodes = [
        DependencyNode("workflow", ["prepare", "missing"]),
        DependencyNode("prepare", []),
    ]

    missing = find_missing_dependencies(nodes)

    assert missing == ["missing"]


def test_find_missing_dependencies_returns_empty_list():
    nodes = [
        DependencyNode("database"),
        DependencyNode("prepare", ["database"]),
    ]

    missing = find_missing_dependencies(nodes)

    assert missing == []


def test_graph_has_node():
    graph = {
        "database": [],
        "prepare": ["database"],
    }

    assert graph_has_node(graph, "database") is True
    assert graph_has_node(graph, "missing") is False


def test_get_dependencies():
    graph = {
        "database": [],
        "prepare": ["database"],
    }

    assert get_dependencies(graph, "prepare") == ["database"]
    assert get_dependencies(graph, "missing") == []


def test_detect_cycles_returns_empty_list_for_acyclic_graph():
    graph = {
        "database": [],
        "prepare": ["database"],
        "workflow": ["prepare"],
    }

    assert detect_cycles(graph) == []
    assert graph_has_cycles(graph) is False


def test_detect_cycles_detects_simple_cycle():
    graph = {
        "a": ["b"],
        "b": ["c"],
        "c": ["a"],
    }

    cycles = detect_cycles(graph)

    assert cycles == [["a", "b", "c", "a"]]
    assert graph_has_cycles(graph) is True


def test_detect_cycles_detects_self_cycle():
    graph = {
        "a": ["a"],
    }

    cycles = detect_cycles(graph)

    assert cycles == [["a", "a"]]
    assert graph_has_cycles(graph) is True

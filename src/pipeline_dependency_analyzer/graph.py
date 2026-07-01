from pipeline_dependency_analyzer.contract import DependencyNode


def build_dependency_graph(nodes: list[DependencyNode]) -> dict[str, list[str]]:
    return {node.pipeline_id: list(node.dependencies) for node in nodes}


def get_all_pipeline_ids(nodes: list[DependencyNode]) -> set[str]:
    return {node.pipeline_id for node in nodes}


def find_missing_dependencies(nodes: list[DependencyNode]) -> list[str]:
    pipeline_ids = get_all_pipeline_ids(nodes)
    missing: set[str] = set()

    for node in nodes:
        for dependency in node.dependencies:
            if dependency not in pipeline_ids:
                missing.add(dependency)

    return sorted(missing)


def graph_has_node(graph: dict[str, list[str]], pipeline_id: str) -> bool:
    return pipeline_id in graph


def get_dependencies(graph: dict[str, list[str]], pipeline_id: str) -> list[str]:
    return graph.get(pipeline_id, [])

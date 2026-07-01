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


def detect_cycles(graph: dict[str, list[str]]) -> list[list[str]]:
    visited: set[str] = set()
    visiting: set[str] = set()
    stack: list[str] = []
    cycles: list[list[str]] = []

    def visit(node: str) -> None:
        if node in visiting:
            cycle_start = stack.index(node)
            cycles.append(stack[cycle_start:] + [node])
            return

        if node in visited:
            return

        visiting.add(node)
        stack.append(node)

        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)

        stack.pop()
        visiting.remove(node)
        visited.add(node)

    for node in graph:
        visit(node)

    return cycles


def graph_has_cycles(graph: dict[str, list[str]]) -> bool:
    return len(detect_cycles(graph)) > 0


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    visited: set[str] = set()
    visiting: set[str] = set()
    order: list[str] = []

    def visit(node: str) -> None:
        if node in visiting:
            raise ValueError(f"Cycle detected at node: {node}")

        if node in visited:
            return

        visiting.add(node)

        for dependency in graph.get(node, []):
            if dependency in graph:
                visit(dependency)

        visiting.remove(node)
        visited.add(node)
        order.append(node)

    for node in graph:
        visit(node)

    return order

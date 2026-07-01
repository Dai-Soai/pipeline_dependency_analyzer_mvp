from pipeline_dependency_analyzer.contract import (
    DependencyIssue,
    DependencyNode,
    DependencyResult,
)
from pipeline_dependency_analyzer.graph import (
    build_dependency_graph,
    detect_cycles,
    find_missing_dependencies,
    topological_sort,
)


def analyze_dependencies(nodes: list[DependencyNode]) -> DependencyResult:
    graph = build_dependency_graph(nodes)
    issues: list[DependencyIssue] = []

    missing = find_missing_dependencies(nodes)
    for dependency in missing:
        issues.append(
            DependencyIssue(
                code="missing_dependency",
                message=f"Missing dependency: {dependency}",
            )
        )

    cycles = detect_cycles(graph)
    for cycle in cycles:
        issues.append(
            DependencyIssue(
                code="cycle_detected",
                message=f"Cycle detected: {' -> '.join(cycle)}",
            )
        )

    if issues:
        return DependencyResult(
            ok=False,
            nodes=nodes,
            issues=issues,
        )

    execution_order = topological_sort(graph)

    return DependencyResult(
        ok=True,
        nodes=[
            DependencyNode(
                pipeline_id=pipeline_id,
                dependencies=graph[pipeline_id],
            )
            for pipeline_id in execution_order
        ],
        issues=[],
    )

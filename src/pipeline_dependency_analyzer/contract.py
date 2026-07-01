from dataclasses import dataclass, field
from typing import List


@dataclass
class DependencyNode:
    """
    Represents one pipeline.
    """

    pipeline_id: str
    dependencies: List[str] = field(default_factory=list)


@dataclass
class DependencyIssue:
    """
    Represents one dependency issue.
    """

    code: str
    message: str


@dataclass
class DependencyResult:
    """
    Final dependency analysis result.
    """

    ok: bool
    nodes: List[DependencyNode] = field(default_factory=list)
    issues: List[DependencyIssue] = field(default_factory=list)

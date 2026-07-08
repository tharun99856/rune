from dataclasses import dataclass, field
from typing import List, Optional, Union


@dataclass(frozen=True)
class Take:
    count: int


@dataclass(frozen=True)
class Order:
    key: str
    descending: bool = False


@dataclass(frozen=True)
class Group:
    source: str
    key: str


@dataclass(frozen=True)
class Count:
    noun: str


@dataclass(frozen=True)
class Explore:
    source: str
    start: str
    target: Optional[str] = None


Step = Union[Take, Order, Group, Count, Explore]


@dataclass(frozen=True)
class TransformationGraph:
    steps: List[Step] = field(default_factory=list)

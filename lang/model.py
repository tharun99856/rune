from dataclasses import dataclass, field
from typing import List, Union


@dataclass(frozen=True)
class Take:
    count: int


@dataclass(frozen=True)
class Order:
    key: str
    descending: bool = False


Step = Union[Take, Order]


@dataclass(frozen=True)
class TransformationGraph:
    steps: List[Step] = field(default_factory=list)

from dataclasses import dataclass, field
from typing import List, Union


@dataclass(frozen=True)
class Take:
    count: int


Step = Union[Take]


@dataclass(frozen=True)
class TransformationGraph:
    steps: List[Step] = field(default_factory=list)

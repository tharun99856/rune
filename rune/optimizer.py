from dataclasses import dataclass

from rune.model import Order, Take


@dataclass(frozen=True)
class TopK:
    key: str
    descending: bool
    count: int


@dataclass(frozen=True)
class RewriteExplanation:
    rule: str
    before: str
    after: str
    reason: str


def optimize(steps):
    new_steps = []
    explanations = []
    i = 0
    while i < len(steps):
        step = steps[i]
        if isinstance(step, Order) and i + 1 < len(steps) and isinstance(steps[i + 1], Take):
            take = steps[i + 1]
            new_steps.append(TopK(key=step.key, descending=step.descending, count=take.count))
            direction = "DESC" if step.descending else "ASC"
            explanations.append(
                RewriteExplanation(
                    rule="ORDER_TAKE_TO_TOP_K",
                    before=f"ORDER BY {step.key} {direction} + TAKE {take.count}",
                    after=f"TOP_K({step.key}, {take.count})",
                    reason=(
                        "ORDER immediately followed by TAKE recognized as top-k "
                        "selection; a heap of size k avoids fully sorting the input."
                    ),
                )
            )
            i += 2
        else:
            new_steps.append(step)
            i += 1
    return new_steps, explanations

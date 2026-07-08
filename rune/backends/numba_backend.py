import numpy as np
from numba import njit

from rune.backend import Backend
from rune.model import Count, Group
from rune.optimizer import TopK
from rune.runner import CountedBucket


@njit(cache=True)
def _bincount(data, domain_size):
    counts = np.zeros(domain_size, dtype=np.int64)
    for x in data:
        counts[x] += 1
    return counts


class NumbaBackend(Backend):
    """Compiles Group(BY value) -> Count -> TopK to real machine code via
    LLVM (through numba/llvmlite). Only supports that exact shape -- this is
    a proof the pattern works, not a general Rune executor. Falls back to
    InterpreterBackend for anything else.

    Requires the value domain to be a bounded range of non-negative
    integers, known ahead of time -- a real, stated precondition, not a
    hidden assumption.
    """

    def __init__(self, domain_size: int):
        self.domain_size = domain_size

    def supports(self, steps) -> bool:
        return (
            len(steps) == 3
            and isinstance(steps[0], Group)
            and steps[0].key == "value"
            and isinstance(steps[1], Count)
            and isinstance(steps[2], TopK)
            and steps[2].descending  # only the descending (top-k) case is implemented and tested
        )

    def run(self, steps, data):
        topk = steps[2]
        arr = np.asarray(data, dtype=np.int64)
        if arr.size and (arr.min() < 0 or arr.max() >= self.domain_size):
            raise ValueError(
                f"data contains values outside declared domain [0, {self.domain_size})"
            )
        counts = _bincount(arr, self.domain_size)
        k = min(topk.count, int(np.count_nonzero(counts)))
        if k == 0:
            return []
        # Deterministic tie-break: count descending, then key ascending --
        # must match InterpreterBackend's rule exactly (see runner.py's
        # _tiebreak), or switching backends can silently change which tied
        # element you get. Encoded as one combined score so argpartition/
        # argsort only ever need to compare a single number.
        idx = np.arange(self.domain_size, dtype=np.int64)
        combined = counts * (self.domain_size + 1) - idx
        top_idx = np.argpartition(combined, -k)[-k:]
        top_idx = top_idx[np.argsort(-combined[top_idx])]
        return [CountedBucket(key=int(i), count=int(counts[i])) for i in top_idx]

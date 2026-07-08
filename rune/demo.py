import random
import time

from rune.backends.interpreter_backend import InterpreterBackend
from rune.optimizer import optimize
from rune.parser import parse_program

PROGRAM = "GROUP nums BY value\nCOUNT EACH group\nORDER BY count DESC\nTAKE 10"


def _pairs(buckets):
    return sorted((b.key, b.count) for b in buckets)


def run_demo(data_size=500_000, domain_size=1000, seed=42):
    rng = random.Random(seed)
    data = [rng.randint(0, domain_size - 1) for _ in range(data_size)]

    lines = []
    lines.append("Rune source:")
    for line in PROGRAM.splitlines():
        lines.append(f"  {line}")
    lines.append("")

    graph = parse_program(PROGRAM)
    optimized_steps, explanations = optimize(graph.steps)

    lines.append("Optimizer:")
    for exp in explanations:
        lines.append(f"  Rewrote: {exp.before}")
        lines.append(f"      ->   {exp.after}")
        lines.append(f"  Reason:  {exp.reason}")
    lines.append("")

    interpreter = InterpreterBackend()

    t0 = time.perf_counter()
    naive_result = interpreter.run(graph.steps, data)
    naive_ms = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    optimized_result = interpreter.run(optimized_steps, data)
    optimized_ms = (time.perf_counter() - t0) * 1000

    if _pairs(naive_result) != _pairs(optimized_result):
        lines.append("MISMATCH: optimized result disagrees with naive result -- STOP, this is a bug.")
        return "\n".join(lines)

    lines.append(f"Data: {data_size:,} items, domain [0, {domain_size})")
    lines.append(f"Naive interpreter    (full sort):  {naive_ms:8.2f} ms")
    lines.append(f"Optimized interpreter (heap top-k): {optimized_ms:8.2f} ms")
    lines.append(f"Speedup from the optimizer alone: {naive_ms / optimized_ms:.2f}x (no compilation involved)")
    lines.append("")

    try:
        from rune.backends.numba_backend import NumbaBackend

        numba_backend = NumbaBackend(domain_size=domain_size)
        numba_backend.run(optimized_steps, data[:100])  # warm up JIT; exclude compile time

        t0 = time.perf_counter()
        numba_result = numba_backend.run(optimized_steps, data)
        numba_ms = (time.perf_counter() - t0) * 1000

        if _pairs(numba_result) != _pairs(naive_result):
            lines.append("MISMATCH: numba backend disagrees with naive result -- STOP, this is a bug.")
            return "\n".join(lines)

        lines.append(f"Numba-compiled (real LLVM, same TOP_K plan): {numba_ms:8.2f} ms")
        lines.append(f"Speedup over naive interpreted: {naive_ms / numba_ms:.2f}x")
    except ImportError:
        lines.append("(numba not installed -- skipping compiled comparison.")
        lines.append(" pip install -r requirements-backends.txt to see it.)")

    return "\n".join(lines)


if __name__ == "__main__":
    print(run_demo())

"""A real C++ backend: Rune plan -> generated C++ -> compiled with zig c++
-> native executable -> run.

Supports specific recognized optimized-plan shapes (the ones the optimizer
produces proofs for), not arbitrary compositions -- honest about its narrow,
per-shape coverage rather than pretending to be a general C++ compiler.
Compilation uses `python -m ziglang c++`, a self-contained clang/C++
toolchain that installs from pip with no system compiler required.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from rune.backend import Backend
from rune.model import Count, Group
from rune.optimizer import KadaneScan, TopK
from rune.runner import CountedBucket

# --- Kadane: C headers only, so no libc++ (fast, warning-free compile) ------
_KADANE_TEMPLATE = r"""#include <cstdio>
#include <cstdlib>

int main(int argc, char** argv) {{
    if (argc < 2) {{ return 1; }}
    FILE* f = fopen(argv[1], "r");
    if (!f) {{ return 1; }}
    long long n;
    if (fscanf(f, "%lld", &n) != 1 || n <= 0) {{ printf("NONE\n"); fclose(f); return 0; }}
    long long* a = (long long*)malloc(sizeof(long long) * n);
    for (long long i = 0; i < n; i++) {{
        if (fscanf(f, "%lld", &a[i]) != 1) {{ a[i] = 0; }}
    }}
    fclose(f);

    long long best = a[0], run = a[0];
    for (long long i = 1; i < n; i++) {{
        long long v = a[i];
        long long ext = run + v;
        run = (v {cmp} ext) ? v : ext;
        if (run {cmp} best) best = run;
    }}
    printf("%lld\n", best);
    free(a);
    return 0;
}}
"""

# --- Top-K: frequency count + partial selection, tie-break count desc/key asc
# (must match rune.runner's tie-break exactly, or the two backends disagree).
_TOPK_TEMPLATE = r"""#include <cstdio>
#include <map>
#include <vector>
#include <algorithm>

int main(int argc, char** argv) {{
    if (argc < 2) {{ return 1; }}
    FILE* f = fopen(argv[1], "r");
    if (!f) {{ return 1; }}
    long long n;
    if (fscanf(f, "%lld", &n) != 1) {{ fclose(f); return 1; }}
    std::map<long long, long long> cnt;
    for (long long i = 0; i < n; i++) {{
        long long x;
        if (fscanf(f, "%lld", &x) == 1) cnt[x]++;
    }}
    fclose(f);

    std::vector<std::pair<long long, long long> > v;  // (key, count)
    for (std::map<long long, long long>::iterator it = cnt.begin(); it != cnt.end(); ++it)
        v.push_back(std::make_pair(it->first, it->second));
    std::sort(v.begin(), v.end(),
        [](const std::pair<long long,long long>& a, const std::pair<long long,long long>& b) {{
            if (a.second != b.second) return a.second > b.second;  // count desc
            return a.first < b.first;                              // key asc (tie-break)
        }});

    long long k = {k};
    for (long long i = 0; i < k && i < (long long)v.size(); i++)
        printf("%lld %lld\n", v[i].first, v[i].second);
    return 0;
}}
"""


def _is_topk_plan(steps):
    return (
        len(steps) == 3
        and isinstance(steps[0], Group)
        and steps[0].key == "value"
        and isinstance(steps[1], Count)
        and isinstance(steps[2], TopK)
        and steps[2].descending
    )


def _is_kadane_plan(steps):
    return len(steps) == 1 and isinstance(steps[0], KadaneScan)


def emit_cpp(steps) -> str:
    if _is_kadane_plan(steps):
        cmp = ">" if steps[0].direction == "maximize" else "<"
        return _KADANE_TEMPLATE.format(cmp=cmp)
    if _is_topk_plan(steps):
        return _TOPK_TEMPLATE.format(k=steps[2].count)
    raise ValueError(f"cpp backend cannot generate code for: {steps!r}")


class CppBackend(Backend):
    def supports(self, steps) -> bool:
        return _is_kadane_plan(steps) or _is_topk_plan(steps)

    def run(self, steps, data):
        source = emit_cpp(steps)
        with tempfile.TemporaryDirectory() as d:
            d = Path(d)
            src = d / "prog.cpp"
            exe = d / ("prog.exe" if sys.platform == "win32" else "prog")
            datafile = d / "data.txt"

            src.write_text(source)
            datafile.write_text(str(len(data)) + "\n" + " ".join(str(x) for x in data))

            subprocess.run(
                [sys.executable, "-m", "ziglang", "c++", str(src), "-O2", "-w", "-o", str(exe)],
                capture_output=True, check=True, timeout=120,
            )
            out = subprocess.run(
                [str(exe), str(datafile)], capture_output=True, text=True, check=True, timeout=60,
            ).stdout.strip()

        if _is_topk_plan(steps):
            buckets = []
            for line in out.splitlines():
                if line.strip():
                    key, count = line.split()
                    buckets.append(CountedBucket(key=int(key), count=int(count)))
            return buckets
        return None if out == "NONE" else int(out)

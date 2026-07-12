"""A real C++ backend: Rune plan -> generated C++ -> compiled with zig c++
-> native executable -> run.

Supports only the KadaneScan plan (MAXIMIZE|MINIMIZE SUM OVER CONTIGUOUS)
for now -- a genuine compiled path, not a stub, kept honest about its narrow
coverage. Compilation uses `python -m ziglang c++`, a self-contained
clang/C++ toolchain that installs from pip with no system compiler required.
"""

import subprocess
import sys
import tempfile
from pathlib import Path

from rune.backend import Backend
from rune.optimizer import KadaneScan

# Deliberately C headers only (no <vector>/<string>) so the generated program
# doesn't pull in libc++ -- faster compiles, and none of the header warnings.
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


def emit_cpp(steps) -> str:
    if len(steps) == 1 and isinstance(steps[0], KadaneScan):
        cmp = ">" if steps[0].direction == "maximize" else "<"
        return _KADANE_TEMPLATE.format(cmp=cmp)
    raise ValueError(f"cpp backend cannot generate code for: {steps!r}")


class CppBackend(Backend):
    def supports(self, steps) -> bool:
        return len(steps) == 1 and isinstance(steps[0], KadaneScan)

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

        return None if out == "NONE" else int(out)

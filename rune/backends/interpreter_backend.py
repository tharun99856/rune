from rune.backend import Backend
from rune.runner import run_program


class InterpreterBackend(Backend):
    """Reference backend: pure Python, always correct, never the fast path.

    The only backend guaranteed to run any plan Rune can produce.
    """

    def supports(self, steps) -> bool:
        return True

    def run(self, steps, data):
        return run_program(steps, data)

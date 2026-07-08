from abc import ABC, abstractmethod


class Backend(ABC):
    """Executes an optimized plan against data.

    A backend does not have to support every plan shape. supports() lets a
    caller check before attempting run() -- InterpreterBackend is the only
    backend guaranteed to run everything; specialized backends (NumbaBackend,
    and eventually LLVM/Rust/C++ backends) opt into narrower, faster paths
    for the specific patterns they recognize, and fall back otherwise.
    """

    @abstractmethod
    def supports(self, steps) -> bool:
        ...

    @abstractmethod
    def run(self, steps, data):
        ...

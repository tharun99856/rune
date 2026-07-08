import pytest

from rune.backend import Backend


def test_backend_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        Backend()

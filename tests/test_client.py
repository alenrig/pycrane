import pytest
from pycrane.client import Pycrane


def test_client_init():
    with pytest.raises(ValueError):
        Pycrane()

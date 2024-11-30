"""Client testing module."""

import pytest

from pycrane.client import Pycrane


def test_client_init():
    """Test client initialization."""
    with pytest.raises(ValueError):
        Pycrane()

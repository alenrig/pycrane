"""Client testing module."""

from contextlib import nullcontext

import pytest

from pycrane.client import Pycrane


@pytest.mark.parametrize(
    ["username", "password", "authfile", "expectation", "error_msg"],
    [
        (None, None, None, pytest.raises(ValueError), "Specify auth method"),
        (
            "a",
            None,
            None,
            pytest.raises(ValueError),
            "Both username and password should be defined",
        ),
        (
            None,
            "b",
            None,
            pytest.raises(ValueError),
            "Both username and password should be defined",
        ),
        (
            "a",
            None,
            "path",
            pytest.raises(ValueError),
            "Both username and password should be defined",
        ),
        (
            None,
            "b",
            "path",
            pytest.raises(ValueError),
            "Both username and password should be defined",
        ),
        (
            "a",
            "b",
            "path",
            pytest.raises(ValueError),
            "Only one of authfile or username should be defined",
        ),
        ("a", "b", None, nullcontext(), ""),
        (None, None, "path", nullcontext(), ""),
    ],
)
def test_client_init(username, password, authfile, expectation, error_msg):
    """Test client initialization."""
    with expectation as e:
        Pycrane(username=username, password=password, authfile=authfile)
    if e:
        assert str(e.value) == error_msg

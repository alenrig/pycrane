"""Utils Testing Module"""
import pytest

from pycrane import utils


@pytest.mark.parametrize(
    ["url", "expected"],
    [
        ("registry-1.docker.io", "registry-1.docker.io"),
        ("registry-1.docker.io/", "registry-1.docker.io"),
        ("https://registry-1.docker.io", "registry-1.docker.io"),
        ("https://registry-1.docker.io/", "registry-1.docker.io"),
        ("registry-1.docker.io:8080", "registry-1.docker.io:8080"),
        ("registry-1.docker.io:8080/", "registry-1.docker.io:8080"),
        ("https://registry-1.docker.io:8080", "registry-1.docker.io:8080"),
        ("https://registry-1.docker.io:8080/", "registry-1.docker.io:8080"),
    ]
)
def test_get_base_url(url, expected):
    """Test get_base_url"""
    assert utils.get_base_url(url) == expected

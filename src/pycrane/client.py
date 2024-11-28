"""Wrapper for the registry API."""

from typing import Optional


class Pycrane:
    """Represents a Registry server connection."""

    def __init__(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authfile: Optional[str] = None,
    ) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.authfile = authfile

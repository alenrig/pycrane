"""Wrapper for the registry API."""

from typing import Any, Optional

from requests import Response
from requests.auth import AuthBase, HTTPBasicAuth


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
        self._set_auth_info()

    def _set_auth_info(self) -> None:
        if (self.username and not self.password) or (
            not self.username and self.password
        ):
            raise ValueError("Both username and password should be defined")
        if self.authfile and self.username:
            raise ValueError(
                "Only one of authfile or username should be defined"
            )
        self._auth: Optional[AuthBase] = None
        if self.username and self.password:
            self._auth = HTTPBasicAuth(self.username, self.password)

    def http_get(
        self, path: str, query_data: Optional[dict[str, Any]] = None
    ) -> Response:
        """Make a GET request to the Docker Registry server.

        Args:
            path (str): path to query.
            query_data (Optional[dict[str, Any]], optional): data to send
                as query parameters. Defaults to None.

        Returns:
            Response: request result
        """

    def http_post(
        self, path: str, query_data: Optional[dict[str, Any]] = None
    ) -> Response:
        """Make a POST request to the Docker Registry server.

        Args:
            path (str): path to query.
            query_data (Optional[dict[str, Any]], optional): data to send
                as query parameters. Defaults to None.

        Returns:
            Response: _description_
        """

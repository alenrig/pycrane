"""Wrapper for the registry API."""

from typing import Optional

from requests.auth import AuthBase, HTTPBasicAuth

from pycrane import utils


class Pycrane:
    """Represents a Registry server connection."""

    def __init__(
        self,
        url: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        authfile: Optional[str] = None,
        api_version: str = "2",
    ) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.authfile = authfile
        self._base_url = utils.get_base_url(url)
        self._api_version = api_version
        self._url = f"{self._base_url}/api/v{api_version}"
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

    def _build_url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        return f"{self._url}/{path}"

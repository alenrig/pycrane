"""Wrapper for the registry API."""

from pathlib import Path

import www_authenticate
from requests.auth import AuthBase, HTTPBasicAuth

from pycrane.backend import HTTPBackend
from pycrane.utils import get_authfile_credentials, get_base_url


class Pycrane:
    """Represents a Registry server connection."""

    def __init__(
        self,
        url: str = "registry-1.docker.io",
        username: str | None = None,
        password: str | None = None,
        authfile: str | None = None,
    ) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.authfile = authfile
        self.api_version = 2
        self._backend = HTTPBackend(url=self._base_url, auth=self._auth)

    @property
    def _base_url(self) -> str:
        return get_base_url(self.url)

    @property
    def _url(self) -> str:
        return f"{self._base_url}/v{self.api_version}"

    @property
    def _auth(self) -> AuthBase:
        if not any([self.username, self.password, self.authfile]):
            raise ValueError("Specify auth method")
        if (self.username and not self.password) or (
            not self.username and self.password
        ):
            raise ValueError("Both username and password should be defined")
        if self.authfile and self.username:
            raise ValueError(
                "Only one of authfile or username should be defined"
            )
        if self.authfile:
            return get_authfile_credentials(
                Path(self.authfile), self._base_url
            )
        return HTTPBasicAuth(str(self.username), str(self.password))

    def get_token(self) -> str | None:
        """Get registry JWT token.

        Returns:
            str | None: token on successful auth.
        """
        response = self._backend.http_get(url=self._url)
        auth_headers = www_authenticate.parse(
            response.headers["WWW-Authenticate"]
        )
        bearer: dict[str, str] = auth_headers.get("bearer", {})
        realm = bearer.get("realm", "")
        service = bearer.get("service", "")
        auth_url = f"{realm}?service={service}&client_id=pycrane"
        response = self._backend.http_get(url=auth_url)
        content = response.json()
        if isinstance(content, dict):
            return content.get("token")
        return None

    def inspect(self, image: str) -> str:
        """Get image manifest.

        Args:
            image (str): full image path to inspect.

        Returns:
            str: image manifest if exists.
        """
        return image

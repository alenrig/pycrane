"""Wrapper for the registry API."""

from pathlib import Path

import www_authenticate
from httpx import Auth, BasicAuth, Response

from pycrane.backend import BearerAuth, HTTPBackend
from pycrane.utils import get_authfile_credentials, get_netloc


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

    @property
    def _base_url(self) -> str:
        return get_netloc(self.url)

    @property
    def _url(self) -> str:
        return f"{self._base_url}/v{self.api_version}"

    @property
    def _auth(self) -> Auth:
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
            username, password = get_authfile_credentials(
                Path(self.authfile), self._base_url
            )
            return BasicAuth(username, password)
        return BasicAuth(str(self.username), str(self.password))

    @property
    def _authenticator(self) -> HTTPBackend:
        return HTTPBackend(url=self._base_url, auth=self._auth)

    @property
    def _backend(self) -> HTTPBackend:
        return HTTPBackend(
            url=self._base_url, auth=BearerAuth(token=self._request_token())
        )

    def _request_token(self) -> str:
        response = self._authenticator.http_get(url=self._url)
        auth_headers = www_authenticate.parse(
            response.headers["WWW-Authenticate"]
        )
        bearer: dict[str, str] = auth_headers.get("bearer", {})
        realm = bearer.get("realm", "")
        service = bearer.get("service", "")
        auth_url = f"{realm}?service={service}&client_id=pycrane"
        response = self._authenticator.http_get(url=auth_url)
        return self._get_token(response=response)

    def _get_token(self, response: Response) -> str:
        content = response.json()
        if isinstance(content, dict) and content.get("token"):
            return str(content.get("token"))
        raise Exception("Can`t get auth token")

    def inspect(self, image: str) -> str:
        """Get image manifest.

        Args:
            image (str): full image path to inspect.

        Returns:
            str: image manifest if exists.
        """
        return image

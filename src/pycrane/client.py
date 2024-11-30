"""Wrapper for the registry API."""

from pathlib import Path

from requests.auth import AuthBase, HTTPBasicAuth

from pycrane.utils import get_authfile_credentials, get_base_url


class Pycrane:
    """Represents a Registry server connection."""

    def __init__(
        self,
        url: str | None = None,
        username: str | None = None,
        password: str | None = None,
        authfile: Path | None = None,
    ) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.authfile = authfile
        self._set_auth_info()
        self._base_url = get_base_url(url)

    def _set_auth_info(self) -> None:
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
        self._auth: AuthBase | None = None
        if self.username and self.password:
            self._auth = HTTPBasicAuth(self.username, self.password)
        if self.authfile:
            self._auth = get_authfile_credentials(
                self.authfile, self._base_url
            )

    def inspect(self, image: str) -> str:
        """Get image metadata.

        Args:
            image (str): image to inpect.

        Returns:
            str: result
        """
        return image

    def mock(self) -> None:
        """Mock method
        """

"""HTTP Backend module for http calls."""

from requests import Response, Session
from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token: str):
        self._token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self._token
        return r


class HTTPBackend:
    """Class for http calls."""

    def __init__(self, url: str, auth: AuthBase | None = None) -> None:
        self._url = url
        self._auth = auth

    @property
    def _session(self) -> Session:
        session = Session()
        if self._auth:
            session.auth = self._auth
        return session

    def http_get(self, url: str) -> Response:
        """Make GET HTTP request.

        Args:
            url (str): path for request.

        Returns:
            Response: result of request.
        """
        return self._session.request(method="get", url=url)

    def http_post(self, url: str) -> Response:
        """Make POST HTTP request.

        Args:
            url (str): path for request.

        Returns:
            Response: result of request.
        """
        return self._session.request(method="post", url=url)

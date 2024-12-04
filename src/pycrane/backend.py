"""HTTP Backend module for http calls."""

from httpx import Auth, Client, Response


class BearerAuth(Auth):
    def __init__(self, token: str):
        self._token = token

    def auth_flow(self, request):
        request.headers["authorization"] = "Bearer " + self._token


class HTTPBackend:
    """Class for http calls."""

    def __init__(self, url: str, auth: Auth | None = None) -> None:
        self._url = url
        self._auth = auth

    def _client(self) -> Client:
        return Client(auth=self._auth)

    def http_get(self, url: str) -> Response:
        """Make GET HTTP request.

        Args:
            url (str): path for request.

        Returns:
            Response: result of request.
        """
        with self._client() as client:
            return client.get(url=url)

    def http_post(self, url: str) -> Response:
        """Make POST HTTP request.

        Args:
            url (str): path for request.

        Returns:
            Response: result of request.
        """
        with self._client() as client:
            return client.post(url=url)

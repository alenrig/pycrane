"""HTTP Backend module for http calls."""

import www_authenticate
from requests import Session
from requests.auth import HTTPBasicAuth


class HTTPBackend:
    """Class for http calls."""

    def __init__(
        self, url: str, username: str, password: str, verify_ssl: bool = True
    ) -> None:
        self._url = url
        self._username = username
        self._password = password
        self._verify_ssl = verify_ssl

    @property
    def _session(self) -> Session:
        session = Session()
        session.verify = self._verify_ssl
        auth = HTTPBasicAuth(username=self._username, password=self._password)
        session.auth = auth
        return session

    def _get_token(self) -> str | None:
        url = "https://registry-1.docker.io/v2"
        response = self._session.get(url=url)
        auth_headers = www_authenticate.parse(
            response.headers["WWW-Authenticate"]
        )
        bearer: dict[str, str] = auth_headers.get("bearer", {})
        realm = bearer.get("realm", "")
        service = bearer.get("service", "")
        auth_url = f"{realm}?service={service}&client_id=pycrane"
        response = self._session.get(url=auth_url)
        content = response.json()
        if isinstance(content, dict):
            return content.get("token")
        return None

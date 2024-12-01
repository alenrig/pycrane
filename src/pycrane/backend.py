"""HTTP Backend module for http calls."""

import www_authenticate
from requests import Session


class HTTPBackend:
    """Class for http calls."""

    @property
    def _session(self) -> Session:
        session = Session()
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

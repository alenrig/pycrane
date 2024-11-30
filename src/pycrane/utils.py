"""Utils module."""

import json
from pathlib import Path

from requests.auth import HTTPBasicAuth

from pycrane import const


def get_base_url(url: str | None = None) -> str:
    """Returns the base url with the trailing slash stripped.
    If the URL is not provided, the default URL is returned.

    Args:
        url (str | None, optional): url to strip. Defaults to None.

    Returns:
        str: the base url
    """
    if url:
        return url.rstrip("/")
    return const.DEFAULT_URL


def get_authfile_credentials(authfile: Path, base_url: str) -> HTTPBasicAuth:
    """Get endpoint credentials from provided docker authfile.

    Args:
        authfile (Path): docker authfile in json format.
        base_url (str): base url of registry.

    Returns:
        HTTPBasicAuth: auth for endpoint
    """
    with open(authfile, mode="rb") as file:
        credentials: dict = json.loads(file.read()).get("auths", {})
    endpoint_credentials = credentials.get(base_url, {})
    username = endpoint_credentials.get("username", "")
    password = endpoint_credentials.get("password", "")
    if not any([username, password]):
        raise ValueError(f"Not found credentials for {base_url}")
    return HTTPBasicAuth(username=username, password=password)

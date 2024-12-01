"""Utils module."""

import json
from pathlib import Path
from urllib.parse import urlparse

from requests.auth import HTTPBasicAuth


def get_netloc(url: str) -> str:
    """Get url network location.

    Args:
        url (str): url to parse.

    Returns:
        str: network location. Example docker.io for https://docker.io/path.
    """
    if not url.startswith("http"):
        url = "//" + url
    return urlparse(url).netloc


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

"""Utils module."""

from typing import Optional

from pycrane import const


def get_base_url(url: Optional[str] = None) -> str:
    """Returns the base url with the trailing slash stripped.
    If the URL is not provided, the default URL is returned.

    Args:
        url (Optional[str], optional): url to strip. Defaults to None.

    Returns:
        str: the base url
    """
    if url:
        return url.rstrip("/")
    return const.DEFAULT_URL

"""Utils module."""

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

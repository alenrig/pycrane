import requests
class HTTPClient:
    def __init__(self, host: str, verify_ssl: bool = False):
        self._host = host
        self._verify_ssl = verify_ssl

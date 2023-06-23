from __future__ import annotations

import http.client
import http.server
import json
import urllib.parse
from typing import Any, Dict, Optional

from ..typedefs import LazyProxy


class HttpClient(LazyProxy[http.client.HTTPConnection]):
    """A simple HTTP client"""

    DEFAULT_HEADERS = {
        "Content-Type": "text/plain; charset=utf-8",
        "User-Agent": "Oscar Bahamonde <oscar.bahamonde.dev@gmail.com>",
    }

    def __load__(self) -> http.client.HTTPConnection:
        return http.client.HTTPConnection("localhost", 8080)

    def request(
        self, url: str, method: str, headers: Optional[Dict[str, str]], body: Any
    ):
        """Send a request to a URL"""
        parsed_url = urllib.parse.urlparse(url)
        conn = self._get_connection(parsed_url)
        headers = self._prepare_headers(headers)

        if headers.get("Content-Type") == "application/x-www-form-urlencoded":
            body = self._url_encode_body(body)
        if body is not None:
            conn.request(method, parsed_url.path, body.encode(), headers)
            with conn.getresponse() as res:
                response_headers = self._parse_response_headers(res)
                response_body = self._parse_response_body(res, response_headers)
                return {
                    "status": res.status,
                    "headers": response_headers,
                    "body": response_body,
                }
        else:
            conn.request(method, parsed_url.path, None, headers)
            with conn.getresponse() as res:
                response_headers = self._parse_response_headers(res)
                response_body = self._parse_response_body(res, response_headers)
                return {
                    "status": res.status,
                    "headers": response_headers,
                    "body": response_body,
                }

    def _url_encode_body(self, body: Dict[str, str]) -> str:
        """Encode the body as a URL-encoded string"""
        encoded_params = urllib.parse.urlencode(body)
        return encoded_params

    def get(self, url: str, headers: Optional[Dict[str, str]] = None):
        """Send a GET request to a URL"""
        return self.request(url, "GET", headers, None)

    def post(
        self, url: str, body: Dict[str, Any], headers: Optional[Dict[str, str]] = None
    ):
        """Send a POST request to a URL"""
        return self.request(url, "POST", headers, body)

    def put(self, url: str, body: Any, headers: Optional[Dict[str, str]] = None):
        """Send a PUT request to a URL"""
        return self.request(url, "PUT", headers, body)

    def delete(self, url: str, headers: Optional[Dict[str, str]] = None):
        """Send a DELETE request to a URL"""
        return self.request(url, "DELETE", headers, None)

    def _get_connection(self, parsed_url: urllib.parse.ParseResult):
        """Create an HTTPConnection or HTTPSConnection based on the URL scheme"""
        if parsed_url.scheme == "http":
            return http.client.HTTPConnection(parsed_url.netloc)
        elif parsed_url.scheme == "https":
            return http.client.HTTPSConnection(parsed_url.netloc)
        else:
            raise ValueError(f"Unsupported scheme: {parsed_url.scheme}")

    def _prepare_headers(self, headers: Optional[Dict[str, str]]):
        """Prepare headers with defaults"""
        prepared_headers = self.DEFAULT_HEADERS.copy()
        if headers:
            prepared_headers.update(headers)
        return prepared_headers

    def _parse_response_headers(self, response):
        """Parse response headers into a dictionary"""
        return {k.lower(): v for k, v in response.getheaders()}

    def _parse_response_body(self, response, headers):
        """Parse response body based on Content-Type header"""
        content_type = headers.get("content-type", "")
        if content_type.endswith("json"):
            return json.loads(response.read().decode())
        if content_type.startswith("text/"):
            return response.read().decode()
        if content_type.startswith("x-www-form-urlencoded"):
            return urllib.parse.parse_qs(response.read().decode())
        return response.read()
    
    
def main():
    """Run the HTTP client"""
    client = HttpClient()
    url = "http://localhost:8080"
    path = input("Enter path: ")
    method = input("Enter method: 1) GET 2) POST 3) PUT 4) DELETE: ")
    if method == "1":
        method = "GET"
    elif method == "2":
        method = "POST"
    elif method == "3":
        method = "PUT"
    elif method == "4":
        method = "DELETE"
    else:
        print("Invalid method")
        return
    response = client.request(url + path, method, None, None)
    print("Status: ", response["status"])
    print("Headers: ", response["headers"])
    print("Body: ", response["body"])
    print("Done")
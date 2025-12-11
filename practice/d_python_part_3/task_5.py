"""
Write a function that makes a request to some url
using urllib. Return status code and decoded response data in utf-8
Examples:
     >>> make_request('https://www.google.com')
     200, 'response data'
"""
from typing import Tuple
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import ssl


def make_request(url: str) -> Tuple[int, str]:
    """
    Makes an HTTP request to the given URL and returns the status code
    and decoded response data.

    :param url: The URL to request.
    :return: A tuple (status_code, decoded_data).
    """

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    req = Request(url)

    try:
        with urlopen(req, context=ssl_context) as response:
            status_code = response.getcode()
            data = response.read().decode('utf-8')

            return status_code, data

    except HTTPError as e:
        error_status_code = e.code
        error_data = e.read().decode('utf-8')
        return error_status_code, error_data

    except URLError as e:
        return 0, f"URL Error: {e.reason}"
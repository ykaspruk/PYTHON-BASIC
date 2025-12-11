"""
Write test for make_request function
Use Mock for mocking request with urlopen https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 200
    >>> m.method2.return_value = b'some text'
    >>> m.method()
    200
    >>> m.method2()
    b'some text'
"""
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError
import io
import http

from task_5 import make_request


@patch('task_5.urlopen')
def test_make_request_success_200(mock_urlopen):
    test_url = 'http://test.com/success'
    expected_data = '<html>Hello World</html>'
    expected_status = 200

    mock_response = Mock()
    mock_response.getcode.return_value = expected_status
    mock_response.read.return_value = expected_data.encode('utf-8')

    mock_urlopen.return_value.__enter__.return_value = mock_response

    status, data = make_request(test_url)

    assert status == expected_status
    assert data == expected_data


@patch('task_5.urlopen')
def test_make_request_http_error_404(mock_urlopen):
    test_url = 'http://test.com/404'
    error_body = 'Page not found.'
    expected_status = 404

    def side_effect(*args, **kwargs):
        raise HTTPError(
            test_url, expected_status, http.client.responses[expected_status], None,
            io.BytesIO(error_body.encode('utf-8'))
        )

    http_error_instance = HTTPError(
        test_url, expected_status, 'Not Found', None, io.BytesIO(error_body.encode('utf-8'))
    )
    http_error_instance.read = lambda: error_body.encode('utf-8')

    mock_urlopen.side_effect = http_error_instance

    status, data = make_request(test_url)

    assert status == expected_status
    assert data == error_body


@patch('task_5.urlopen')
def test_make_request_network_error(mock_urlopen):
    test_url = 'http://bad-domain-name-12345.com'
    error_reason = 'Name or service not known'
    expected_status = 0

    mock_urlopen.side_effect = URLError(reason=error_reason)

    status, data = make_request(test_url)

    assert status == expected_status
    assert data == f"URL Error: {error_reason}"
"""
write tests for is_http_domain function
"""
from task_3 import is_http_domain


def test_is_http_domain_http_no_slash():
    """Valid HTTP domain with no trailing slash."""
    assert is_http_domain('http://wikipedia.org') is True


def test_is_http_domain_https_with_slash():
    """Valid HTTPS domain with a trailing slash."""
    assert is_http_domain('https://ru.wikipedia.org/') is True


def test_is_http_domain_multiple_subdomains():
    """Valid domain with multiple subdomains."""
    assert is_http_domain('http://www.docs.google.com') is True


def test_is_http_domain_tld_min_length():
    """Valid domain with a 2-letter TLD."""
    assert is_http_domain('https://a.co') is True


def test_is_http_domain_tld_long():
    """Valid domain with a longer TLD."""
    assert is_http_domain('http://example.museum') is True


def test_is_http_domain_with_hyphens():
    """Valid domain containing hyphens."""
    assert is_http_domain('https://my-awesome-site.co.uk') is True


def test_is_http_domain_no_scheme():
    """Fails because the scheme (http://) is missing."""
    assert is_http_domain('griddynamics.com') is False


def test_is_http_domain_ftp_scheme():
    """Fails due to an incorrect scheme."""
    assert is_http_domain('ftp://example.org') is False


def test_is_http_domain_double_slash():
    """Fails due to multiple trailing slashes."""
    assert is_http_domain('https://example.org//') is False


def test_is_http_domain_tld_too_short():
    """Fails because TLD is only one letter."""
    assert is_http_domain('http://example.c') is False


def test_is_http_domain_ip_address():
    """Fails because IP addresses do not fit the domain name pattern (must be letters/hyphens)."""
    assert is_http_domain('http://192.168.1.1') is False


def test_is_http_domain_trailing_characters():
    """Fails because there are characters after the optional slash."""
    assert is_http_domain('https://example.com/path') is False


def test_is_http_domain_empty_string():
    """Fails for an empty string."""
    assert is_http_domain('') is False
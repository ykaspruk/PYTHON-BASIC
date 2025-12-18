"""
Write at least 2 tests on your choose.
Links:
    - requests docs: https://docs.python-requests.org/en/latest/
    - beautiful soup docs: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
    - lxml docs: https://lxml.de/
"""
import pytest
from unittest.mock import patch, MagicMock
from stock_info import get_most_active_codes, get_ceo_info, parse_float
from bs4 import BeautifulSoup
from stock_info import SESSION

# --- Mock Data ---

MOCK_MOST_ACTIVE_HTML = """
<html>
<body>
<table>
    <tbody>
        <tr class="data-row-0"><td>TSLA</td><td>Tesla, Inc.</td></tr>
        <tr class="data-row-1"><td>MSFT</td><td>Microsoft Corp.</td></tr>
        <tr class="data-row-2"><td>AAPL</td><td>Apple Inc.</td></tr>
    </tbody>
</table>
</body>
</html>
"""

MOCK_PROFILE_HTML = """
<html>
<body>
<section data-testid="key-dev-data">
    <div class="table-container">
        <table>
            <tbody>
                <tr><td class="key">Sector</td><td>Technology</td></tr>
                <tr><td class="key">Full Time Employees</td><td>221,000</td></tr>
            </tbody>
        </table>
    </div>
</section>
<section data-testid="management-section">
    <h3>Management</h3>
    <div class="test-ceo-row">
        <h3>Chief Executive Officer</h3>
        <div>
            <div>Satya Nadella</div>
            <span class="title">Chief Executive Officer</span>
        </div>
    </div>
    <p>... additional text (b. 1967) ...</p>
</section>
</body>
</html>
"""


# --- Tests ---

@pytest.fixture
def mock_response():
    """Fixture to mock requests.get response object."""
    mock = MagicMock()
    mock.raise_for_status.return_value = None
    return mock


@patch.object(SESSION, 'get')
def test_get_most_active_codes_success(mock_get, mock_response):
    """Test parsing of stock codes and names from the most active page."""

    mock_response.text = MOCK_MOST_ACTIVE_HTML
    mock_get.return_value = mock_response

    expected = [
        {'code': 'TSLA', 'name': 'Tesla, Inc.'},
        {'code': 'MSFT', 'name': 'Microsoft Corp.'},
        {'code': 'AAPL', 'name': 'Apple Inc.'}
    ]

    result = get_most_active_codes()

    assert result == expected
    mock_get.assert_called_once()


@patch('stock_info.fetch_and_parse')
def test_get_ceo_info_parsing_success(mock_fetch_and_parse):
    """Test successful parsing of CEO, Country, Employees, and Year Born from the profile tab."""
    mock_fetch_and_parse.return_value = BeautifulSoup(MOCK_PROFILE_HTML, 'lxml')
    code = 'MSFT'
    result = get_ceo_info(code)

    expected = {
        'CEO Name': 'Satya Nadella',
        'CEO Year Born': 1967,
        'Country': 'Technology',
        'Employees': 221000.0
    }

    assert result['CEO Name'] == expected['CEO Name']
    assert result['CEO Year Born'] == expected['CEO Year Born']
    assert result['Country'] == expected['Country']
    assert result['Employees'] == expected['Employees']

def test_parse_float_conversions():
    """Test the utility function for financial string parsing (K, M, B, %)."""

    assert parse_float("1.23M") == 1230000.0
    assert parse_float("500B") == 500000000000.0
    assert parse_float("1,000K") == 1000000.0
    assert parse_float("45.67%") == 0.4567
    assert parse_float("N/A") == 0.0
    assert parse_float("12345") == 12345.0
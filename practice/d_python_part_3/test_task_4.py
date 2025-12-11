"""
Write test for print_name_address function
Use Mock for mocking args argument https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock
Example:
    >>> m = Mock()
    >>> m.method.return_value = 123
    >>> m.method()
    123
"""
import pytest
import json
from unittest.mock import Mock, patch
from io import StringIO
import argparse
from task_4 import print_name_address, generate_data


def create_mock_faker(data_sequence):
    mock_fake = Mock()

    for provider in ['name', 'address']:
        setattr(mock_fake, provider, Mock())

    return data_sequence


class MockNamespace(argparse.Namespace):
    def __init__(self, number, providers):
        self.number = number
        self.providers = providers
        super().__init__()


@patch('task_4.generate_data')
@patch('sys.stdout', new_callable=StringIO)
def test_print_name_address_success(mock_stdout, mock_generate_data):
    """
    Tests successful execution and output format.
    """
    mock_data = [
        {"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green"},
        {"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard"}
    ]
    mock_generate_data.return_value = mock_data

    args = MockNamespace(
        number=2,
        providers={'some_name': 'name', 'fake-address': 'address'}
    )

    print_name_address(args)

    expected_output = (
        '{"some_name":"Chad Baird","fake-address":"62323 Hobbs Green"}\n'
        '{"some_name":"Courtney Duncan","fake-address":"8107 Nicole Orchard"}\n'
    )

    actual_lines = mock_stdout.getvalue().strip().split('\n')

    assert len(actual_lines) == 2

    expected_dicts = [
        {"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green"},
        {"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard"}
    ]

    actual_dicts = [json.loads(line) for line in actual_lines]

    assert actual_dicts == expected_dicts

    mock_generate_data.assert_called_once_with(
        2,
        {'some_name': 'name', 'fake-address': 'address'}
    )


@patch('task_4.generate_data')
@patch('sys.stdout', new_callable=StringIO)
def test_print_name_address_single_item_single_field(mock_stdout, mock_generate_data):
    """
    Tests successful execution for a single item with a single field.
    """
    mock_data = [{"id": 100}]
    mock_generate_data.return_value = mock_data

    args = MockNamespace(
        number=1,
        providers={'id': 'pyint'}
    )

    print_name_address(args)

    actual_output = mock_stdout.getvalue().strip()
    expected_output = '{"id":100}'

    assert actual_output == expected_output


def test_print_name_address_no_providers_raises_value_error():
    """
    Tests that a ValueError is raised if the provider map is empty.
    """
    args = MockNamespace(
        number=5,
        providers={}
    )
    with pytest.raises(ValueError) as excinfo:
        print_name_address(args)

    assert "Must provide at least one field/provider argument" in str(excinfo.value)


def test_generate_data_calls_faker_correctly():
    """
    Tests that generate_data correctly maps field names to Faker provider methods.
    """
    mock_fake = Mock()
    mock_fake.name.return_value = "Test Name"
    mock_fake.address.return_value = "Test Address"

    with patch('task_4.Faker', return_value=mock_fake):
        result = generate_data(1, {'n': 'name', 'a': 'address'})

    mock_fake.name.assert_called_once()
    mock_fake.address.assert_called_once()

    assert result == [{'n': 'Test Name', 'a': 'Test Address'}]


def test_generate_data_invalid_provider_raises_value_error():
    """
    Tests that generate_data raises a ValueError if a provider name is invalid.
    """
    provider_map = {'name': 'invalid_provider_name'}

    with pytest.raises(ValueError) as excinfo:
        generate_data(1, provider_map)

    assert "Faker provider 'invalid_provider_name' for field 'name' not found." in str(excinfo.value)
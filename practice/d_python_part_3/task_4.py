"""
Create virtual environment and install Faker package only for this venv.
Write command line tool which will receive int as a first argument and one or more named arguments
 and generates defined number of dicts separated by new line.
Exec format:
`$python task_4.py NUMBER --FIELD=PROVIDER [--FIELD=PROVIDER...]`
where:
NUMBER - positive number of generated instances
FIELD - key used in generated dict
PROVIDER - name of Faker provider
Example:
`$python task_4.py 2 --fake-address=address --some_name=name`
{"some_name": "Chad Baird", "fake-address": "62323 Hobbs Green\nMaryshire, WY 48636"}
{"some_name": "Courtney Duncan", "fake-address": "8107 Nicole Orchard Suite 762\nJosephchester, WI 05981"}
"""

import argparse
import json
import sys
from typing import Dict, Any, List

try:
    from faker import Faker
except ImportError:
    print("Error: Faker package is not installed. Please run 'pip install Faker' in your virtual environment.")
    sys.exit(1)


def generate_data(count: int, provider_map: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Generates a list of dictionaries using Faker providers.

    :param count: The number of dictionaries to generate.
    :param provider_map: A mapping of dictionary keys (fields) to Faker provider names.
    :return: A list of generated dictionaries.
    """
    fake = Faker()
    results = []

    for field, provider in provider_map.items():
        if not hasattr(fake, provider):
            raise ValueError(f"Faker provider '{provider}' for field '{field}' not found.")

    for _ in range(count):
        instance = {}
        for field, provider in provider_map.items():
            provider_method = getattr(fake, provider)
            instance[field] = provider_method()
        results.append(instance)

    return results


def print_name_address(args: argparse.Namespace) -> None:
    """
    Parses command line arguments and prints generated JSON data.
    """
    count = args.number
    provider_map = args.providers

    if not provider_map:
        raise ValueError("Must provide at least one field/provider argument (e.g., --name=name).")

    generated_list = generate_data(count, provider_map)

    for item in generated_list:
        print(json.dumps(item, separators=(',', ':')))


def main():
    parser = argparse.ArgumentParser(
        description="Generates JSON dictionaries using Faker providers.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "number",
        type=int,
        help="Positive number of generated instances.",
    )

    class FieldProviderAction(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not values:
                return

            if 'providers' not in namespace:
                setattr(namespace, 'providers', {})

            field_name = option_string.lstrip('-')
            provider_name = values

            namespace.providers[field_name] = provider_name

    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)

    try:
        count = int(sys.argv[1])
        if count <= 0:
            raise ValueError("NUMBER must be a positive integer.")
    except ValueError as e:
        print(f"Error: Invalid NUMBER argument. {e}")
        sys.exit(1)

    provider_map = {}

    for arg in sys.argv[2:]:
        if not arg.startswith('--'):
            print(f"Error: Field arguments must start with '--'. Found '{arg}'.")
            sys.exit(1)

        clean_arg = arg[2:]
        if '=' not in clean_arg:
            print(f"Error: Field argument '{arg}' must be in the format --FIELD=PROVIDER.")
            sys.exit(1)

        field, provider = clean_arg.split('=', 1)
        if not field or not provider:
            print(f"Error: Field or Provider name missing in '{arg}'.")
            sys.exit(1)

        provider_map[field] = provider

    class MockNamespace:
        def __init__(self, number, providers):
            self.number = number
            self.providers = providers

    args = MockNamespace(number=count, providers=provider_map)

    try:
        print_name_address(args)
    except (ValueError, TypeError) as e:
        print(f"Execution Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
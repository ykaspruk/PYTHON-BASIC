import os
import json
import statistics
import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Optional
from collections import namedtuple

BASE_DATA_PATH = os.path.join('source_data')
DATE_OBSERVATION = '2021_09_25'
COUNTRY_NAME = 'Spain'
JSON_FILENAME = f'{DATE_OBSERVATION}.json'
OUTPUT_FILENAME = 'result.xml'

CityStats = namedtuple(
    'CityStats',
    ['city', 'mean_temp', 'max_temp', 'min_temp',
     'mean_wind_speed', 'max_wind_speed', 'min_wind_speed']
)


def round_float(value: float) -> str:
    """Rounds a float to two decimal places and returns it as a string."""
    return f"{value:.2f}"


def calculate_city_stats(city_data: List[Dict[str, Any]], city_name: str) -> Optional[CityStats]:
    """
    Calculates mean, min, and max temperature and wind speed for a single city.
    """
    try:
        temps = [hour['temp'] for hour in city_data]
        wind_speeds = [hour['wind_speed'] for hour in city_data]
    except KeyError as e:
        print(f"Error: Missing field {e} in data for {city_name}")
        return None
    except TypeError:
        print(f"Error: Data structure is incorrect for {city_name}.")
        return None

    if not temps or not wind_speeds:
        print(f"Warning: No valid hourly data for {city_name}.")
        return None

    mean_t = statistics.mean(temps)
    max_t = max(temps)
    min_t = min(temps)

    mean_ws = statistics.mean(wind_speeds)
    max_ws = max(wind_speeds)
    min_ws = min(wind_speeds)

    return CityStats(
        city=city_name,
        mean_temp=mean_t,
        max_temp=max_t,
        min_temp=min_t,
        mean_wind_speed=mean_ws,
        max_wind_speed=max_ws,
        min_wind_speed=min_ws
    )


def process_all_cities(base_dir: str) -> List[CityStats]:
    """
    Walks through the directory, parses JSON files, and calculates stats for all cities.
    """
    all_city_stats = []

    if not os.path.isdir(base_dir):
        print(f"Error: Base data directory not found at {base_dir}")
        return []

    for city_name in os.listdir(base_dir):
        city_path = os.path.join(base_dir, city_name)

        if not os.path.isdir(city_path):
            continue

        file_path = os.path.join(city_path, JSON_FILENAME)

        if not os.path.exists(file_path):
            print(f"Warning: File not found for {city_name} at {file_path}")
            continue

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            hourly_data = data.get('hourly', [])

            stats = calculate_city_stats(hourly_data, city_name)

            if stats:
                all_city_stats.append(stats)

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in {file_path}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred processing {city_name}: {e}")

    return all_city_stats


def calculate_country_summary(all_stats: List[CityStats]) -> Dict[str, Any]:
    """
    Calculates country-wide mean stats and finds the extreme cities.
    """
    if not all_stats:
        return {}

    all_mean_temps = [s.mean_temp for s in all_stats]
    all_mean_winds = [s.mean_wind_speed for s in all_stats]

    country_mean_temp = statistics.mean(all_mean_temps)
    country_mean_wind_speed = statistics.mean(all_mean_winds)

    warmest = max(all_stats, key=lambda s: s.mean_temp)
    coldest = min(all_stats, key=lambda s: s.mean_temp)
    windiest = max(all_stats, key=lambda s: s.mean_wind_speed)

    return {
        'mean_temp': country_mean_temp,
        'mean_wind_speed': country_mean_wind_speed,
        'coldest_place': coldest.city,
        'warmest_place': warmest.city,
        'windiest_place': windiest.city
    }


def create_xml_report(city_stats: List[CityStats], country_summary: Dict[str, Any], output_filename: str):
    """
    Builds the final XML report file.
    """
    weather = ET.Element('weather')
    weather.set('country', COUNTRY_NAME)
    weather.set('date', DATE_OBSERVATION)

    summary = ET.SubElement(weather, 'summary')
    summary.set('mean_temp', round_float(country_summary['mean_temp']))
    summary.set('mean_wind_speed', round_float(country_summary['mean_wind_speed']))
    summary.set('coldest_place', country_summary['coldest_place'])
    summary.set('warmest_place', country_summary['warmest_place'])
    summary.set('windiest_place', country_summary['windiest_place'])

    cities = ET.SubElement(weather, 'cities')

    for stats in city_stats:
        sanitized_city_name = stats.city.replace(' ', '_').replace('-', '_')

        city_element = ET.SubElement(cities, sanitized_city_name)
        city_element.set('mean_temp', round_float(stats.mean_temp))
        city_element.set('max_temp', round_float(stats.max_temp))
        city_element.set('min_temp', round_float(stats.min_temp))
        city_element.set('mean_wind_speed', round_float(stats.mean_wind_speed))
        city_element.set('max_wind_speed', round_float(stats.max_wind_speed))
        city_element.set('min_wind_speed', round_float(stats.min_wind_speed))

    tree = ET.ElementTree(weather)

    try:
        ET.indent(tree, space="  ", level=0)
    except AttributeError:
        pass

    # weather.set('date', DATE_OBSERVATION.replace('_', '-'))

    tree.write(output_filename, encoding='utf-8', xml_declaration=True)

    print(f"\nSuccessfully generated XML report: {output_filename}")


if __name__ == "__main__":
    print(f"Starting weather data processing from: {BASE_DATA_PATH}")
    city_statistics = process_all_cities(BASE_DATA_PATH)

    if not city_statistics:
        print("No valid city data processed. Cannot generate report.")
    else:
        country_summary_data = calculate_country_summary(city_statistics)

        create_xml_report(city_statistics, country_summary_data, OUTPUT_FILENAME)
import os
import requests
from concurrent.futures import ThreadPoolExecutor

API_KEY = "Ax6Om0A8ZxoftZNS943Ih2niOt4TT4MkBJsMqdjI"
APOD_ENDPOINT = 'https://api.nasa.gov/planetary/apod'
OUTPUT_DIR = './output'


def get_apod_metadata(start_date: str, end_date: str, api_key: str) -> list:
    """Fetches metadata for a range of dates from the NASA APOD API."""
    params = {
        'api_key': api_key,
        'start_date': start_date,
        'end_date': end_date
    }
    try:
        response = requests.get(APOD_ENDPOINT, params=params)
        response.raise_for_status()  # Raise error for bad status
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching metadata: {e}")
        return []

def download_single_image(item: dict):
    """Helper function to download one image from its metadata."""
    if item.get('media_type') == 'image':
        url = item.get('hdurl') or item.get('url')
        date = item.get('date')

        # Determine file extension from URL
        ext = os.path.splitext(url)[1]
        if not ext:
            ext = ".jpg"

        file_path = os.path.join(OUTPUT_DIR, f"{date}{ext}")

        try:
            img_data = requests.get(url).content
            with open(file_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded: {date}")
        except Exception as e:
            print(f"Failed to download {date}: {e}")

def download_apod_images(metadata: list):
    """Uses a ThreadPool to download images concurrently."""
    if not metadata:
        print("No metadata found.")
        return

    print(f"Starting download of {len(metadata)} potential images...")

    # Using 10 threads
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(download_single_image, metadata)

    print("All downloads complete.")


def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    metadata = get_apod_metadata(
        start_date='2021-08-01',
        end_date='2021-09-30',
        api_key=API_KEY,
    )

    download_apod_images(metadata=metadata)

if __name__ == '__main__':
    main()
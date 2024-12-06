
import requests
import time
import pandas as pd

def fetch_phishing_data_from_api(api_url, api_key=None):
    """Fetch phishing data from an external API."""
    headers = {'Authorization': f'Bearer {api_key}'} if api_key else {}
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to fetch data from {api_url}: {response.status_code}")

def simulate_real_time_streaming(data, delay=1):
    """Simulate real-time data streaming."""
    for record in data:
        time.sleep(delay)
        yield record

def collect_data_sources(file_path=None, api_url=None, api_key=None):
    """Combine data collection from file and API."""
    data = []
    if file_path:
        data += pd.read_csv(file_path).to_dict(orient='records')
    if api_url:
        data += fetch_phishing_data_from_api(api_url, api_key)
    return data

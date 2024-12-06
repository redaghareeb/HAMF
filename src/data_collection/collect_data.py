
import requests

def collect_data(source, params=None):
    """
    Collects data from specified sources.
    
    :param source: URL or path of the data source
    :param params: Optional parameters for API requests
    :return: Collected data in JSON format
    """
    if source.startswith("http"):
        response = requests.get(source, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to collect data from {source}")
    else:
        raise ValueError("Unsupported data source type")

import requests

def collect_from_web(url):
    response = requests.get(url)
    return response.json()

def collect_from_csv(file_path):
    import pandas as pd
    return pd.read_csv(file_path)

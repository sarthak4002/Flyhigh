import requests
import pandas as pd

# Define your API key here
API_KEY = '62ede90eab3a6b49f8f20fb9bfda9612'  # Replace with your actual API key
BASE_URL = 'http://api.aviationstack.com/v1/'  # AviationStack Base URL

def load_data():
    data = pd.read_csv('path_to_your_csv_file.csv')
    return data

def fetch_data(endpoint, params={}):
    params['62ede90eab3a6b49f8f20fb9bfda9612'] = API_KEY  # Add API key to the params
    url = BASE_URL + endpoint  # Construct the full API URL
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")

# Fetch and save data from all endpoints
def main():
    endpoints = [
        'flights',
        'airports',
        'airlines',
        'historical',
        'aircraft-types',
        'airplanes',
        'aviation-taxes',
        'cities',
        'countries',
        'autocomplete',
        'flight-schedules',
        'future-flights'
    ]
    
    for endpoint in endpoints:
        print(f"Fetching data from {endpoint}...")
        data = fetch_data(endpoint)
        if data:
            save_to_csv(data['data'], 'flight_data.csv')  # Save data to CSV
        else:
            print(f"Error fetching data from {endpoint}.")

if __name__ == '__main__':
    main()


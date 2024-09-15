from flask import Flask, render_template, request
import requests
import pandas as pd

app = Flask(__name__)

# Define your API key and base URL
API_KEY = '62ede90eab3a6b49f8f20fb9bfda9612'
BASE_URL = 'http://api.aviationstack.com/v1/'

def fetch_data(endpoint, params={}):
    """Fetch data from the AviationStack API."""
    params['access_key'] = API_KEY
    url = BASE_URL + endpoint
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    return None

def clean_flight_data(flight):
    """Function to clean and format flight data."""
    return {
        'flight_date': flight['flight_date'],
        'flight_status': flight.get('flight_status', 'N/A'),
        'departure_airport': flight['departure']['airport'],
        'departure_time': flight['departure'].get('scheduled', 'N/A'),
        'arrival_airport': flight['arrival']['airport'],
        'arrival_time': flight['arrival'].get('scheduled', 'N/A'),
        'airline_name': flight['airline']['name'],
        'flight_number': flight['flight']['iata'],
        'departure_delay': flight['departure'].get('delay', 'N/A'),
        'arrival_delay': flight['arrival'].get('delay', 'N/A'),
        'departure_terminal': flight['departure'].get('terminal', 'N/A'),
        'arrival_terminal': flight['arrival'].get('terminal', 'N/A'),
        'departure_gate': flight['departure'].get('gate', 'N/A'),
        'arrival_gate': flight['arrival'].get('gate', 'N/A'),
        'baggage': flight['arrival'].get('baggage', 'N/A'),
        'aircraft': flight['aircraft'],
        'live_info': flight['live']
    }

@app.route('/')
def home():
    # Get filter parameters from request arguments
    search_query = request.args.get('search', '')
    flight_status_filter = request.args.get('flight_status', '')
    departure_airport_filter = request.args.get('departure_airport', '')
    arrival_airport_filter = request.args.get('arrival_airport', '')
    page = int(request.args.get('page', 1))
    
    # Define the number of results per page
    results_per_page = 10

    # Fetch flight data
    flights_data = fetch_data('flights')
    
    if flights_data:
        cleaned_data = [clean_flight_data(flight) for flight in flights_data['data']]
        
        # Apply filters
        if search_query:
            cleaned_data = [flight for flight in cleaned_data if search_query.lower() in flight['flight_number'].lower()]
        if flight_status_filter:
            cleaned_data = [flight for flight in cleaned_data if flight_status_filter.lower() in flight['flight_status'].lower()]
        if departure_airport_filter:
            cleaned_data = [flight for flight in cleaned_data if departure_airport_filter.lower() in flight['departure_airport'].lower()]
        if arrival_airport_filter:
            cleaned_data = [flight for flight in cleaned_data if arrival_airport_filter.lower() in flight['arrival_airport'].lower()]

        # Pagination
        total_results = len(cleaned_data)
        total_pages = (total_results + results_per_page - 1) // results_per_page
        start_index = (page - 1) * results_per_page
        end_index = min(start_index + results_per_page, total_results)
        
        return render_template('index.html', 
                               data=cleaned_data[start_index:end_index],
                               columns=['flight_date', 'flight_status', 'departure_airport', 'departure_time', 'arrival_airport', 'arrival_time', 'airline_name', 'flight_number'],
                               page=page,
                               total_pages=total_pages,
                               search_query=search_query,
                               flight_status_filter=flight_status_filter,
                               departure_airport_filter=departure_airport_filter,
                               arrival_airport_filter=arrival_airport_filter)
    else:
        return "Error fetching data."

@app.route('/airports')
def airports():
    airports_data = fetch_data('airports')
    if airports_data:
        cleaned_data = [airport for airport in airports_data['data']]
        return render_template('index.html', data=cleaned_data, columns=['airport_name', 'city', 'country', 'iata', 'icao'])
    else:
        return "Error fetching airports data."

@app.route('/airlines')
def airlines():
    airlines_data = fetch_data('airlines')
    if airlines_data:
        cleaned_data = [airline for airline in airlines_data['data']]
        return render_template('index.html', data=cleaned_data, columns=['name', 'iata', 'icao'])
    else:
        return "Error fetching airlines data."

if __name__ == '__main__':
    app.run(debug=True)

from model.country import Country
from model.airport import Airport
import json
import csv
from curl_cffi import requests
from datetime import datetime
from datetime import timedelta
from itertools import product
from model.cache import Cache


class AppState:
    _instance = None
    
    # the key for dictionaries is the couple (country_name, country_code)
    # the value for dictionaries is the tuple defined by country or airport

    countries = {}                      # all the coutries (always in memory)
    airports = {}                       # all the airports (always in memory)
    routes = {}
    selectable_departure_countries = {}           # countries to show for selection filtered by text searched
    selectable_departure_airports = {}            # airports to show for selection filtered by country and text searched
    selectable_arrival_countries = {}
    selectable_arrival_airports = {}
    selected_departure_airports = {}              # the airports the user has selected for departure (for now only IATA)
    selected_arrival_airports= {}
    selected_dates = []
    valid_date_couples = []
    selected_nights_min = 2
    selected_nights_max = 4
    selected_passengers = 1
    found_flights = []
    language = "Italiano"
    credits_key = ""
    valid_keys = []
    
    def __new__(cls):
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.airports = {}
                cls._instance.read_valid_keys() 
                cls._instance.read_countries()
                cls._instance.read_airports()
                cls._instance.read_all_routes()
            return cls._instance

    # get the couple country code and name given the country code only 
    def get_country_full_key(self, code):
        codes_map = {full_key[0]: full_key for full_key in self.countries.keys()}
        return codes_map.get(code)

    def read_valid_keys(self):
        f_keys = open("files/valid_keys.txt")
        self.valid_keys = [line.strip() for line in f_keys.readlines()]
        f_keys.close()

    # read all the countries
    def read_countries(self):
        f_countries = open("files/countries.csv", "r", encoding="utf-8-sig")
        reader = csv.reader(f_countries, delimiter=',', quotechar='"', skipinitialspace=True, lineterminator='\n')
        next(reader)
        for r_country in reader:
            code = r_country[1].strip()
            name = r_country[2].strip()
            countries = Country(code, name)
            self.countries[countries.code] = countries.name
        f_countries.close()
                
        self.countries = {
            k: v for k, v in sorted(self.countries.items(), key=lambda item: item[1])
        }
        self.filter_departure_countries("")
        
    # read all the airports and put them in a dictionary
    def read_airports(self):
        f_airports = open("files/airports.csv", "r", encoding="utf-8-sig")
        reader = csv.reader(f_airports, delimiter=',', quotechar='"', skipinitialspace=True)
        next(reader)
        for r_airport in reader:
            airport_type = r_airport[2].strip()
            name = r_airport[3].strip()
            country = r_airport[8].strip()
            city = r_airport[10].strip()
            scheduled_service = r_airport[11].strip()
            iata = r_airport[13].strip()
            if iata != '' and scheduled_service=='yes' and airport_type in ['medium_airport', 'large_airport']:
                airport = Airport(name, country, city, iata)
                country_key = (country, self.countries[country])
                if not country_key in self.airports:
                    self.airports[country_key] = [(airport.name, airport.country, airport.city, airport.iata)]    
                else:
                    self.airports[country_key].append((airport.name, airport.country, airport.city, airport.iata))

        f_airports.close()

        self.filter_departure_countries("")
        self.filter_departure_airports("")

    def filter_departure_countries(self, searched_text):
            self.selectable_departure_countries = {
                key: value
                for key, value in self.countries.items()
                if searched_text.lower() in value.lower()
            }

    def filter_departure_airports(self, searched_text):
        self.selectable_departure_airports.clear()
        for country in self.selectable_departure_countries.items():
            if country in self.airports.keys():
                if country in self.selectable_departure_airports.keys():
                    self.selectable_departure_airports[country].extend(self.airports[country])
                else:
                    self.selectable_departure_airports[country] = self.airports[country]

        misc_airports = {}

        for key, tuple_list in self.airports.items():
            matching_tuples = [
                tup for tup in tuple_list 
                if searched_text.lower() in tup[2].lower() 
                or searched_text.lower() in tup[3].lower()
                or searched_text.lower() in tup[0].lower()
            ]
            if matching_tuples:
                misc_airports[key] = matching_tuples
                        
        self.selectable_departure_airports |= misc_airports

    # update selectable countries and airports based on requested text
    def filter_selectable_departures(self, text):
        self.filter_departure_countries(text)
        self.filter_departure_airports(text)

    # add tapped airport to selection
    def add_departure_airport(self, airport):
        iata = airport[-4:-1]
        
        if not iata in self.selected_departure_airports.keys():
            name = airport.split(" - ")[0].strip()
            city = airport.split(" - ")[1].strip()
            country = airport.split(" - ")[2][:2]
            self.selected_departure_airports[iata] = (city, country, name)

    def remove_departure_airport(self, airport):
        iata = airport[-4:-1]
        if iata in self.selected_departure_airports.keys():
            self.selected_departure_airports.pop(iata)

    def add_arrival_airport(self, airport):
        iata = airport[-4:-1]
                
        if not iata in self.selected_departure_airports.keys():
            name = airport.split(" - ")[0].strip()
            city = airport.split(" - ")[1].strip()
            country = airport.split(" - ")[2][:2]
            self.selected_arrival_airports[iata] = (city, country, name)

    def remove_arrival_airport(self, airport):
        iata = airport[-4:-1]
        if iata in self.selected_arrival_airports.keys():
            self.selected_arrival_airports.pop(iata)

    def read_all_routes(self):
        # da aggiornare su https://github.com/Jonty/airline-route-data/blob/main/airline_routes.json
        json_routes = open("files/airline_routes.json", "r")
        self.routes = json.load(json_routes)

    def filter_selectable_arrivals(self, text):
        if self.selected_departure_airports == []:
            return []

        # iata_list contiene tutti gli aeroporti di arrivo possibili data una partenza
        iata_list = []
        for iata in self.selected_departure_airports.keys():
            iata_list =  list(set(iata_list + [item["iata"] for item in self.routes[iata]["routes"]]))
        iata_list.sort()

        search = text.lower()
        self.selectable_arrival_airports = {
            country: [
                a
                for a in airports
                if a[3] in iata_list
                and (
                    search in country[1].lower()  # Nome Paese (country è la tupla (cod, nome))
                    or search in a[0].lower()  # Nome Aeroporto (a[0])
                    or search in a[2].lower()  # Città (a[2])
                    or search in a[3].lower()  # Codice IATA (a[3])
                )
            ]
            for country, airports in self.airports.items()
            if any(
                a[3] in iata_list
                and (
                    search in country[1].lower()
                    or search in a[0].lower()
                    or search in a[2].lower()
                    or search in a[3].lower()
                )
                for a in airports
            )
        }

        self.selectable_arrival_countries = self.selectable_arrival_airports.keys()
        

    def add_selected_dates(self, start_date, end_date):
        self.selected_dates.append((start_date, end_date))
        self.compute_valid_dates()

    def remove_selected_dates(self, start_date, end_date):
        if (start_date, end_date) in self.selected_dates:
            self.selected_dates.remove((start_date, end_date))
            self.compute_valid_dates()

    def find_flights_serpapi(self, state):
        TOKEN = "6496ab33fa84f7ee7d06d53753606c16ebbf1117816682786b0853144737102e"
        url = "https://serpapi.com/search.json"
        flights = []
        outbound_flights = []
        inbound_flights = []
        outbound_dates = set(el[0] for el in state.valid_date_couples)
        inbound_dates = set(el[1] for el in state.valid_date_couples)

        for outbound_date in outbound_dates:
            params = {
                "api_key": TOKEN,
                "engine": "google_flights",
                "departure_id": ",".join(state.selected_departure_airports.keys()),
                "arrival_id": ",".join(state.selected_arrival_airports.keys()),
                "outbound_date": outbound_date.strftime("%Y-%m-%d"),
                "currency": "EUR",
                "hl": "en",
                "gl": "it",
                "type": 2,
                "sort_by": 2
            }
            response = requests.request("GET", url, params=params)
            outbound_results = response.json()

            if "best_flights" in outbound_results:
                for best_outbound_flight in outbound_results["best_flights"]:
                    no_flights = len(best_outbound_flight["flights"])
                    outbound_flight = {
                        "origin": best_outbound_flight["flights"][0]["departure_airport"]["id"],
                        "origin_name": best_outbound_flight["flights"][0]["departure_airport"]["name"],
                        "departure_at": best_outbound_flight["flights"][0]["departure_airport"]["time"],
                        "destination": best_outbound_flight["flights"][no_flights-1]["arrival_airport"]["id"],
                        "destination_name": best_outbound_flight["flights"][no_flights-1]["arrival_airport"]["name"],
                        "arrival_at": best_outbound_flight["flights"][no_flights-1]["arrival_airport"]["time"],
                        "price": best_outbound_flight["price"],
                        "airline_logo": best_outbound_flight["flights"][no_flights-1]["airline_logo"]
                    }
                    outbound_flights.append(outbound_flight)

            if "other_flights" in outbound_results:
                for other_outbound_flight in outbound_results["other_flights"]:
                    no_flights = len(other_outbound_flight["flights"])
                    outbound_flight = {
                        "origin": other_outbound_flight["flights"][0]["departure_airport"]["id"],
                        "origin_name": other_outbound_flight["flights"][0]["departure_airport"]["name"],
                        "departure_at": other_outbound_flight["flights"][0]["departure_airport"]["time"],
                        "destination": other_outbound_flight["flights"][no_flights-1]["arrival_airport"]["id"],
                        "destination_name": other_outbound_flight["flights"][no_flights-1]["arrival_airport"]["name"],
                        "arrival_at": other_outbound_flight["flights"][no_flights-1]["arrival_airport"]["time"],
                        "price": other_outbound_flight["price"],
                        "airline_logo": other_outbound_flight["flights"][no_flights-1]["airline_logo"]
                    }
                    outbound_flights.append(outbound_flight)

        for inbound_date in inbound_dates:
            params = {
                "api_key": TOKEN,
                "engine": "google_flights",
                "departure_id": ",".join(state.selected_arrival_airports.keys()),
                "arrival_id": ",".join(state.selected_departure_airports.keys()),
                "outbound_date": inbound_date.strftime("%Y-%m-%d"),
                "currency": "EUR",
                "hl": "en",
                "gl": "it",
                "type": 2,
                "sort_by": 2
            }
            response = requests.request("GET", url, params=params)

            inbound_results = response.json()

            if "best_flights" in inbound_results:
                for best_inbound_flight in inbound_results["best_flights"]:
                    no_flights = len(best_inbound_flight["flights"])
                    inbound_flight = {
                        "origin": best_inbound_flight["flights"][0]["departure_airport"]["id"],
                        "origin_name": best_inbound_flight["flights"][0]["departure_airport"]["name"],
                        "departure_at": best_inbound_flight["flights"][0]["departure_airport"]["time"],
                        "destination": best_inbound_flight["flights"][no_flights-1]["arrival_airport"]["id"],
                        "destination_name": best_inbound_flight["flights"][no_flights-1]["arrival_airport"]["name"],
                        "arrival_at": best_inbound_flight["flights"][no_flights-1]["arrival_airport"]["time"],
                        "price": best_inbound_flight["price"],
                        "airline_logo": best_inbound_flight["flights"][no_flights-1]["airline_logo"]
                    }
                    inbound_flights.append(inbound_flight)

            if "other_flights" in inbound_results:
                for other_inbound_flight in inbound_results["other_flights"]:
                    no_flights = len(other_inbound_flight["flights"])
                    inbound_flight = {
                        "origin": other_inbound_flight["flights"][0]["departure_airport"]["id"],
                        "origin_name": other_inbound_flight["flights"][0]["departure_airport"]["name"],
                        "departure_at": other_inbound_flight["flights"][0]["departure_airport"]["time"],
                        "destination": other_inbound_flight["flights"][no_flights-1]["arrival_airport"]["id"],
                        "destination_name": other_inbound_flight["flights"][no_flights-1]["arrival_airport"]["name"],
                        "arrival_at": other_inbound_flight["flights"][no_flights-1]["arrival_airport"]["time"],
                        "price": other_inbound_flight["price"],
                        "airline_logo": other_inbound_flight["flights"][no_flights-1]["airline_logo"]
                    }
                    inbound_flights.append(inbound_flight)

        cache = Cache()
        cache.save_results(outbound_flights, inbound_flights)

        flights = list(product(outbound_flights, inbound_flights))

        valid_flights = []

        for outbound_flight, inbound_flight in flights:
            if outbound_flight["destination"] != inbound_flight["origin"]:
                continue

            outbound_date = datetime.strptime(outbound_flight["departure_at"], "%Y-%m-%d %H:%M").date()
            inbound_date = datetime.strptime(inbound_flight["arrival_at"], "%Y-%m-%d %H:%M").date()

            if (outbound_date, inbound_date) in state.valid_date_couples:
                valid_flights.append((outbound_flight, inbound_flight))

        return valid_flights

    def compute_valid_dates(self):
        self.valid_date_couples = []
        for selected_date in self.selected_dates:
            for k in range(0, self.selected_nights_max):
                for n in range(self.selected_nights_min, self.selected_nights_max + 1):
                    if selected_date[0] + timedelta(days=n+k) <= selected_date[1]:
                        self.valid_date_couples.append((selected_date[0] + timedelta(days=k), selected_date[0] + timedelta(days=n+k)))


    



    
        

    
    
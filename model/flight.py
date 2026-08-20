class Flight:
    def __init__(self, 
                 departure_out_airport, departure_out_date, arrival_out_airport, arrival_out_date, 
                 departure_in_airport, departure_in_date, arrival_in_airport, arrival_in_date,
                 price):
        super().__init__()
        self.departure_out_airport = departure_out_airport 
        self.departure_out_date = departure_out_date
        self.arrival_out_airport = arrival_out_airport
        self.arrival_out_date = arrival_out_date
        self.departure_in_airport = departure_in_airport
        self.departure_in_date = departure_in_date
        self.arrival_in_airport = arrival_in_airport
        self.arrival_in_date = arrival_in_date
        self.price = price
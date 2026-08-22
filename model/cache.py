from datetime import datetime
import json

class Cache:
    def __init__(self):
        super().__init__()

    def save_research(self, state):
        f_cache = open("files/cache.csv", "a", encoding="utf-8")
        f_cache.write(datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + ";" + state.credits_key + ";" + str(len(state.valid_date_couples) * 2))
        f_cache.close()

    def save_results(self, outbound_flights, inbound_flights):
        f_cache = open("files/results.json", "a", encoding="utf-8")

        for outbound_flight in outbound_flights:
            outbound_flight["last_update"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            json.dump(outbound_flight, f_cache, ensure_ascii=False, indent=4)
            f_cache.write(",\n")

        for inbound_flight in inbound_flights:
            inbound_flight["last_update"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            json.dump(outbound_flight, f_cache, ensure_ascii=False, indent=4)
            f_cache.write(",\n")

        f_cache.close()
            
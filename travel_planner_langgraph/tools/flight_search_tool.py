from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from datetime import date
from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

class FlightInput(BaseModel):
    origin: str = Field(description="Airport code of the origin city or nearby city. An airport code is an uppercase 3-letter code")
    destination: str = Field(description="Airport code of the destination city or nearby city. An airport code is an uppercase 3-letter code")
    departure_date: date = Field(description="Departure date")
    return_date: date = Field(description="Return date")

class FlightSearchTool(BaseTool):
    name: str = "flight_search"
    description: str = "Search for flight information between two cities for given dates"
    args_schema: type[FlightInput] = FlightInput

    def _search_flights(self, origin: str, destination: str, date: date):
        params = {
            "engine": "google_flights",
            "departure_id": origin,
            "arrival_id": destination,
            "outbound_date": date.strftime("%Y-%m-%d"),
            "api_key": os.getenv("SERPAPI_API_KEY"),
            "type": 2,
            "currency" : "INR"
        }
        # print("params:", params)
        search = GoogleSearch(params)
        response = search.get_dict()
        # print("response:", response)
        return response["best_flights"]

    def _run(self, origin: str, destination: str, departure_date: date, return_date: date):
        outbound_results = self._search_flights(origin, destination, departure_date)
        inbound_results = self._search_flights(destination, origin, return_date)
        return {
            "outbound_flight": outbound_results,
            "return_flight": inbound_results
        }

    def _arun(self, origin: str, destination: str, departure_date: date, return_date: date):
        raise NotImplementedError("Async implementation not available")

from typing import Optional, List
from langchain.tools import BaseTool
import requests
from pydantic import BaseModel, Field
from datetime import date, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

class WeatherInput(BaseModel):
    city: str = Field(description="The name of the city to get weather forecast for")
    start_date: date = Field(description="Start date for historical weather data")
    end_date: date = Field(description="End date for historical weather data") 

class Temperature(BaseModel):
    min: float
    max: float
    unit: str = "°C"

class Conditions(BaseModel):
    day: str
    night: str

class DailyWeather(BaseModel):
    date: date
    temperature: Temperature
    conditions: Conditions

class WeatherHistory(BaseModel):
    historical_weather: List[DailyWeather]

class WeatherTool(BaseTool):
    name: str = "historical_weather"
    description: str = "Get historical weather data for a given city and date range from last year using AccuWeather API"
    args_schema: type[WeatherInput] = WeatherInput

    def _get_location_key(self, city: str, api_key: str) -> Optional[str]:
        """Get AccuWeather location key for the given city."""
        url = "http://dataservice.accuweather.com/locations/v1/cities/search"
        params = {
            "apikey": api_key,
            "q": city
        }
        
        response = requests.get(url, params=params)
        # print("Response: ", response.status_code)
        if response.status_code == 200:
            locations = response.json()
            if locations:
                return locations[0]["Key"]
        return None

    def _get_historical_weather(self, location_key: str, target_date: date, api_key: str) -> Optional[DailyWeather]:
        
        """Get historical weather for a specific date."""
        url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}/historical/24"
        params = {
            "apikey": api_key,
            "date": target_date.strftime("%Y-%m-%d")
        }
        
        response = requests.get(url, params=params)
        # print("response:", response.status_code)
        if response.status_code == 200:
            data = response.json()
            if data:
                
                min_temp = float('inf')
                max_temp = float('-inf')
                
                for hourly_data in data:
                    temp_celsius = hourly_data["Temperature"]["Metric"]["Value"]
                    if temp_celsius < min_temp:
                        min_temp = temp_celsius
                    if temp_celsius > max_temp:
                        max_temp = temp_celsius
                
                return DailyWeather(
                    date=target_date,
                    temperature=Temperature(
                        min=min_temp,
                        max=max_temp
                    ),
                    conditions=Conditions(
                        day=data[0]["WeatherText"],
                        night=data[0]["WeatherText"]
                    )
                )
        return None

    def _run(self, city: str, start_date: date, end_date: date) -> WeatherHistory:
        print("Calling weather api.....")
        """Run the historical weather tool."""
        
        # Get API key from environment variable
        api_key = os.getenv("ACCUWEATHER_API_KEY")
        if not api_key:
            raise ValueError("ACCUWEATHER_API_KEY environment variable not set")
        
        # Get location key for the city
        location_key = self._get_location_key(city, api_key)
        if not location_key:
            raise ValueError(f"Could not find location key for city: {city}")

        # Calculate last year's dates
        last_year_start = start_date.replace(year=start_date.year - 1)
        last_year_end = end_date.replace(year=end_date.year - 1)

        # Get historical weather for each day in the date range
        historical_data = []
        current_date = last_year_start
        while current_date <= last_year_end:
            daily_weather = self._get_historical_weather(location_key, current_date, api_key)
            if daily_weather:
                historical_data.append(daily_weather)
            current_date += timedelta(days=1)

        weather_history = WeatherHistory(historical_weather=historical_data)
            
        return weather_history
    
    def _arun(self, city: str, start_date: date, end_date: date) -> WeatherHistory:
        """Async implementation of the weather tool."""
        raise NotImplementedError("Async implementation not available")

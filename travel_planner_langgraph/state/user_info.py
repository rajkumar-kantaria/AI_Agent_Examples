from typing import Optional, TypedDict
from pydantic import Field
from datetime import date

class UserInfo(TypedDict):
    name: Optional[str] = Field(
        description="the provided full name of the user"
    )
    current_city: Optional[str] = Field(
        description="the provided current city of the user"
    )
    travel_type: Optional[str] = Field(
        description="the provided travel type of the user. Eg: Romantic, Adventure, Leisure, etc"
    )
    travel_start_date: Optional[date] = Field(
        description="the provided start date of the travel"
    )
    travel_end_date: Optional[date] = Field(
        description="the provided end date of the travel"
    )
    budget: Optional[int] = Field(
        description="the provided budget for the trip in INR"
    )
    possible_destinations: Optional[str] = Field(
        description="The possible list of destinations based on the user criteria. Do not ask it from user. It will be provided by the system."
    )
    selected_destination: Optional[str] = Field(
        description="The selected destination that user wants to visit. Do not ask it from user. It will be provided by the system."
    )
    
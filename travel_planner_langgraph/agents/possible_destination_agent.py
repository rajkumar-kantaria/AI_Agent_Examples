from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from pydantic import BaseModel, Field
from typing import List
from state.assistant_graph_state import AssistantGraphState
from dotenv import load_dotenv

load_dotenv()

class Destinations(BaseModel):
    destinations: List[str] = Field(description="List of destinations to visit based on preferences")

DESTINATION_PROMPT = """You are an expert in choosing destination for travel plan. You can suggest list of destinations based on
the user's preferences such as type of trip, number of days for trip, budget. Provide the list of destinations, user can visit based
on these inputs. Return the list of only 5 most relevant destinations.
User's current location: {current_location}
Type of trip: {trip_type}
Start date of the trip: {start_date}
End date of the trip: {end_date}
Budget in INR: {budget}"""

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)


def possible_destination_node(state: AssistantGraphState):
    # print("Starting destination node....")
    prompt = DESTINATION_PROMPT.format(
        current_location=state['required_information']['current_city'],
        trip_type=state['required_information']['travel_type'],
        start_date=state['required_information']['travel_start_date'],
        end_date=state['required_information']['travel_end_date'],
        budget=state['required_information']['budget']
    )
    messages = [
        SystemMessage(content=prompt),
        HumanMessage(content="Please suggest destinations based on the above preferences.")
    ]
    
    response = model.with_structured_output(Destinations).invoke(messages)
    
    required_information = state["required_information"]
    required_information["possible_destinations"] = response.destinations

    # print("Finished destination node....")
    return {"required_information" : required_information}


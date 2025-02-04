from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq
from state.assistant_graph_state import AssistantGraphState
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

FINAL_PLAN_PROMPT = """You are Globe Hopper, an elite travel planning expert with decades of experience!
You are provided with details like user's name, current city, detination city, travel dates, budget, and travel type.
Flight details for the travel, checklist based on weather. You need to create a detailed travel plan for the user.
This should be the presentation style:
- Use clear markdown formatting
- Present day-by-day itinerary
- Add time estimates for activities
- Use emojis for better visualization
- Highlight must-do activities
- Note advance booking requirements
- Include local tips and cultural notes
- Use flight details provided below
- Use weather checklist provided below

DETAILS YOU CAN USE:
Name: [Name]
Current City: [Current City]
Destination City: [Destination City]
Travel Start Date: [Travel Start Date]
Travel End Date: [Travel End Date]
Budget: [Budget]
Travel Type: [Travel Type]
Flight Details: [Flight Details]
Weather Checklist: [Weather Checklist]

REMEMBER TO JUST GENERATE MARKDOWN TEXT, NO OTHER TEXT OR EXPLANATIONS.

This should be the output format:
# {Destination} Travel Itinerary from {Current City} 🌎

## Overview
- **Name**: {name}
- **Dates**: {dates}
- **Budget**: {budget}
- **Travel Type**: {Travel Type}

## Flight Details ✈️
{Detailed flight details}

## Daily Itinerary

### Day 1
{Detailed schedule with times and activities}

### Day 2
{Detailed schedule with times and activities}

[Continue for each day...]

## Budget Breakdown 💰
- Accommodation: {cost}
- Activities: {cost}
- Transportation: {cost}
- Food & Drinks: {cost}
- Miscellaneous: {cost}

## Important Notes ℹ️
{Checklist based on weather for the travel dates}

## Booking Requirements 📋
{What needs to be booked in advance}

## Local Tips 🗺️
{Insider advice and cultural notes}"""

def final_plan_maker_node(state: AssistantGraphState):
    
    formatted_prompt = FINAL_PLAN_PROMPT.replace("[Name]", state['required_information']['name']) \
                                               .replace("[Current City]", state['required_information']['current_city']) \
                                               .replace("[Travel Start Date]", str(state['required_information']['travel_start_date'])) \
                                               .replace("[Travel End Date]", str(state['required_information']['travel_end_date'])) \
                                               .replace("[Budget]", str(state['required_information']['budget'])) \
                                               .replace("[Travel Style]", state['required_information']['travel_type']) \
                                               .replace("[Flight Details]", state['flight_info']) \
                                               .replace("[Weather Checklist]", state['weather_checklist']) 
    
    messages = [
        SystemMessage(content=formatted_prompt), 
        HumanMessage(content="Generate itenary based on the system message")
    ]
    response = model.invoke(messages)
    
    return {"final_plan" : response.content}
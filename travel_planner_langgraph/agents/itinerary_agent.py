from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from state.assistant_graph_state import AssistantGraphState
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

ITINERARY_PROMPT = '''
Create a detailed travel itinerary for a trip to [City Name] from [Start Date] to [End Date], tailored for a [Type of Travel] experience (e.g., Leisure, Adventure, Cultural, Romantic, Family, etc.). The itinerary should include a structured plan for each day, covering key activities, meal recommendations, and logistics. Ensure that the schedule is well-paced, realistic, and optimized for the travel type.
REMEMBER to account the budget for the trip. The trip budget is [Trip Budget] INR.
Each day's itinerary should include:

Accommodation: Hotel check-in and check-out details. Just specify check in or check out at hotel. Do not specify hotel name.
Morning Activities: Sightseeing, adventure activities, cultural experiences, or relaxation as per the travel type.
Lunch: Recommendations for local restaurants or cafes.
Afternoon Activities: Visits to landmarks, shopping areas, adventure spots, or free time suggestions.
Evening Activities: Entertainment, nightlife, or unique experiences specific to the city.
Dinner: Suggested dining spots based on cuisine preferences or local specialties.
Arrival & Departure: Information about flight/train/bus schedules and transfer details.
Customize the itinerary based on the best local experiences, must-visit places, and hidden gems suitable for the travel type. Ensure a balanced mix of activities and free time for a fulfilling journey.
'''

def itinerary_node(state: AssistantGraphState):
    formatted_prompt = ITINERARY_PROMPT.replace("[City Name]", state['required_information']['destinations']) \
                                               .replace("[Start Date]", str(state['required_information']['travel_start_date'])) \
                                               .replace("[End Date]", str(state['required_information']['travel_end_date'])) \
                                                .replace("[Type of Travel]", str(state['required_information']['travel_type'])) \
                                                .replace("[Trip Budget]", str(state['required_information']['budget']))
    messages = [
        SystemMessage(content=formatted_prompt), 
        HumanMessage(content="Generate itenary based on the system message")
    ]
    response = model.invoke(messages)
    
    return {"itinerary" : response.content}
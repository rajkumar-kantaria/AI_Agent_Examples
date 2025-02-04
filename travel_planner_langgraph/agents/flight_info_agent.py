from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools.flight_search_tool import FlightSearchTool
from state.assistant_graph_state import AssistantGraphState
from dotenv import load_dotenv

load_dotenv()

flight_tool = FlightSearchTool()
tools = [flight_tool]

FLIGHT_INFO_PROMPT = '''
Based on the departure city, destination city, start date, and end date, provide a list of available flights. Include details such as the airline, departure time, arrival time, and price for each flight. Ensure the information is accurate and up-to-date to assist the user in planning their trip effectively.
You have access to tool which you can use to fetch information of flights. The tool will provide you with the list of flights based on the user's inputs.
Departure City: [Departure City]
Destination City: [Destination City]
Start date: [Start Date]
End date: [End Date]
Format the each flight information in the following format:
Airline: [Airline Name]
Departure Time: [Departure Time]
Arrival Time: [Arrival Time]
Layover if any: [Layover Details]
Price: [Price in INR]
Flight number: [Flight Number]
Departure Airport: [Departure Airport]
Arrival Airport: [Arrival Airport]
'''

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

def flight_info_node(state: AssistantGraphState):
    formatted_prompt = FLIGHT_INFO_PROMPT.replace("[Departure City]", state['required_information']['current_city']) \
                                               .replace("[Destination City]", str(state['required_information']['selected_destination'])) \
                                               .replace("[Start Date]", str(state['required_information']['travel_start_date'])) \
                                               .replace("[End Date]", str(state['required_information']['travel_end_date']))
    agent = create_react_agent(
        model,
        tools=tools
    )
    
    agent_response = agent.invoke({
        "messages": [
            {
                "role": "user", 
                "content": formatted_prompt
            }
        ]
    })
    
    return {"flight_info" : agent_response["messages"][-1].content}
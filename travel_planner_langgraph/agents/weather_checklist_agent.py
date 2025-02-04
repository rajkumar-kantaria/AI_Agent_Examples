from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools.weatherapi_tool import WeatherTool
from state.assistant_graph_state import AssistantGraphState
from dotenv import load_dotenv

load_dotenv()

weather_tool = WeatherTool()
tools = [weather_tool]

WEATHER_CHECKLIST_PROMPT = '''
Generate a comprehensive travel checklist for a trip to [City Name] from [Start Date] to [End Date]. Consider the expected weather forecast during this period and suggest appropriate items accordingly. The checklist should be well-organized into the following sections:

Clothing: Based on the weather conditions, recommend suitable outfits, footwear, and accessories.
Electronics: List essential gadgets such as chargers, power banks, travel adapters, and any city-specific tech needs.
Toiletries: Include personal hygiene items, skincare essentials (adjusted for climate), and any travel-size products.
Miscellaneous: Suggest travel documents, medications, local currency, and any special items relevant to the city.
Additional Considerations: Highlight any city-specific requirements, such as cultural attire, safety precautions, or local customs that may impact packing.
Ensure the checklist is practical, well-structured, and tailored to the traveler's destination and travel dates.
'''

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

def weather_checklist_node(state: AssistantGraphState):
    formatted_prompt = WEATHER_CHECKLIST_PROMPT.replace("[City Name]", state['required_information']['selected_destination']) \
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
    return {"weather_checklist" : agent_response["messages"][-1].content}
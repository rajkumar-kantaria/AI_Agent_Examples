from langchain_groq import ChatGroq
from langgraph.types import interrupt
from langchain.schema import AIMessage
from state.assistant_graph_state import AssistantGraphState
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)
assistant_prompt = """
Parse the input and determine the destination user has selected from the list of possible destinations. 
Return only the selected destination from the given list: {possible_destinations}.
User input: {input}
"""

def select_destination_node(state: AssistantGraphState):
    
    possible_destinations = state['required_information']['possible_destinations']
    
    question = "Based on the input, these are the possible destinations. Please select one of the destinations from this list: " + ", ".join(possible_destinations)
    sample_text = AIMessage(content=question)
    state["messages"].append(sample_text)

    selected_destination = interrupt(
        question
    )
        
    # Format the prompt with the required information
    formatted_prompt = assistant_prompt.format(
        possible_destinations=possible_destinations,
        input=selected_destination
    )
    
    # Invoke the model with the formatted prompt
    response = model.invoke(formatted_prompt)
    
    # Create a simple structure to hold the response
    class DestinationSelection(BaseModel):
        place: str
        
    # Parse the response into the expected structure
    res = DestinationSelection(place=response.content)

    required_information = state["required_information"]
    required_information["selected_destination"] = res.place
    
    # print("Finished destination selection node....")
    return {"required_information": required_information}

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.graph import END, StateGraph
from state.assistant_graph_state import AssistantGraphState
from agents.assistant_agent import assistant_node, collect_info
from state.user_info import UserInfo
from langgraph.checkpoint.memory import MemorySaver
import uuid
from langgraph.types import Command
from agents.possible_destination_agent import possible_destination_node
from agents.weather_checklist_agent import weather_checklist_node
from agents.flight_info_agent import flight_info_node
from agents.final_plan_maker_agent import final_plan_maker_node
from agents.human_destination_selector_agent import select_destination_node
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
workflows = {}

class UserInput(BaseModel):
    message: str
    thread_id: str = None

def provided_all_details(state: AssistantGraphState) -> str:
    if "required_information" not in state:
        return "need to collect more information"
    provided_information: UserInfo = state["required_information"]
    if (
        provided_information.get("name")
        and provided_information.get("current_city")
        and provided_information.get("travel_type")
        and provided_information.get("travel_start_date")
        and provided_information.get("travel_end_date")
        and provided_information.get("budget")
    ):
        return "all information collected"
    else:
        return "need to collect more information"
        
def create_workflow():
    workflow = StateGraph(AssistantGraphState)

    # Add nodes to the workflow
    workflow.add_node("assistant", assistant_node)
    workflow.add_node("collect_info", collect_info)
    workflow.add_node("possible_destination_node", possible_destination_node)
    workflow.add_node("weather_checklist_node", weather_checklist_node)
    workflow.add_node("flight_info_node", flight_info_node)
    workflow.add_node("final_plan_maker_node", final_plan_maker_node)
    workflow.add_node("select_destination_node", select_destination_node)

    #Set Entrypoint of the workflow
    workflow.set_entry_point("assistant")

    #Add edges between nodes
    workflow.add_edge("assistant", "collect_info")
    workflow.add_conditional_edges(
        "collect_info",
        provided_all_details,
        {
            "need to collect more information": "assistant",
            "all information collected": "possible_destination_node",
        },
    )
    workflow.add_edge("possible_destination_node", "select_destination_node")
    workflow.add_edge("select_destination_node", "weather_checklist_node")
    workflow.add_edge("select_destination_node", "flight_info_node")
    workflow.add_edge("weather_checklist_node", "final_plan_maker_node")
    workflow.add_edge("flight_info_node", "final_plan_maker_node")
    workflow.add_edge("final_plan_maker_node", END)
    
    checkpointer = MemorySaver()
    graph = workflow.compile(checkpointer=checkpointer)
    graph.get_graph().draw_mermaid_png(output_file_path="graph.png")
    return graph

@app.post("/chat")
async def chat(user_input: UserInput):
    if not user_input.thread_id:
        thread_id = str(uuid.uuid4())
        workflows[thread_id] = create_workflow()
        thread_config = {"configurable": {"thread_id": thread_id}}
        result = workflows[thread_id].invoke(
            {"user_question": user_input.message},
            config=thread_config
        )
    else:
        if user_input.thread_id not in workflows:
            raise HTTPException(status_code=404, detail="Thread not found")
        thread_config = {"configurable": {"thread_id": user_input.thread_id}}
        result = workflows[user_input.thread_id].invoke(
            Command(resume=user_input.message),
            config=thread_config
        )

    # print("Last message:", result["messages"][-1])
    response_message = result.get("final_plan") if result.get("final_plan") else (
        result["messages"][-1].content if result.get("messages") else "No response"
    )

    if result.get("final_plan"):
        return {
            "message": response_message
        }
    else:
        return {
            "thread_id": user_input.thread_id or thread_id,
            "message": response_message
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

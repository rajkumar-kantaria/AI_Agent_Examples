from langchain_core.prompts import ChatPromptTemplate
from typing import Any, Dict
from state.assistant_graph_state import AssistantGraphState
from state.user_info import UserInfo
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.types import interrupt
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(
    model="llama-3.3-70b-versatile"
)

SYSTEM_PROMPT = """You are a a helpful travel assistant \n tasked with helping a customer for theier travel planning.
            1. You first need to collect some travel information before you can proceed.
            2. After your collect ALL information say thank you and that you
               are going to make travel itinerary for them.
            
            The information needs to be collected: 

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

            make sure you have the information before you can proceed, but only one field at a time
            if the input from user was wrong please tell them why.
            
            DO NOT FILL IN THE USERS INFORMATION, YOU NEED TO COLLECT IT.
            """
assistant_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM_PROMPT),
        (
            "human",
            "User question: {user_question}"
            "Chat history: {messages}"
            "\n\n What the user have provided so far {provided_required_information} \n\n",
        ),
    ]
)

def assistant_node(state: AssistantGraphState) -> Dict[str, Any]:
    get_information_chain = assistant_prompt | model
    res = get_information_chain.invoke(
        {
            "user_question": state["user_question"],
            "provided_required_information": state["required_information"] if "required_information" in state else None,
            "messages": state["messages"] if "messages" in state else [],
        }
    )
    print(res.content)
    return {"messages": [res]}

def collect_info(state: AssistantGraphState) -> Dict[str, Any]:
    # information_from_stdin = str(input("\nenter information\n"))
    question = state["messages"][-1] if "messages" in state else "Sample question"
    information_from_stdin = interrupt(
        question
    )
    structured_llm_user_info = model.with_structured_output(UserInfo)

    information_chain = assistant_prompt | structured_llm_user_info
    res = information_chain.invoke(
        {
            "user_question": state["user_question"],
            "provided_required_information": information_from_stdin,
            "messages": state["messages"],
        }
    )

    # print("res:", res)
    required_info = res
    return {
        "required_information": required_info,
        "messages": [HumanMessage(content=information_from_stdin)],
    }
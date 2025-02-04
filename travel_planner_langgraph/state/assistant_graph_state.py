from typing import Annotated, TypedDict, Optional
from langgraph.graph import add_messages
from pydantic import Field
from state.user_info import UserInfo

class AssistantGraphState(TypedDict):
    user_question: str
    required_information: UserInfo
    messages: Annotated[list, add_messages]
    verified: bool
    weather_checklist: Optional[str] = Field(
        description="The weather checklist for the user. Do not ask it from user. It will be provided by the system."
    )
    itinerary: Optional[str] = Field(
        description="The itinerary for the user. Do not ask it from user. It will be provided by the system."
    )
    flight_info: Optional[str] = Field(
        description="The flight information for the user. Do not ask it from user. It will be provided by the system."
    )
    final_plan: Optional[str] = Field(
        description="The final travel plan details."
    )
    question_for_user: Optional[str] = Field(
        description="Question to ask to user"
    )
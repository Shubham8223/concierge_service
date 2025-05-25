from typing import TypedDict, Annotated, List, Dict, Any
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from server.schemas.concierge_service_schema import FollowUpQuestionSchema


class AgentState(TypedDict, total=False):
    input: str
    messages: Annotated[List[BaseMessage], add_messages]
    intent_category: str
    confidence_score: float
    entities: List[Dict[str, Any]]
    follow_up_questions: List[FollowUpQuestionSchema]
    web_search_results: List[str]
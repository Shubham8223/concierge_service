
from pydantic import BaseModel
from typing import Any, List

class ConciergeWorkflowRequest(BaseModel):
    input: str
    messages: List[Any] = []
    entities: List[Any] = []
    follow_up_questions: List[Any] = []
    web_search_results: List[str] = []
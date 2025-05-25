
from pydantic import BaseModel
from typing import List, Any

class WebSearchOutput(BaseModel):
    web_search_results: str
    model_config = {
        "extra": "ignore"
    }

class ConciergeWorkflowOutput(BaseModel):
    intent_category: str 
    confidence_score: float 
    entities: dict
    follow_up_questions: List[Any]
    model_config = {
        "extra": "ignore"
    }

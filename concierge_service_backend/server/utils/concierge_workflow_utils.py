from typing import List, Tuple, Type, Dict
from pydantic import BaseModel, Field
from server.schemas import concierge_service_schema
def create_dynamic_schema_for_entities_with_follow_up_questions(intent_category: str) -> Tuple[Type[BaseModel], Dict[str, str]]:
    intent_entities = concierge_service_schema.INTENT_ENTITIES_SCHEMA_MAPPER[intent_category]
    field_descriptions = {
        field: info.description
        for field, info in intent_entities.model_fields.items()
    }
    class EntityFollowUpQuestionsSchema(BaseModel):
        follow_up_questions: List[concierge_service_schema.FollowUpQuestionSchema] = Field(description="A list of follow up questions, each with its type and potential answer options.")
        entities: intent_entities = Field(description="Entities data for this intent category")

    return EntityFollowUpQuestionsSchema, field_descriptions

def get_schema_from_state(state):
    intent_category = state["intent_category"]
    schema_class, field_descriptions = create_dynamic_schema_for_entities_with_follow_up_questions(intent_category)
    return {"schema_class":schema_class,"field_descriptions":field_descriptions}

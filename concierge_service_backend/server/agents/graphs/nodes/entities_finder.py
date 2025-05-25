from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable
from server.agents.states.concierge_workflow_state import AgentState
from server.decorators.inject_and_validate_schema import inject_and_validate_schema
from server.utils.concierge_workflow_utils import get_schema_from_state
from typing import Type, Dict
from pydantic import BaseModel
from datetime import datetime
import json


@inject_and_validate_schema(get_schema_from_state)
async def entities_finder(state: AgentState, llm: Runnable , system_prompt: str, human_prompt: str, schema_class : Type[BaseModel], field_descriptions: Dict[str, str]) -> dict:
    intent_category = state["intent_category"]
    input = state["input"]
    current_time = datetime.now().isoformat()

    messages = [
        ("system", system_prompt),
        ("human", human_prompt),
    ]
    parser = JsonOutputParser(pydantic_object=schema_class)
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    chain = chat_prompt | llm | parser

    try:
        response = await chain.ainvoke(input={"input": input,"field_descriptions": field_descriptions, "intent_category": intent_category, "current_time":current_time, "format_instructions": parser.get_format_instructions()}) 
        if response["entities"]:
            response["entities"] = {k: v for k, v in response["entities"].items() if v}

        return {"entities": response["entities"], "follow_up_questions": response["follow_up_questions"],"messages":[AIMessage(content=json.dumps(response))]}

    except Exception as e:
        print("An unexpected error occurred:", e)
        raise RuntimeError(f"Error fetching the data: {str(e)}")
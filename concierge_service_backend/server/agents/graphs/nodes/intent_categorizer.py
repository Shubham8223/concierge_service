from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable
from server.agents.states.concierge_workflow_state import AgentState
from server.schemas.concierge_service_schema import IntentCategorySchema
from server.decorators.inject_and_validate_schema import inject_and_validate_schema
from typing import Type 
from pydantic import BaseModel
import json


@inject_and_validate_schema(IntentCategorySchema)
async def intent_categorizer(state: AgentState, llm: Runnable, system_prompt: str, human_prompt: str, schema_class : Type[BaseModel]) -> dict:
    input = state["input"]

    messages = [
        ("system", system_prompt),
        ("human", human_prompt),
    ]
    
    parser = JsonOutputParser(pydantic_object=schema_class)
    chat_prompt = ChatPromptTemplate.from_messages(messages)
    chain = chat_prompt | llm | parser

    try:
        response = await chain.ainvoke(input={"input": input,"format_instructions": parser.get_format_instructions()})

        return {"confidence_score": response["confidence_score"], "intent_category": response["intent_category"],"messages":[AIMessage(content=json.dumps(response))]}

    except Exception as e:
        print("An unexpected error occurred:", e)
        raise RuntimeError(f"Error fetching the data: {str(e)}")

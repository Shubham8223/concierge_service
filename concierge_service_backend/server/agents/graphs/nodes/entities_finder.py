from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable
from server.agents.states.concierge_workflow_state import AgentState
from server.decorators.inject_and_validate_schema import inject_and_validate_schema
from server.decorators.inject_llm import inject_llm
from server.utils.concierge_workflow_utils import get_schema_from_state
from typing import Type, Dict
from pydantic import BaseModel
from datetime import datetime
import json


@inject_and_validate_schema(get_schema_from_state)
@inject_llm('bedrock_claude_3_7_sonnet')
async def entities_finder(state: AgentState, llm: Runnable ,schema_class : Type[BaseModel], field_descriptions: Dict[str, str]) -> dict:
    intent_category = state["intent_category"]
    input = state["input"]
    current_time = datetime.now().isoformat()
    system_prompt = """
    You are an entity extraction assistant. Your task is to:

    1. Analyze the user query and the provided intent category.
    2. Extract relevant entities from the predefined list below.
    3. If any expected entity is missing, generate a list of clear, concise follow-up questions to gather that missing information from the user.
    4. Use the current timestamp to interpret or validate any time-related information (e.g., booking time, delivery date, etc.).
  
    Current timestamp: {current_time}

    Valid intent entities with descriptions:
    {field_descriptions}
    Return only a parsable JSON object. Do not include any explanation or extra text.
    """

    human_prompt = """
    Given the user query and its intent category, extract entities and generate follow-up questions as needed.

    User query: {input}
    Intent category: {intent_category}

    {format_instructions}
    """


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
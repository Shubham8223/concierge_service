from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.messages import AIMessage
from langchain_core.runnables import Runnable
from server.agents.states.concierge_workflow_state import AgentState
from server.schemas.concierge_service_schema import IntentCategorySchema
from server.decorators.inject_and_validate_schema import inject_and_validate_schema
from server.decorators.inject_llm import inject_llm
from typing import Type 
from pydantic import BaseModel
import json


@inject_and_validate_schema(IntentCategorySchema)
@inject_llm('bedrock_claude_3_7_sonnet')
async def intent_categorizer(state: AgentState, llm: Runnable, schema_class : Type[BaseModel]) -> dict:
    input = state["input"]
    system_prompt = """
    You are an intent categorization assistant. Your task is to analyze user input and determine the most relevant intent category from the predefined list below.
    You must also assign a confidence score between 0 and 1 indicating how confident you are in your classification.
    Valid intent categories:
    1. "dining" – Queries about restaurant reservations, cuisine preferences, finding places to eat, booking a table, or dining experiences.
    2. "gifting" – Queries involving buying or sending gifts, gift recommendations, selecting gifts for someone, or choosing gift types like flowers, gadgets, etc.
    3. "travel" – Queries related to planning or booking travel such as flights, trains, destinations, travel dates, or vacation plans.
    4. "cab booking" – Queries about booking a taxi, cab service, finding rides, pickup/drop locations, or selecting cab types.
    If none of the categories match, use the "other" category with confidence_score 0.
    Return only a parsable JSON object. Do not include any explanation or extra text.
    """
    human_prompt = """
    Analyze the following user query: {input}
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
        response = await chain.ainvoke(input={"input": input,"format_instructions": parser.get_format_instructions()})

        return {"confidence_score": response["confidence_score"], "intent_category": response["intent_category"],"messages":[AIMessage(content=json.dumps(response))]}

    except Exception as e:
        print("An unexpected error occurred:", e)
        raise RuntimeError(f"Error fetching the data: {str(e)}")

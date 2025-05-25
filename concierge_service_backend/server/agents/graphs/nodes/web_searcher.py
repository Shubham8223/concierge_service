from langchain_core.messages import ToolMessage
from server.agents.states.concierge_workflow_state import AgentState

async def web_searcher(state: AgentState, tools: dict) -> dict:
    input = state["input"]
    try:
        search_input = { "query":input}
        results = tools.get("duckduckgo_search").invoke({"search_input": search_input})

        return {"web_search_results":results ,"messages":[ToolMessage(
            content=results,
            tool_name="duckduckgo_search",
            tool_call_id="1234")]}

    except Exception as e:
        print("An unexpected error occurred:", e)
        raise RuntimeError(f"Error fetching the data: {str(e)}")
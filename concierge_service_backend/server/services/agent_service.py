
from fastapi import HTTPException
from server.agents.graphs import concierge_workflow_graph
from server.agents.states import concierge_workflow_state
from server.schemas import response_schemas
class AgentService:
    def __init__(self):
        ...

    async def query_concierge_workflow_graph(self, state: dict) -> dict:
        if not state:
             raise HTTPException(status_code=404, detail="params is missing.")
        graph = concierge_workflow_graph.Graph(concierge_workflow_state.AgentState)
        results = await graph.invoke(state)
        if results['intent_category'] == "other":
            return response_schemas.WebSearchOutput(**results).dict(),200
        return response_schemas.ConciergeWorkflowOutput(**results).dict(),200
    

    

from fastapi import APIRouter, HTTPException, Depends
from server.utils.response_handlers import success_response, error_response
from server.schemas import request_schemas
from server.services.agent_service import AgentService

router = APIRouter()

def get_agent_service():
    return AgentService()

@router.post("/call-concierge-service")
async def call_concierge_service(state: request_schemas.ConciergeWorkflowRequest ,service: AgentService = Depends(get_agent_service)):
    try:
        data, status_code = await service.query_concierge_workflow_graph(state)
        return success_response(data=data, status_code=status_code, message="Concierge service executed successfully")
    except HTTPException as e:
        return error_response(message = "An Unexpected Error Occured", status_code=e.status_code, details={"error": str(e)})
    except ValueError as e:
        return error_response(message = "An Unexpected Error Occured", status_code=404 , details={"error": str(e)})
    except Exception as e:
        return error_response( message = "An Unexpected Error Occured", status_code=500, details={"error": str(e)})


from fastapi import APIRouter

from server.api.v1.agent import router as agent_router

router = APIRouter()

router.include_router(agent_router, prefix="/agent", tags=["Agent"])

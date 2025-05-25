from fastapi import FastAPI,APIRouter
from server.api.v1 import router as api_v1_router 
from contextlib import asynccontextmanager
from server.config.logging import logger
from server.decorators.logging_middleware import logging_middleware
from dotenv import load_dotenv

load_dotenv()


@asynccontextmanager #context manager for handling lifecycle of connections
async def lifespan(app: FastAPI):

    logger.info("Application Started")

    yield

    logger.info("Application Closed Gracefully.")

app = FastAPI(lifespan=lifespan)
        
app.middleware("http")(logging_middleware)

api_router = APIRouter()

api_router.include_router(api_v1_router, prefix="/v1")

app.include_router(api_router, prefix="/api")

from fastapi import Request, Response
from server.config.logging import logger

async def logging_middleware(request: Request, call_next):
    try:
        if request.method in ["POST", "PUT", "PATCH"]:
            request_payload = await request.json()
        else:
            request_payload = {}
        logger.info(f"Request: {request.method} {request.url} - Payload: {request_payload}")

        response = await call_next(request)

        logger.info(f"Response: {response.status_code} for {request.method} {request.url}")
        return response

    except Exception as e:
        logger.error(f"Error occurred: {str(e)} - Request Payload: {request_payload}")
        return Response("Internal Server Error", status_code=500)

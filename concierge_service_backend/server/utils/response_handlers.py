from fastapi.responses import JSONResponse
from fastapi import status as http_status


def success_response(data=None, message="Request completed successfully", status_code=http_status.HTTP_200_OK):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "data": data,
            "message": message
        }
    )


def error_response(message: str, status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR, details: dict = {}):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": status_code,
            "data": None,
            "message": message,
            **details
        }
    )

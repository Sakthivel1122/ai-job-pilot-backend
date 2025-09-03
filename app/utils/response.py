from fastapi.responses import JSONResponse
from fastapi import HTTPException

def response(content=None, message="", status_code=400):
    if content is None:
        content = {}
    return JSONResponse(
        content={
            "content": content,
            "response": {
                "message": message,
                "status": status_code
            }
        },
        status_code=status_code
    )

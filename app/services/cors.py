from fastapi.routing import APIRoute
from fastapi import Request
from starlette.responses import Response, JSONResponse

ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://sakthivel-profile.vercel.app",
    # Add more if needed
]

class CORSEnabledRoute(APIRoute):
    def __init__(self, *args, **kwargs):
        # Ensure OPTIONS is always in the methods
        methods = kwargs.get("methods", [])
        if "OPTIONS" not in methods:
            methods = list(set(methods + ["OPTIONS"]))
        kwargs["methods"] = methods

        super().__init__(*args, **kwargs)
    
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_handler(request: Request):
            origin = request.headers.get("origin")

            # Handle preflight OPTIONS request
            if request.method == "OPTIONS":
                if origin in ALLOWED_ORIGINS:
                    return Response(
                        status_code=204,
                        headers={
                            "Access-Control-Allow-Origin": origin,
                            "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
                            "Access-Control-Allow-Headers": "Content-Type, X-API-KEY",
                            "Access-Control-Max-Age": "86400"
                        }
                    )
                return Response(status_code=403, content="CORS origin not allowed")

            # Proceed with normal request
            response: Response = await original_route_handler(request)

            if origin in ALLOWED_ORIGINS:
                response.headers["Access-Control-Allow-Origin"] = origin
                response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
                response.headers["Access-Control-Allow-Headers"] = "Content-Type, X-API-KEY"

            return response

        return custom_handler

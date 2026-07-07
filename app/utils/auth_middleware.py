from starlette.middleware.base import BaseHTTPMiddleware

from app.logger import logger


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request,
        call_next
    ):

        logger.info(
            f"Authenticated Request : "
            f"{request.method} {request.url}"
        )

        response = await call_next(request)

        return response
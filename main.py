from fastapi import FastAPI, Request
from router.items import router as items_router
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from router.limit import limiter
from logger import logger
import time


app = FastAPI(title="fastapi PROD READY DB", 
              summary="tips: https://www.youtube.com/watch?v=XlnmN4BfCxw",
              version="0.0.1",
              terms_of_service="http://example.com/terms/",
              contact={
                  "name": "support",
                  "url": None,
                  "email": "bouchetjonathan@gmail.com",
                  },
              license_info={
                "name": "Apache 2.0",
                "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}
                )


@app.middleware('http') # middleware is ran on every request
async def log_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    response_time = time.time() - start_time

    log_dict = {
        "url": request.url.path,
        "method": request.method,
        "response time": response_time
    }

    logger.info(log_dict)
    return response

@app.get("/", tags=["health check"])
async def root() -> dict:
    return {"message": "Hello World"}

app.include_router(items_router)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
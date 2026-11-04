import logging
import traceback

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse

from app.api.routers.categories import router as categories_router
from app.api.routers.task import router as task_router
from app.core.config import get_settings
from app.core.log import configure_logging

# 1. Логирование
configure_logging()
logger = logging.getLogger("app.middleware")

# 2. Настройки
settings = get_settings()

# 3. Приложение
app = FastAPI()


# 4. CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allowed_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

counter = 0


# 5. Middleware логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next) -> Response:
    global counter
    response = await call_next(request)
    counter += 1
    response.headers["x-request-number"] = str(counter)
    return response


# допустим работает


# 6. Debug-обработчик исключений
@app.exception_handler(Exception)
async def debug_exceptions_handler(request: Request, exc: Exception):
    tb = traceback.format_exc()
    print("=" * 80, flush=True)
    print(f"UNHANDLED ERROR on {request.method} {request.url.path}", flush=True)
    print(tb, flush=True)
    print("=" * 80, flush=True)
    return PlainTextResponse(tb, status_code=500)


# 7. Роутеры
app.include_router(router=task_router)
app.include_router(router=categories_router)

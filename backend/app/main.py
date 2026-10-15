"""
Main FastAPI Application Entrypoint
Integrates REST APIs, CORS middleware, error handlers, and database lifecycle.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.core.database import init_db

# Routers
from backend.app.api.endpoints.health import router as health_router
from backend.app.api.endpoints.properties import router as properties_router
from backend.app.api.endpoints.reservations import router as reservations_router
from backend.app.api.endpoints.revenue import router as revenue_router
from backend.app.api.endpoints.occupancy import router as occupancy_router
from backend.app.api.endpoints.invoices import router as invoices_router
from backend.app.api.endpoints.reconciliation import router as reconciliation_router
from backend.app.api.endpoints.expenses import router as expenses_router
from backend.app.api.endpoints.competitors import router as competitors_router
from backend.app.api.endpoints.reports import router as reports_router
from backend.app.api.endpoints.alerts import router as alerts_router
from backend.app.api.endpoints.agents import router as agents_router
from backend.app.api.endpoints.ask import router as ask_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hospitality_app")


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info("Initializing database schema on startup...")
    init_db()
    logger.info("Application startup sequence completed.")
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Agentic Layer for Fintech Operations & Competitive Intelligence in Hospitality Services",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception on {request.url.path}: {exc}", exc_info=True)
    detail = "An internal server error occurred. Please consult backend logs."
    if settings.DEBUG:
        detail = f"{type(exc).__name__}: {str(exc)}"
    return JSONResponse(
        status_code=500,
        content={"detail": detail}
    )

# Include Routers
app.include_router(health_router, prefix=settings.API_V1_PREFIX)
app.include_router(health_router) # Also mount /health at root
app.include_router(properties_router, prefix=settings.API_V1_PREFIX)
app.include_router(reservations_router, prefix=settings.API_V1_PREFIX)
app.include_router(revenue_router, prefix=settings.API_V1_PREFIX)
app.include_router(occupancy_router, prefix=settings.API_V1_PREFIX)
app.include_router(invoices_router, prefix=settings.API_V1_PREFIX)
app.include_router(reconciliation_router, prefix=settings.API_V1_PREFIX)
app.include_router(expenses_router, prefix=settings.API_V1_PREFIX)
app.include_router(competitors_router, prefix=settings.API_V1_PREFIX)
app.include_router(reports_router, prefix=settings.API_V1_PREFIX)
app.include_router(alerts_router, prefix=settings.API_V1_PREFIX)
app.include_router(agents_router, prefix=settings.API_V1_PREFIX)
app.include_router(ask_router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs" if settings.DEBUG else None,
        "health_check": "/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)

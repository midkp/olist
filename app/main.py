"""Main entry point for the Olist API application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.csv_upload import router as csv_router

# from app.core.security import get_api_key
from app.api.routes import router as api_router
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    # dependencies=[Depends(get_api_key)],  # Disabled to bypass API key check
)

# CORS middleware (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(api_router)
app.include_router(csv_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)

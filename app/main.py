from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config, logging_config
from app.api.routes import router as api_router
from app.api.csv_upload import router as csv_router
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

app = FastAPI(title=config.settings.APP_NAME)

# Allow all origins (for development; restrict this in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(api_router)
app.include_router(csv_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.settings.HOST, port=config.settings.PORT)
# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import config, logging_config
from app.api.routes import router as api_router
from app.api.csv_upload import router as csv_router
from app.api.routes import router  # Import the router from routes.py
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

app = FastAPI(title=config.settings.APP_NAME)

# Allow all origins (for development; restrict this in production)
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
app.include_router(router)  # Include the router from routes.py

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.settings.HOST, port=config.settings.PORT)
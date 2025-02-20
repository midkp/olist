# app/api/csv_upload.py
from fastapi import APIRouter, UploadFile, HTTPException
from pydantic import BaseModel
from app.services.csv_service import CSVService
from app.services.sql_service import SQLService

router = APIRouter(prefix="/api/v1", tags=["CSV Upload", "SQL Query"])

class QueryRequest(BaseModel):
    query: str

@router.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile):
    print(f"Received file: {file.filename}")
    try:
        result = await CSVService.process_csv_upload(table_name, file)
        return {
            "status": "success",
            "table": table_name,
            **result
        }
    except Exception as e:
        raise HTTPException(400, detail=str(e))

@router.post("/query")
async def execute_sql_query(request: QueryRequest):
    """Convert natural language query to SQL and execute it."""
    print(f"Received request body: {request.query}")  # Debug print
    try:
        result = await SQLService.execute_sql_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(400, detail=str(e))
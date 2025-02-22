"""API endpoints for CSV upload, SQL query execution, and catalogue processing."""

from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel

from app.services.catalogue_service import CatalogueService
from app.services.csv_service import CSVService
from app.services.sql_service import SQLService

router = APIRouter(prefix="/api/v1", tags=["CSV Upload", "SQL Query", "Catalogue Processing"])


class QueryRequest(BaseModel):
    """Request model for SQL query execution."""

    query: str


@router.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile):
    """Upload a CSV file and process it into the specified table."""
    try:
        result = await CSVService.process_csv_upload(table_name, file)
        return {"status": "success", "table": table_name, **result}
    except Exception as e:
        raise HTTPException(400, detail=str(e)) from e


@router.post("/query")
async def execute_sql_query(request: QueryRequest):
    """Execute a natural language SQL query."""
    try:
        result = await SQLService.execute_sql_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(400, detail=str(e)) from e


@router.post("/catalogue/{product_id}")
async def process_catalogue(
    product_id: str,
    file: UploadFile,
    product_category_name: str = "mobile",
):
    """Process a catalogue file and store specifications."""
    try:
        result = await CatalogueService.process_catalogue(file, product_id, product_category_name)
        return result
    except Exception as e:
        raise HTTPException(400, detail=str(e)) from e

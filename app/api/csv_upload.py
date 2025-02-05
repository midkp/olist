from fastapi import APIRouter, UploadFile, HTTPException
from app.services.csv_service import CSVService

router = APIRouter(prefix="/api/v1", tags=["CSV Upload"])

@router.post("/upload/{table_name}")
async def upload_csv(table_name: str, file: UploadFile):
    try:
        result = await CSVService.process_csv_upload(table_name, file)
        return {
            "status": "success",
            "table": table_name,
            **result
        }
    except Exception as e:
        raise HTTPException(400, detail=str(e))
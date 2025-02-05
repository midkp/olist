import sqlite3

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import JSONResponse
from app.core.database import get_db_connection  # Corrected import path
# from app.models.seller import Seller  # Uncomment if you have a Seller model

router = APIRouter()

# Root endpoint
@router.get("/")
async def read_root():
    return {"message": "API is working"}

# File upload endpoint
@router.post("/upload/{table_name}")
async def upload_file(table_name: str, file: UploadFile = File(...)):
    # Here you can process the file and store it, or return any other response
    # For now, we will just return the file name and the table name
    return {"message": f"File uploaded successfully to table {table_name}", "filename": file.filename}

@router.get("/sellers")
async def get_sellers():
    db_path = "olist.db"  # Ensure this matches where the database is created
    conn = sqlite3.connect(db_path)  # Make sure this path is correct
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sellers")
    sellers = cursor.fetchall()
    conn.close()  # Don't forget to close the connection
    return {"sellers": [dict(row) for row in sellers]}
import sqlite3
import io
import csv
from fastapi import APIRouter, File, UploadFile

router = APIRouter()

def insert_csv_data_to_db(table_name, file):
    # Open the file in text mode with the correct encoding
    file_content = io.StringIO(file.read().decode('utf-8'))  # Convert bytes to text
    reader = csv.DictReader(file_content)
    
    # Connect to the SQLite database
    conn = sqlite3.connect('olist.db')  # Ensure this points to your correct database
    cursor = conn.cursor()
    
    # Check if the table exists, and create it if it doesn't
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    if not cursor.fetchone():
        # Create table if it doesn't exist
        columns = ', '.join([f"{col} TEXT" for col in reader.fieldnames])  # Assuming all fields are TEXT
        create_table_query = f"CREATE TABLE {table_name} ({columns})"
        cursor.execute(create_table_query)
    
    # Loop through each row in the CSV file and insert it into the database
    for row in reader:

        print("Row Data:", row)  # Debugging line to print each row before inserting
        
        # Construct the insert query dynamically based on the CSV fieldnames
        columns = ', '.join(row.keys())
        placeholders = ', '.join('?' for _ in row)
        insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        # Execute the insert query
        cursor.execute(insert_query, tuple(row.values()))
    
    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    return f"Data uploaded successfully to table {table_name}"

# CSV upload endpoints for each table
@router.post("/upload/customers")
async def upload_olist_customers(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("customers", file.file)}

@router.post("/upload/orders")
async def upload_olist_orders(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("orders", file.file)}

@router.post("/upload/order_items")
async def upload_olist_order_items(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("order_items", file.file)}

@router.post("/upload/order_payments")
async def upload_olist_order_payments(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("order_payments", file.file)}

@router.post("/upload/order_reviews")
async def upload_olist_order_reviews(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("order_reviews", file.file)}

@router.post("/upload/products")
async def upload_olist_products(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("products", file.file)}

@router.post("/upload/sellers")
async def upload_olist_sellers(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("sellers", file.file)}

@router.post("/upload/geolocation")
async def upload_olist_geolocation(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("geolocation", file.file)}

@router.post("/upload/marketing_qualified_leads")
async def upload_olist_marketing_qualified_leads(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("leads_qualified", file.file)}

@router.post("/upload/closed_deals")
async def upload_olist_closed_deals(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("leads_closed", file.file)}

@router.post("/upload/product_category_name_translation")
async def upload_product_category_name_translation(file: UploadFile = File(...)):
    return {"message": insert_csv_data_to_db("product_category_name_translation", file.file)}
"""API routes for uploading CSV data to various tables."""

from fastapi import APIRouter, File, UploadFile

from app.services.csv_service import CSVService

router = APIRouter(prefix="/api/v1", tags=["CSV Upload"])
DEFAULT_FILE = File(...)


@router.post("/upload/customers")
async def upload_customers(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the customers table."""
    result = await CSVService.process_csv_upload("customers", file)
    return {"message": "Uploaded to customers", **result}


@router.post("/upload/orders")
async def upload_orders(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the orders table."""
    result = await CSVService.process_csv_upload("orders", file)
    return {"message": "Uploaded to orders", **result}


@router.post("/upload/order_items")
async def upload_order_items(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the order_items table."""
    result = await CSVService.process_csv_upload("order_items", file)
    return {"message": "Uploaded to order_items", **result}


@router.post("/upload/order_payments")
async def upload_order_payments(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the order_payments table."""
    result = await CSVService.process_csv_upload("order_payments", file)
    return {"message": "Uploaded to order_payments", **result}


@router.post("/upload/order_reviews")
async def upload_order_reviews(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the order_reviews table."""
    result = await CSVService.process_csv_upload("order_reviews", file)
    return {"message": "Uploaded to order_reviews", **result}


@router.post("/upload/products")
async def upload_products(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the products table."""
    result = await CSVService.process_csv_upload("products", file)
    return {"message": "Uploaded to products", **result}


@router.post("/upload/sellers")
async def upload_sellers(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the sellers table."""
    result = await CSVService.process_csv_upload("sellers", file)
    return {"message": "Uploaded to sellers", **result}


@router.post("/upload/geolocation")
async def upload_geolocation(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the geolocation table."""
    result = await CSVService.process_csv_upload("geolocation", file)
    return {"message": "Uploaded to geolocation", **result}


@router.post("/upload/marketing_qualified_leads")
async def upload_marketing_qualified_leads(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the leads_qualified table."""
    result = await CSVService.process_csv_upload("marketing_qualified_leads", file)
    return {"message": "Uploaded to leads_qualified", **result}


@router.post("/upload/closed_deals")
async def upload_closed_deals(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the leads_closed table."""
    result = await CSVService.process_csv_upload("closed_deals", file)
    return {"message": "Uploaded to leads_closed", **result}


@router.post("/upload/product_category_name_translation")
async def upload_product_category_name_translation(file: UploadFile = DEFAULT_FILE):
    """Upload CSV data to the product_category_name_translation table."""
    result = await CSVService.process_csv_upload("product_category_name_translation", file)
    return {"message": "Uploaded to product_category_name_translation", **result}

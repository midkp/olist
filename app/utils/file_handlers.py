import csv
from app.core.config import settings

def validate_csv_structure(table_name: str, file):
    required_columns = {
        'customers': ['customer_id', 'customer_unique_id', ...],
        'orders': ['order_id', 'customer_id', ...],
        # Add all other tables
    }
    
    reader = csv.DictReader(file.file.read().decode().splitlines())
    if not set(required_columns[table_name]).issubset(reader.fieldnames):
        raise ValueError("CSV structure doesn't match table requirements")
    file.file.seek(0)
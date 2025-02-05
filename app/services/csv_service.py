import pandas as pd
from app.core import database
from app.utils.file_handlers import validate_csv_structure

class CSVService:
    @staticmethod
    async def process_csv_upload(table_name: str, file, chunk_size=1000):
        validate_csv_structure(table_name, file)
        
        with database.get_db_connection() as conn:
            cursor = conn.cursor()
            df = pd.read_csv(file.file, chunksize=chunk_size)

            # Get primary key and table schema
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            
            cursor.execute(f"PRAGMA table_info({table_name})")
            primary_key = [col[1] for col in cursor.fetchall() if col[5] == 1][0]

            inserted = 0
            skipped = 0

            for chunk in df:
                for _, row in chunk.iterrows():
                    
                    # **Foreign Key Validation for 'orders' Table**
                    if table_name == 'orders':
                        cursor.execute("SELECT customer_id FROM customers WHERE customer_id = ?", 
                                       (row['customer_id'],))
                        if not cursor.fetchone():
                            raise ValueError(f"Invalid customer_id: {row['customer_id']} - No matching record in customers table.")

                    # Check for duplicates
                    cursor.execute(
                        f"SELECT {primary_key} FROM {table_name} WHERE {primary_key} = ?",
                        (row[primary_key],)
                    )
                    if cursor.fetchone():
                        skipped += 1
                        continue
                    
                    # Insert record
                    placeholders = ", ".join("?" * len(row))
                    columns_str = ", ".join(row.index)
                    cursor.execute(
                        f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})",
                        tuple(row.values)
                    )
                    inserted += 1

            conn.commit()
            
        return {"inserted": inserted, "skipped": skipped}

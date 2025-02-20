# app/services/csv_service.py
import pandas as pd
import logging
from app.core import database
from app.utils.file_handlers import validate_csv_structure

logger = logging.getLogger(__name__)

class CSVService:
    @staticmethod
    async def process_csv_upload(table_name: str, file, chunk_size=1000):
        try:
            # Map API endpoint names to database table names from init_db.py
            table_mapping = {
                'customers': 'customers',
                'orders': 'orders',
                'order_items': 'order_items',
                'order_payments': 'order_payments',
                'order_reviews': 'order_reviews',
                'products': 'products',
                'sellers': 'sellers',
                'geolocation': 'geolocation',
                'marketing_qualified_leads': 'leads_qualified',
                'closed_deals': 'leads_closed',
                'product_category_name_translation': 'product_category_name_translation'
            }
            full_table_name = table_mapping.get(table_name, table_name)

            logger.info(f"Validating CSV structure for table: {full_table_name}")
            validate_csv_structure(full_table_name, file)
            file.file.seek(0)

            with database.get_db_connection() as conn:
                cursor = conn.cursor()

                # Data types matching CSV data and adjusted for init_db.py schema
                dtypes = {
                    'customers': {
                        'customer_id': 'str',
                        'customer_unique_id': 'str',
                        'customer_zip_code_prefix': 'str',
                        'customer_city': 'str',
                        'customer_state': 'str'
                    },
                    'orders': {
                        'order_id': 'str',
                        'customer_id': 'str',
                        'order_status': 'str',
                        'order_purchase_timestamp': 'str',
                        'order_approved_at': 'str',
                        'order_delivered_carrier_date': 'str',
                        'order_delivered_customer_date': 'str',
                        'order_estimated_delivery_date': 'str'
                    },
                    'order_items': {
                        'order_id': 'str',
                        'order_item_id': 'int64',
                        'product_id': 'str',
                        'seller_id': 'str',
                        'shipping_limit_date': 'str',
                        'price': 'float64',
                        'freight_value': 'float64'
                    },
                    'order_payments': {
                        'order_id': 'str',
                        'payment_sequential': 'int64',
                        'payment_type': 'str',
                        'payment_installments': 'int64',
                        'payment_value': 'float64'
                    },
                    'order_reviews': {
                        'review_id': 'str',
                        'order_id': 'str',
                        'review_score': 'int64',
                        'review_comment_title': 'str',
                        'review_comment_message': 'str',
                        'review_creation_date': 'str',
                        'review_answer_timestamp': 'str'
                    },
                    'products': {
                        'product_id': 'str',
                        'product_category_name': 'str',
                        'product_name_length': 'float64',
                        'product_description_length': 'float64',
                        'product_photos_qty': 'float64',
                        'product_weight_g': 'float64',
                        'product_length_cm': 'float64',
                        'product_height_cm': 'float64',
                        'product_width_cm': 'float64'
                    },
                    'sellers': {
                        'seller_id': 'str',
                        'seller_zip_code_prefix': 'str',
                        'seller_city': 'str',
                        'seller_state': 'str'
                    },
                    'geolocation': {
                        'geolocation_zip_code_prefix': 'str',
                        'geolocation_lat': 'float64',
                        'geolocation_lng': 'float64',
                        'geolocation_city': 'str',
                        'geolocation_state': 'str'
                    },
                    'leads_qualified': {
                        'mql_id': 'str',
                        'first_contact_date': 'str',
                        'landing_page_id': 'str',
                        'origin': 'str'
                    },
                    'leads_closed': {
                        'mql_id': 'str',
                        'seller_id': 'str',
                        'sdr_id': 'str',
                        'sr_id': 'str',
                        'won_date': 'str',
                        'business_segment': 'str',
                        'lead_type': 'str',
                        'lead_behaviour_profile': 'str',
                        'has_company': 'str',
                        'has_gtin': 'str',
                        'average_stock': 'str',
                        'business_type': 'str',
                        'declared_product_catalog_size': 'str',
                        'declared_monthly_revenue': 'float64'
                    },
                    'product_category_name_translation': {
                        'product_category_name': 'str',
                        'product_category_name_english': 'str'
                    }
                }

                # Read CSV with utf-8-sig encoding to handle BOM
                df = pd.read_csv(file.file, chunksize=chunk_size, dtype=dtypes.get(full_table_name, {}), encoding='utf-8-sig')

                # Get table info from database
                cursor.execute(f"PRAGMA table_info({full_table_name})")
                table_info = cursor.fetchall()
                if not table_info:  # Check if table exists
                    raise ValueError(f"Table {full_table_name} does not exist in the database")
                columns = [col[1] for col in table_info]
                
                # Define primary key
                primary_key = {
                    'sellers': 'seller_id',
                    'customers': 'customer_id',
                    'orders': 'order_id',
                    'order_payments': 'order_id',
                    'products': 'product_id',
                    'order_items': 'order_id',
                    'order_reviews': 'review_id',
                    'geolocation': 'geolocation_zip_code_prefix',
                    'leads_qualified': 'mql_id',
                    'leads_closed': 'mql_id',
                    'product_category_name_translation': 'product_category_name'
                }.get(full_table_name, columns[0])

                inserted, skipped = 0, 0

                # Process CSV chunks
                if full_table_name == 'products':
                    for chunk in df:
                        chunk = chunk.rename(columns={
                            'product_name_lenght': 'product_name_length',
                            'product_description_lenght': 'product_description_length'
                        })
                        for _, row in chunk.iterrows():
                            try:
                                cursor.execute(
                                    f"SELECT {primary_key} FROM {full_table_name} WHERE {primary_key} = ?",
                                    (row[primary_key],)
                                )
                                if cursor.fetchone():
                                    skipped += 1
                                    continue
                                placeholders = ", ".join("?" * len(row))
                                columns_str = ", ".join(row.index)
                                cursor.execute(
                                    f"INSERT INTO {full_table_name} ({columns_str}) VALUES ({placeholders})",
                                    tuple(row.values)
                                )
                                inserted += 1
                            except Exception as e:
                                logger.error(f"Error processing row: {row.to_dict()}. Error: {e}")
                                raise
                else:
                    for chunk in df:
                        for _, row in chunk.iterrows():
                            try:
                                cursor.execute(
                                    f"SELECT {primary_key} FROM {full_table_name} WHERE {primary_key} = ?",
                                    (row[primary_key],)
                                )
                                if cursor.fetchone():
                                    skipped += 1
                                    continue
                                placeholders = ", ".join("?" * len(row))
                                columns_str = ", ".join(row.index)
                                cursor.execute(
                                    f"INSERT INTO {full_table_name} ({columns_str}) VALUES ({placeholders})",
                                    tuple(row.values)
                                )
                                inserted += 1
                            except Exception as e:
                                logger.error(f"Error processing row: {row.to_dict()}. Error: {e}")
                                raise

                conn.commit()
                logger.info(f"Inserted {inserted} rows, skipped {skipped} rows into table {full_table_name}")
                
            return {"inserted": inserted, "skipped": skipped}
        
        except Exception as e:
            logger.error(f"Error processing CSV upload for table {table_name}: {e}")
            raise
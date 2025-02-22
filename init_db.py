"""Initialize the SQLite database and create tables."""

import logging
import os
import sqlite3

logger = logging.getLogger(__name__)

DB_PATH = "olist.db"

def init_database():
    """Create the database and tables if they do not exist."""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                customer_unique_id TEXT,
                customer_zip_code_prefix TEXT,
                customer_city TEXT,
                customer_state TEXT
            )
        """)

        # Orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT PRIMARY KEY,
                customer_id TEXT,
                order_status TEXT,
                order_purchase_timestamp TEXT,
                order_approved_at TEXT,
                order_delivered_carrier_date TEXT,
                order_delivered_customer_date TEXT,
                order_estimated_delivery_date TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
            )
        """)

        # Order Items table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_items (
                order_id TEXT,
                order_item_id INTEGER,
                product_id TEXT,
                seller_id TEXT,
                shipping_limit_date TEXT,
                price REAL,
                freight_value REAL,
                PRIMARY KEY (order_id, order_item_id),
                FOREIGN KEY (order_id) REFERENCES orders(order_id),
                FOREIGN KEY (product_id) REFERENCES products(product_id),
                FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
            )
        """)

        # Order Payments table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_payments (
                order_id TEXT,
                payment_sequential INTEGER,
                payment_type TEXT,
                payment_installments INTEGER,
                payment_value REAL,
                PRIMARY KEY (order_id, payment_sequential),
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)

        # Order Reviews table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS order_reviews (
                review_id TEXT PRIMARY KEY,
                order_id TEXT,
                review_score INTEGER,
                review_comment_title TEXT,
                review_comment_message TEXT,
                review_creation_date TEXT,
                review_answer_timestamp TEXT,
                FOREIGN KEY (order_id) REFERENCES orders(order_id)
            )
        """)

        # Products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                product_category_name TEXT,
                product_name_length REAL,
                product_description_length REAL,
                product_photos_qty REAL,
                product_weight_g REAL,
                product_length_cm REAL,
                product_height_cm REAL,
                product_width_cm REAL,
                specifications TEXT
            )
        """)

        # Sellers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sellers (
                seller_id TEXT PRIMARY KEY,
                seller_zip_code_prefix TEXT,
                seller_city TEXT,
                seller_state TEXT
            )
        """)

        # Geolocation table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS geolocation (
                geolocation_zip_code_prefix TEXT PRIMARY KEY,
                geolocation_lat REAL,
                geolocation_lng REAL,
                geolocation_city TEXT,
                geolocation_state TEXT
            )
        """)

        # Leads Qualified table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads_qualified (
                mql_id TEXT PRIMARY KEY,
                first_contact_date TEXT,
                landing_page_id TEXT,
                origin TEXT
            )
        """)

        # Leads Closed table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leads_closed (
                mql_id TEXT PRIMARY KEY,
                seller_id TEXT,
                sdr_id TEXT,
                sr_id TEXT,
                won_date TEXT,
                business_segment TEXT,
                lead_type TEXT,
                lead_behaviour_profile TEXT,
                has_company TEXT,
                has_gtin TEXT,
                average_stock TEXT,
                business_type TEXT,
                declared_product_catalog_size TEXT,
                declared_monthly_revenue REAL,
                FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
            )
        """)

        # Product Category Name Translation table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS product_category_name_translation (
                product_category_name TEXT PRIMARY KEY,
                product_category_name_english TEXT
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Database and tables initialized successfully!")
    else:
        logger.info("Database already exists.")

if __name__ == "__main__":
    init_database()

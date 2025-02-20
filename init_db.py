# init_db.py
import sqlite3
import os

db_path = "olist.db"

if not os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sellers (
            seller_id TEXT PRIMARY KEY,
            seller_zip_code_prefix TEXT NOT NULL,
            seller_city TEXT NOT NULL,
            seller_state TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id TEXT PRIMARY KEY,
            customer_unique_id TEXT NOT NULL,
            customer_zip_code_prefix TEXT NOT NULL,
            customer_city TEXT NOT NULL,
            customer_state TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_id TEXT NOT NULL,
            order_status TEXT NOT NULL,
            order_purchase_timestamp TEXT NOT NULL,
            order_approved_at TEXT,
            order_delivered_carrier_date TEXT,
            order_delivered_customer_date TEXT,
            order_estimated_delivery_date TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_payments (
            order_id TEXT NOT NULL,
            payment_sequential INTEGER NOT NULL,
            payment_type TEXT NOT NULL,
            payment_installments INTEGER NOT NULL,
            payment_value REAL NOT NULL,
            PRIMARY KEY (order_id, payment_sequential),
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
    """)

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
            product_width_cm REAL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            order_id TEXT NOT NULL,
            order_item_id INTEGER NOT NULL,
            product_id TEXT NOT NULL,
            seller_id TEXT NOT NULL,
            shipping_limit_date TEXT,
            price REAL NOT NULL,
            freight_value REAL NOT NULL,
            PRIMARY KEY (order_id, order_item_id),
            FOREIGN KEY (order_id) REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id),
            FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS order_reviews (
            review_id TEXT PRIMARY KEY,
            order_id TEXT NOT NULL,
            review_score INTEGER NOT NULL,
            review_comment_title TEXT,
            review_comment_message TEXT,
            review_creation_date TEXT NOT NULL,
            review_answer_timestamp TEXT,
            FOREIGN KEY (order_id) REFERENCES orders(order_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS geolocation (
            geolocation_zip_code_prefix TEXT PRIMARY KEY,
            geolocation_lat REAL NOT NULL,
            geolocation_lng REAL NOT NULL,
            geolocation_city TEXT NOT NULL,
            geolocation_state TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads_qualified (
            mql_id TEXT PRIMARY KEY,
            first_contact_date TEXT NOT NULL,
            landing_page_id TEXT,
            origin TEXT
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads_closed (
            mql_id TEXT PRIMARY KEY,
            seller_id TEXT NOT NULL,
            sdr_id TEXT,
            sr_id TEXT,
            won_date TEXT NOT NULL,
            business_segment TEXT,
            lead_type TEXT,
            lead_behaviour_profile TEXT,
            has_company TEXT,
            has_gtin TEXT,
            average_stock TEXT,
            business_type TEXT,
            declared_product_catalog_size TEXT,
            declared_monthly_revenue REAL,
            FOREIGN KEY (mql_id) REFERENCES leads_qualified(mql_id),
            FOREIGN KEY (seller_id) REFERENCES sellers(seller_id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_category_name_translation (
            product_category_name TEXT PRIMARY KEY,
            product_category_name_english TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()
    print("Database and tables initialized successfully!")
else:
    print("Database already exists.")
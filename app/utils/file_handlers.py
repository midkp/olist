"""Utilities for handling file operations."""

import csv
import logging

logger = logging.getLogger(__name__)


def validate_csv_structure(table_name: str, file):
    """Validate CSV file structure against required columns."""
    required_columns = {
        "customers": [
            "customer_id",
            "customer_unique_id",
            "customer_zip_code_prefix",
            "customer_city",
            "customer_state",
        ],
        "orders": [
            "order_id",
            "customer_id",
            "order_status",
            "order_purchase_timestamp",
            "order_approved_at",
            "order_delivered_carrier_date",
            "order_delivered_customer_date",
            "order_estimated_delivery_date",
        ],
        "order_items": [
            "order_id",
            "order_item_id",
            "product_id",
            "seller_id",
            "shipping_limit_date",
            "price",
            "freight_value",
        ],
        "order_payments": [
            "order_id",
            "payment_sequential",
            "payment_type",
            "payment_installments",
            "payment_value",
        ],
        "order_reviews": [
            "review_id",
            "order_id",
            "review_score",
            "review_comment_title",
            "review_comment_message",
            "review_creation_date",
            "review_answer_timestamp",
        ],
        "products": [
            "product_id",
            "product_category_name",
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
        "sellers": [
            "seller_id",
            "seller_zip_code_prefix",
            "seller_city",
            "seller_state",
        ],
        "geolocation": [
            "geolocation_zip_code_prefix",
            "geolocation_lat",
            "geolocation_lng",
            "geolocation_city",
            "geolocation_state",
        ],
        "leads_qualified": [
            "mql_id",
            "first_contact_date",
            "landing_page_id",
            "origin",
        ],
        "leads_closed": [
            "mql_id",
            "seller_id",
            "sdr_id",
            "sr_id",
            "won_date",
            "business_segment",
            "lead_type",
            "lead_behaviour_profile",
            "has_company",
            "has_gtin",
            "average_stock",
            "business_type",
            "declared_product_catalog_size",
            "declared_monthly_revenue",
        ],
        "product_category_name_translation": [
            "product_category_name",
            "product_category_name_english",
        ],
    }

    # Read the file content and log it for debugging
    content = file.file.read().decode("utf-8-sig")
    logger.info(f"File content for {table_name}: {content[:100]}...")
    if not content.strip():
        raise ValueError(f"Uploaded file for table {table_name} is empty")

    reader = csv.DictReader(content.splitlines())
    if reader.fieldnames is None:
        raise ValueError(
            f"Uploaded file for table {table_name} has no headers or is not a valid CSV"
        )

    logger.debug(f"Expected columns: {required_columns.get(table_name, [])}")
    logger.debug(f"Actual columns: {reader.fieldnames}")
    if not set(required_columns.get(table_name, [])).issubset(reader.fieldnames):
        raise ValueError(f"CSV structure doesn't match table requirements for {table_name}")

    # Reset file pointer for subsequent reads
    file.file.seek(0)

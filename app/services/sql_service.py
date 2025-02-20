# app/services/sql_service.py
import sqlite3
import pandas as pd
import logging
from openai import OpenAI
from app.core import database

logger = logging.getLogger(__name__)

client = OpenAI(api_key="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")  # Replace with your OpenAI API key

class SQLService:
    @staticmethod
    def get_db_schema(conn):
        """Retrieve table names and schema from the SQLite database."""
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        schema_info = {}
        for table in tables:
            table_name = table[0]
            cursor.execute(f"PRAGMA table_info({table_name})")
            schema_info[table_name] = cursor.fetchall()
        return schema_info

    @staticmethod
    def clean_sql_query(query):
        """Remove markdown formatting from SQL query."""
        query = query.strip()
        if query.startswith("```"):
            query = query[3:]
            if query.lstrip().startswith("sql"):
                query = query.lstrip()[3:]
            query = query.strip()
            if query.endswith("```"):
                query = query[:-3]
        return query.strip()

    @staticmethod
    def generate_sql_query(natural_language_query, schema):
        """Convert natural language query to SQL using OpenAI."""
        schema_text = "\n".join([f"Table {table}: {[(col[1], col[2]) for col in columns]}" for table, columns in schema.items()])
        
        prompt = f"""
        You are an SQL expert. Given the following database schema, convert the user's question into an SQL query.

        {schema_text}

        User Question: {natural_language_query}
        SQL Query:
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Adjust model as needed
            messages=[
                {"role": "system", "content": "You are an AI that generates SQL queries."},
                {"role": "user", "content": prompt}
            ]
        )

        sql_query = response.choices[0].message.content
        return SQLService.clean_sql_query(sql_query)

    @staticmethod
    async def execute_sql_query(natural_language_query):
        """Generate and execute SQL query, return results as JSON."""
        try:
            with database.get_db_connection() as conn:
                # Get database schema
                schema = SQLService.get_db_schema(conn)
                
                # Generate SQL query from natural language
                sql_query = SQLService.generate_sql_query(natural_language_query, schema)
                logger.info(f"Generated SQL Query: {sql_query}")

                # Execute the query and fetch results
                df = pd.read_sql_query(sql_query, conn)
                result = df.to_dict(orient="records")  # Convert DataFrame to list of dictionaries

                return {
                    "status": "success",
                    "query": sql_query,
                    "results": result
                }
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            raise
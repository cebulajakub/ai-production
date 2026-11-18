import os
import pyodbc

connection_string = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    f"SERVER={os.environ['DB_HOST']},{os.environ['DB_PORT']};"
    f"DATABASE={os.environ['DB_NAME']};"
    f"UID={os.environ['DB_USER']};"
    f"PWD={os.environ['DB_PASSWORD']};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)

with pyodbc.connect(connection_string, timeout=5) as connection:
    cursor = connection.cursor()
    cursor.execute("SELECT DB_NAME()")
    database_name = cursor.fetchone()[0]

    print(f"Connected to database: {database_name}")
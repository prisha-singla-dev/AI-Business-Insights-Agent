import os
import pandas as pd
from sqlalchemy import create_engine

# Database connection details
DB_USER = os.getenv("DB_USER", "")  # Replace with your PostgreSQL username
DB_PASSWORD = os.getenv("DB_PASSWORD", "")  # Replace with your PostgreSQL password
DB_HOST = os.getenv("DB_HOST", "") # Replace with your database host
DB_PORT = os.getenv("DB_PORT", "") # Replace with your database port
DB_NAME = os.getenv("DB_NAME", "") # Replace with your PostgreSQL database name


# Create database connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

# Excel file path
excel_file = "your_file_path_of_database"
# Read all sheets from the Excel file
if not os.path.exists(excel_file):
    raise FileNotFoundError(f" Excel file '{excel_file}' not found. Please provide the correct path.")

sheets = pd.ExcelFile(excel_file)


# Define a mapping of sheets to database tables
sheet_to_table = {
    'customer_details': 'customer_details',
    'order_details': 'order_details',
    'payment_details': 'payment_details',
    'product_details': 'product_details',
    'orderitem_details': 'orderitem_details'
}

# Function to load data into PostgreSQL
def load_data(sheet_name, table_name):
    # Read the data from the Excel sheet
    df = pd.read_excel(excel_file, sheet_name=sheet_name)

    # Handle duplicate records before inserting
    if table_name == 'product_details':
        df = df.drop_duplicates(subset=["product_id"])  # Keep unique product_id entries

    elif table_name == 'orderitem_details':
        df = df.drop_duplicates(subset=["order_id", "product_id", "seller_id"])  # Keep unique composite key

    # Insert data into the database table
    try:
        df.to_sql(table_name, engine, if_exists='append', index=False)
        print(f'Data successfully inserted into {table_name}')
    except Exception as e:
        print(f'Error inserting data into {table_name}: {e}')
    
# Import data sheet by sheet
for sheet_name, table_name in sheet_to_table.items():
    if sheet_name in sheets.sheet_names:
        load_data(sheet_name, table_name)
    else:
        print(f'Sheet {sheet_name} not found in Excel file.')

# Close database connection
engine.dispose()



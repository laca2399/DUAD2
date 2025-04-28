from sqlalchemy import create_engine, inspect
from urllib.parse import quote_plus
from datahandler import DB_Manager

# Code the password as it has special characters
password = quote_plus("Lacayo2020!")
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost:5432/postgres")

# Initialize DB_Manager with the engine
db_manager = DB_Manager(engine)

# Validate if tables exist
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

needed_tables = {'users', 'products', 'sales', 'invoices'}

if not needed_tables.issubset(existing_tables):
    print("Tables missing, creating...")
    db_manager.create_all()  # Alternatively, you could call create_all here.
else:
    print("All tables exist.")



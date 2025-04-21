#Realice un script que valide si las tablas existen, y si no las cree en el momento de su ejecución.
from sqlalchemy import create_engine, inspect
from urllib.parse import quote_plus
from tables import metadata

# Code the password as it has special characters
password = quote_plus("Lacayo2020!")
engine = create_engine(f"postgresql+psycopg2://postgres:{password}@localhost:5432/postgres")

# Validate if tables exist
inspector = inspect(engine)
existing_tables = inspector.get_table_names()

needed_tables = {'users', 'addresses', 'cars'}

if not needed_tables.issubset(existing_tables):
    print("Tables missing, creating...")
    metadata.create_all(engine)
else:
    print("All tables exist.")

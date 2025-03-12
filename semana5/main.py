from db import PgManager


db_manager = PgManager(
    db_name="postgres",
    user="postgres",
    password="Lacayo2020!",
    host="localhost"
)

results = db_manager.execute_query("SELECT * FROM users;")
print(results)

db_manager.close_connection()
from db.database import db
from db.models import Base, User, Availability, Product_Category, Cart_Status
from controllers.user_manager import UserDBManager

Base.metadata.drop_all(db.engine)
Base.metadata.create_all(db.engine)

def seed_availability_and_categories():
    with db.Session() as session:
        existing_availabilities = session.query(Availability).count()
        existing_categories = session.query(Product_Category).count()

        if existing_availabilities == 0:
            availabilities = [
                Availability(status="In stock"),
                Availability(status="Out of stock"),
                Availability(status="Pre-order"),
            ]
            session.add_all(availabilities)
            print("✅ Availability data inserted.")

        if existing_categories == 0:
            categories = [
                Product_Category(name="Fruits"),
                Product_Category(name="Vegetables"),
                Product_Category(name="Dairy"),
                Product_Category(name="Bakery"),
            ]
            session.add_all(categories)
            print("✅ Product categories data inserted.")

        session.commit()

def seed_cart_status():
    with db.Session() as session:
        existing_statuses = session.query(Cart_Status).count()
        if existing_statuses == 0:
            statuses = [
                Cart_Status(status="active"),
                Cart_Status(status="completed"),
                Cart_Status(status="cancelled"),
            ]
            session.add_all(statuses)
            print("✅ Cart status data inserted.")
            session.commit()
        else:
            print("ℹ️ Cart statuses already exist.")

def create_default_admin():
    with db.Session() as session:
        admin = session.query(User).filter_by(email='admin@test.com').first()
        if not admin:
            user_manager = UserDBManager()
            user_manager.insert_user(
                email="admin@test.com",
                password="adminpassword",
                name="Admin",
                role="admin",
                session=session
            )
            print("✅ Admin created by default.")
        else:
            print("ℹ️ Admin already exists.")

seed_availability_and_categories()
seed_cart_status()
create_default_admin()

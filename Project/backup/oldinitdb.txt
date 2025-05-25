from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from basemanager import Base
from user_manager import UserDBManager
from models import User

DATABASE_URL = "postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)


Base.metadata.create_all(engine)

def create_default_admin():
    Session = sessionmaker(bind=engine)
    with Session() as session:
        admin = session.query(User).filter_by(username='admin').first()
        if not admin:
            user_manager = UserDBManager(engine)
            user_manager.insert_user(session, "admin", "adminpassword", role="admin")
            print("✅ Admin created by default.")

create_default_admin()
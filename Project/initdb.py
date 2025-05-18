from database import db
from models import Base, User
from user_manager import UserDBManager

Base.metadata.create_all(db.engine)

def create_default_admin():
    with db.Session() as session:
        admin = session.query(User).filter_by(username='admin').first()
        if not admin:
            user_manager = UserDBManager()
            user_manager.insert_user(session, "admin", "adminpassword", role="admin")
            print("✅ Admin created by default.")

create_default_admin()

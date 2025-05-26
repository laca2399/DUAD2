from database import db
from usermanager import UserDBManager
from models import User, Base

Base.metadata.create_all(db.engine)

def create_default_admin():
    with db.Session() as session:
        admin = session.query(User).filter_by(username='admin').first()
        if not admin:
            user_manager = UserDBManager()
            user_manager.insert_user(session, "admin", "adminpassword", role="admin")
            print("✅ Admin created by default.")

create_default_admin()

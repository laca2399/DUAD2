from basemanager import BaseDBManager
from models import User

class UserDBManager(BaseDBManager):
    def insert_user(self, email, password, name, role="client"):
        with self.get_session() as session:
            new_user = User(email=email, password=password, name=name, role=role)
            session.add(new_user)
            session.commit()
            return new_user

    def get_user_by_email(self, email):
        with self.get_session() as session:
            return session.query(User).filter_by(email=email).first()

    def get_user_by_id(self, user_id):
        with self.get_session() as session:
            return session.query(User).filter_by(id=user_id).first()

    def verify_password(self, user, password):
        return user.password == password

    def get_user_role(self, user_id):
        user = self.get_user_by_id(user_id)
        return user.role if user else None
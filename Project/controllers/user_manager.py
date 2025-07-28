from db.basemanager import BaseDBManager
from db.models import User

class UserDBManager(BaseDBManager):

    def _user_to_dict(self, user):
        if not user:
            return None
        return {
            "id": user.id,
            "email": user.email,
            "password": user.password,
            "name": user.name,
            "role": user.role,
        }

    def insert_user(self, email, password, name, role="client", session=None):
        external_session = session is not None
        if not external_session:
            with self.get_session() as session:
                new_user = User(email=email, password=password, name=name, role=role)
                session.add(new_user)
                session.commit()
                session.refresh(new_user)  
                return self._user_to_dict(new_user)
        else:
            new_user = User(email=email, password=password, name=name, role=role)
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return self._user_to_dict(new_user)
    

    def get_user_by_email(self, email):
        with self.get_session() as session:
            user = session.query(User).filter_by(email=email).first()
            return self._user_to_dict(user) if user else None

    def get_user_by_id(self, user_id):
        with self.get_session() as session:
            user = session.query(User).filter_by(id=user_id).first()
            return self._user_to_dict(user) if user else None

    def verify_password(self, user, password):
        return user and user.get('password') == password


    def get_user_role(self, user_id):
        user = self.get_user_by_id(user_id)
        return user.get('role') if user else None
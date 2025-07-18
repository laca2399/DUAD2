from database import db
from models import Base

class BaseDBManager:
    def __init__(self):
        self.Session = db.Session

    def get_session(self):
        return self.Session()

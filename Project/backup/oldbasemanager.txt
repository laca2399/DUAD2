from sqlalchemy.orm import sessionmaker

class BaseDBManager:
    def __init__(self, engine):
        self.engine = engine
        self.Session = sessionmaker(bind=engine)

    def get_session(self):
        return self.Session()
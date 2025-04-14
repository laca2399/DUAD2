#Punto 4: 4. Cree una serie de clases para manejo de datos (una para usuarios, otra para automoviles y 
# otra para direcciones) donde implemente funciones que realicen las siguientes tareas:
    #1. Crear/Modificar/Eliminar un usuario nuevo.
    #2. Crear/Modificar/Eliminar un automóvil nuevo.
    #3. Crear/Modificar/Eliminar una dirección nueva.
    #4. Asociar un automóvil a un usuario.
    #5. Consultar todos los usuarios.
    #6. Consultar todos los automóviles.
    #7. Consultar todas las direcciones.
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"  # Muestra el id y el nombre del usuario
    
    def create_user(self):
        session.add(self)
        session.commit()
    
    def update_user(self, new_name):
        self.name = new_name
        session.commit()

    def delete_user(self):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()


class Address(Base):
    __tablename__ = 'addresses'
    id = Column(Integer, primary_key=True)
    street = Column(String)
    city = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, street, city, user_id):
        self.street = street
        self.city = city
        self.user_id = user_id

    def __repr__(self):
        return f"<Address(id={self.id}, street={self.street}, city={self.city}, user_id={self.user_id})>"  # Muestra la dirección, ciudad y el ID del usuario asociado
    
    def create_address(self):
        session.add(self)
        session.commit()

    def update_address(self, new_street, new_city):
        self.street = new_street
        self.city = new_city
        session.commit()

    def delete_address(self):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()


class Car(Base):
    __tablename__ = 'cars'
    id = Column(Integer, primary_key=True)
    branch = Column(String)
    model = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)

    def __init__(self, branch, model, user_id=None):
        self.branch = branch
        self.model = model
        self.user_id = user_id

    def __repr__(self):
        return f"<Car(id={self.id}, branch={self.branch}, model={self.model}, user_id={self.user_id})>"  # Muestra la marca, modelo y el ID del usuario asociado
    
    def create_car(self):
        session.add(self)
        session.commit()

    def update_car(self, new_branch, new_model):
        self.branch = new_branch
        self.model = new_model
        session.commit()

    def delete_car(self):
        session.delete(self)
        session.commit()

    @classmethod
    def get_all(cls):
        return session.query(cls).all()

    def assign_user(self, user_id):
        self.user_id = user_id
        session.commit()

# Setup engine and session
engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

# Crete tables if not exist
Base.metadata.create_all(engine)
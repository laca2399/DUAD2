#Punto 2: Plantee una DB con tablas para usuarios, direcciones y automóviles.
    #1. Tanto las direcciones como los automóviles deben tener FKs que apunten a los usuarios.
    #2. Los automoviles pueden no tener usuarios asociados, pero todas las direcciones deben tener un usuario asociado.
from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String)
)

addresses = Table(
    'addresses',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('street', String),
    Column('city', String),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False)
)

cars = Table(
    'cars',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('branch', String),
    Column('model', String),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=True)
)

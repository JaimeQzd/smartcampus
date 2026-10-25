import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#Busco obtener la direccion de la base de datos desde la variable creada
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./smartcampus.db",
)


#Configuracion de sqlite
connect_args = {}

if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}


#Establexco el motor de conexion entre SQl y la base de datos 
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
)


#Permito la creacion de sesiones para realizar operaciones 
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


#La base para los modelos 
class Base(DeclarativeBase):
    pass

#Se crea una base de datos cada vez que se necesita, cunado no se la necesita se cierra
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
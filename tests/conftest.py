import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app


#Establecemos la base de datos con la que realizaremos las pruebas 
TEST_DATABASE_URL = "sqlite:///./test_smartcampus.db"


#Nos conectamos a nuestra base de datos de prueba 
test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Creamos las sesiones a usar en nuestros test
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


#sustituimos la base de datos por la que usaremos para las pruebas 
def override_get_db():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


#Establecemos el uso de la conexion de pruebas 
app.dependency_overrides[get_db] = override_get_db


#Para que los test no dependan de otros, se deja la base de datos limpia.
@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)

#Sesion de bd para los test unitarios
@pytest.fixture
def db_session():
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()

#creamos un cliente para realizar peticiones HTTP
@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client
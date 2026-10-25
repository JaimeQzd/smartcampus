import pytest
from pydantic import ValidationError

from app import schemas, services

#datos de ejemplo para los tests unitarios
ROOM_DATA = {
    "nombre": "Laboratorio de Informática",
    "edificio": "Edificio C",
    "capacidad": 25,
    "equipamiento": [
        "ordenadores",
        "proyector",
    ],
}


#comprobamos la funcion que crea aulas
def test_service_create_room(db_session):
    #creamos el esquema con los datos del aula
    room_data = schemas.RoomCreate(**ROOM_DATA)

    #llamamos a la funcion de services.py
    room = services.create_room(
        db=db_session,
        room=room_data,
    )

    #comprobamos que los datos se hayan guardado correctamente
    assert room.id is not None
    assert room.nombre == "Laboratorio de Informática"
    assert room.edificio == "Edificio C"
    assert room.capacidad == 25


#comprobamos la funcion que obtiene las aulas
def test_service_get_rooms(db_session):
    room_data = schemas.RoomCreate(**ROOM_DATA)

    #creamos un aula
    services.create_room(
        db=db_session,
        room=room_data,
    )

    #obtenemos las aulas
    rooms = services.get_rooms(db_session)

    assert len(rooms) == 1
    assert rooms[0].nombre == "Laboratorio de Informática"


#comprobamos la busqueda de un aula por su id
def test_service_get_room_by_id(db_session):
    room_data = schemas.RoomCreate(**ROOM_DATA)

    #creamos el aula
    created_room = services.create_room(
        db=db_session,
        room=room_data,
    )

    #buscamos el aula por su id
    room = services.get_room_by_id(
        db=db_session,
        room_id=created_room.id,
    )

    assert room is not None
    assert room.id == created_room.id
    assert room.nombre == "Laboratorio de Informática"


#comprobamos la eliminacion de un aula
def test_service_delete_room(db_session):
    room_data = schemas.RoomCreate(**ROOM_DATA)

    #creamos el aula
    created_room = services.create_room(
        db=db_session,
        room=room_data,
    )

    room_id = created_room.id

    #eliminamos el aula
    services.delete_room(
        db=db_session,
        room=created_room,
    )

    #intentamos buscar el aula de nuevo
    room = services.get_room_by_id(
        db=db_session,
        room_id=room_id,
    )

    assert room is None


#comprobamos la validacion de capacidad
def test_room_invalid_capacity():
    #Pydantic lanzaa un error si capacidad es 0
    with pytest.raises(ValidationError):
        schemas.RoomCreate(
            nombre="Aula inválida",
            edificio="Edificio D",
            capacidad=0,
            equipamiento=[],
        )
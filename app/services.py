from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


#creamos un aula y la guardamos en la BD
def create_room(
    db: Session,
    room: schemas.RoomCreate,
):
    #creamos el modelo Room con los datos recibidos
    new_room = models.Room(
        nombre=room.nombre,
        edificio=room.edificio,
        capacidad=room.capacidad,
        equipamiento=room.equipamiento,
    )

    #añadimos el aula a la BD
    db.add(new_room)

    #guardamos los cambios
    db.commit()

    #actualizamos el objeto para obtener lod datos
    db.refresh(new_room)

    return new_room


#obtenemos todas las aulas de la BD
def get_rooms(db: Session):
    #preparamos la consulta
    statement = select(models.Room)

    #ejecutamos la consulta de todas las aulas
    rooms = db.scalars(statement).all()

    return rooms


#buscamos un aula concreta con id
def get_room_by_id(
    db: Session,
    room_id: int,
):
    room = db.get(models.Room, room_id)

    return room


#eliminamos un aula de la BD
def delete_room(
    db: Session,
    room: models.Room,
):
    #eliminamos el aula
    db.delete(room)

    #guardamos  el cambio
    db.commit()
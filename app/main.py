#importamos desde fastapi nuestra FastAPI
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

#importamos los modelos, esquemas y la conexion con la base de datos
from app import models, schemas
from app.database import engine, get_db


#SQLAlchemy revisa los modelos definidos en models.py
#y crea las tablas que todavia no existan
models.Base.metadata.create_all(bind=engine)


#creamos la aplicacion FastAPI
app = FastAPI(
    title="SmartCampus API",
    description="API para la gestión de aulas y reservas universitarias",
    version="1.0.0",
)


#comprobamos si la aplicacion esta activa
@app.get("/health")
def health():
    return {"status": "ok"}


#creamos una nueva aula
#recibimos los datos mediante RoomCreate
@app.post(
    "/rooms",
    response_model=schemas.RoomResponse,
    status_code=201,
)
def create_room(
    room: schemas.RoomCreate,
    db: Session = Depends(get_db),
):
    #creamos un objeto Room con los datos recibidos
    new_room = models.Room(
        nombre=room.nombre,
        edificio=room.edificio,
        capacidad=room.capacidad,
        equipamiento=room.equipamiento,
    )

    #añadimos el aula
    db.add(new_room)
    #guardamos los cambios
    db.commit()
    #actualizamos el objeto
    db.refresh(new_room)
    return new_room


#consultamos todas las aulas existentes
@app.get(
    "/rooms",
    response_model=list[schemas.RoomResponse],
)
def get_rooms(
    db: Session = Depends(get_db),
):
    #preparamos una consulta que selecciona todas las aulas
    statement = select(models.Room)
    #ejecutamos la consulta y obtenemos los resultados
    rooms = db.scalars(statement).all()
    return rooms


#consultamos un aula con el id
@app.get(
    "/rooms/{room_id}",
    response_model=schemas.RoomResponse,
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    #buscamos el aula por id
    room = db.get(models.Room, room_id)
    #si el aula no existe devolvemos un error 404
    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    return room


#eliminamos un aula por su id
@app.delete(
    "/rooms/{room_id}",
    status_code=204,
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    #buscamos el aula que queremos eliminar
    room = db.get(models.Room, room_id)
    #si el aula no existe devolvemos un error 404
    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    #eliminamos el aula 
    db.delete(room)
    #guardamos  los cambios
    db.commit()

    return None
#importamos desde fastapi nuestra FastAPI
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

#importamos los modelos, esquemas, servicios y la conexion con la base de datos
from app import models, schemas, services
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
@app.post(
    "/rooms",
    response_model=schemas.RoomResponse,
    status_code=201,
)
def create_room(
    room: schemas.RoomCreate,
    db: Session = Depends(get_db),
):
    #utilizamos services.py para crear y guardar el aula
    new_room = services.create_room(
        db=db,
        room=room,
    )

    #devolvemos el aula creada
    return new_room


#consultamos todas las aulas existentes
@app.get(
    "/rooms",
    response_model=list[schemas.RoomResponse],
)
def get_rooms(
    db: Session = Depends(get_db),
):
    #utilizamos services.py para obtener todas las aulas
    rooms = services.get_rooms(db)

    return rooms


#consultamos un aula mediante su id
@app.get(
    "/rooms/{room_id}",
    response_model=schemas.RoomResponse,
)
def get_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    #buscamos el aula mediante services.py
    room = services.get_room_by_id(
        db=db,
        room_id=room_id,
    )

    #si el aula no existe devolvemos un error 404
    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    #si existe devolvemos sus datos
    return room


#eliminamos un aula mediante su id
@app.delete(
    "/rooms/{room_id}",
    status_code=204,
)
def delete_room(
    room_id: int,
    db: Session = Depends(get_db),
):
    #buscamos primero el aula que queremos eliminar
    room = services.get_room_by_id(
        db=db,
        room_id=room_id,
    )

    #si el aula no existe devolvemos un error 404
    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    #utilizamos services.py para eliminar el aula
    services.delete_room(
        db=db,
        room=room,
    )

    return None
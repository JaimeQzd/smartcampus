from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas, services
from app.database import engine, get_db


# SQLAlchemy crea las tablas que todavia no existan
models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SmartCampus API",
    description="API para la gestión de aulas y reservas universitarias",
    version="1.0.0",
)


# tipo reutilizable para obtener una sesion de base de datos
DbSession = Annotated[Session, Depends(get_db)]


# comprobamos si la aplicacion esta activa
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# ENDPOINTS DE AULAS
# -------------------------

@app.post(
    "/rooms",
    response_model=schemas.RoomResponse,
    status_code=201,
)
def create_room(
    room: schemas.RoomCreate,
    db: DbSession,
):
    return services.create_room(
        db=db,
        room=room,
    )


@app.get(
    "/rooms",
    response_model=list[schemas.RoomResponse],
)
def get_rooms(
    db: DbSession,
):
    return services.get_rooms(db)


@app.get(
    "/rooms/{room_id}",
    response_model=schemas.RoomResponse,
)
def get_room(
    room_id: int,
    db: DbSession,
):
    room = services.get_room_by_id(
        db=db,
        room_id=room_id,
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    return room


@app.delete(
    "/rooms/{room_id}",
    status_code=204,
)
def delete_room(
    room_id: int,
    db: DbSession,
):
    room = services.get_room_by_id(
        db=db,
        room_id=room_id,
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    services.delete_room(
        db=db,
        room=room,
    )


# -------------------------
# ENDPOINTS DE RESERVAS
# -------------------------

@app.get(
    "/bookings",
    response_model=list[schemas.BookingResponse],
)
def get_bookings(
    db: DbSession,
):
    return services.get_bookings(db)


@app.post(
    "/bookings",
    response_model=schemas.BookingResponse,
    status_code=201,
)
def create_booking(
    booking: schemas.BookingCreate,
    db: DbSession,
):
    # no se puede reservar un aula inexistente
    room = services.get_room_by_id(
        db=db,
        room_id=booking.aula_id,
    )

    if room is None:
        raise HTTPException(
            status_code=404,
            detail="Aula no encontrada",
        )

    # la hora de inicio debe ser anterior a la hora de fin
    if not services.is_valid_time_range(
        booking.hora_inicio,
        booking.hora_fin,
    ):
        raise HTTPException(
            status_code=400,
            detail="La hora de inicio debe ser anterior a la hora de fin",
        )

    # no permitimos reservas solapadas
    if services.has_booking_overlap(
        db=db,
        booking=booking,
    ):
        raise HTTPException(
            status_code=409,
            detail="La reserva se solapa con otra reserva existente",
        )

    return services.create_booking(
        db=db,
        booking=booking,
    )


@app.delete(
    "/bookings/{booking_id}",
    status_code=204,
)
def delete_booking(
    booking_id: int,
    db: DbSession,
):
    booking = services.get_booking_by_id(
        db=db,
        booking_id=booking_id,
    )

    if booking is None:
        raise HTTPException(
            status_code=404,
            detail="Reserva no encontrada",
        )

    services.delete_booking(
        db=db,
        booking=booking,
    )
from datetime import time

from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas


# -------------------------
# SERVICIOS DE AULAS
# -------------------------

def create_room(
    db: Session,
    room: schemas.RoomCreate,
):
    new_room = models.Room(
        nombre=room.nombre,
        edificio=room.edificio,
        capacidad=room.capacidad,
        equipamiento=room.equipamiento,
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    return new_room


def get_rooms(db: Session):
    statement = select(models.Room)
    return db.scalars(statement).all()


def get_room_by_id(
    db: Session,
    room_id: int,
):
    return db.get(models.Room, room_id)


def delete_room(
    db: Session,
    room: models.Room,
):
    db.delete(room)
    db.commit()


# -------------------------
# SERVICIOS DE RESERVAS
# -------------------------

# comprobamos que la hora de inicio sea anterior a la hora de fin
def is_valid_time_range(
    hora_inicio: time,
    hora_fin: time,
) -> bool:
    return hora_inicio < hora_fin


# comprobamos si dos intervalos horarios se solapan
def bookings_overlap(
    inicio_1: time,
    fin_1: time,
    inicio_2: time,
    fin_2: time,
) -> bool:
    return inicio_1 < fin_2 and fin_1 > inicio_2


# comprobamos si ya existe una reserva que se solape
# para la misma aula y la misma fecha
def has_booking_overlap(
    db: Session,
    booking: schemas.BookingCreate,
) -> bool:
    statement = select(models.Booking).where(
        models.Booking.aula_id == booking.aula_id,
        models.Booking.fecha == booking.fecha,
    )

    existing_bookings = db.scalars(statement).all()

    return any(
        bookings_overlap(
            booking.hora_inicio,
            booking.hora_fin,
            existing.hora_inicio,
            existing.hora_fin,
        )
        for existing in existing_bookings
    )


# creamos una reserva
def create_booking(
    db: Session,
    booking: schemas.BookingCreate,
):
    new_booking = models.Booking(
        aula_id=booking.aula_id,
        usuario=booking.usuario,
        fecha=booking.fecha,
        hora_inicio=booking.hora_inicio,
        hora_fin=booking.hora_fin,
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)

    return new_booking


# obtenemos todas las reservas
def get_bookings(db: Session):
    statement = select(models.Booking)
    return db.scalars(statement).all()


# buscamos una reserva concreta mediante su id
def get_booking_by_id(
    db: Session,
    booking_id: int,
):
    return db.get(models.Booking, booking_id)


# eliminamos una reserva
def delete_booking(
    db: Session,
    booking: models.Booking,
):
    db.delete(booking)
    db.commit()
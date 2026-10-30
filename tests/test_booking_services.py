from datetime import date, time

from app import schemas, services


# comprobamos un intervalo horario valido
def test_valid_time_range():
    assert services.is_valid_time_range(
        time(10, 0),
        time(12, 0),
    )


# comprobamos un intervalo horario invalido
def test_invalid_time_range():
    assert not services.is_valid_time_range(
        time(13, 0),
        time(12, 0),
    )


# comprobamos la funcion pura de solapamiento
def test_bookings_overlap():
    assert services.bookings_overlap(
        time(10, 0),
        time(12, 0),
        time(11, 0),
        time(13, 0),
    )


# reservas consecutivas no se solapan
def test_bookings_do_not_overlap_when_adjacent():
    assert not services.bookings_overlap(
        time(10, 0),
        time(12, 0),
        time(12, 0),
        time(13, 0),
    )


# comprobamos directamente la creacion de una reserva
def test_service_create_booking(db_session):
    room = schemas.RoomCreate(
        nombre="Aula Unit Test",
        edificio="Edificio U",
        capacidad=25,
        equipamiento=[],
    )

    created_room = services.create_room(
        db=db_session,
        room=room,
    )

    booking = schemas.BookingCreate(
        aula_id=created_room.id,
        usuario="alumno1",
        fecha=date(2026, 11, 10),
        hora_inicio=time(10, 0),
        hora_fin=time(12, 0),
    )

    created_booking = services.create_booking(
        db=db_session,
        booking=booking,
    )

    assert created_booking.id is not None
    assert created_booking.aula_id == created_room.id


# comprobamos la deteccion de solapamiento usando la base de datos
def test_service_detects_overlap(db_session):
    room = schemas.RoomCreate(
        nombre="Aula Overlap",
        edificio="Edificio U",
        capacidad=25,
        equipamiento=[],
    )

    created_room = services.create_room(
        db=db_session,
        room=room,
    )

    first_booking = schemas.BookingCreate(
        aula_id=created_room.id,
        usuario="alumno1",
        fecha=date(2026, 11, 10),
        hora_inicio=time(10, 0),
        hora_fin=time(12, 0),
    )

    services.create_booking(
        db=db_session,
        booking=first_booking,
    )

    second_booking = schemas.BookingCreate(
        aula_id=created_room.id,
        usuario="alumno2",
        fecha=date(2026, 11, 10),
        hora_inicio=time(11, 0),
        hora_fin=time(13, 0),
    )

    assert services.has_booking_overlap(
        db=db_session,
        booking=second_booking,
    )


# comprobamos directamente la eliminacion de una reserva
def test_service_delete_booking(db_session):
    room = schemas.RoomCreate(
        nombre="Aula Delete",
        edificio="Edificio U",
        capacidad=25,
        equipamiento=[],
    )

    created_room = services.create_room(
        db=db_session,
        room=room,
    )

    booking = schemas.BookingCreate(
        aula_id=created_room.id,
        usuario="alumno1",
        fecha=date(2026, 11, 10),
        hora_inicio=time(10, 0),
        hora_fin=time(12, 0),
    )

    created_booking = services.create_booking(
        db=db_session,
        booking=booking,
    )

    booking_id = created_booking.id

    services.delete_booking(
        db=db_session,
        booking=created_booking,
    )

    assert services.get_booking_by_id(
        db=db_session,
        booking_id=booking_id,
    ) is None
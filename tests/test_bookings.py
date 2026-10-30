# datos base de un aula para poder crear reservas
ROOM_DATA = {
    "nombre": "Aula de Tests",
    "edificio": "Edificio T",
    "capacidad": 30,
    "equipamiento": ["proyector"],
}


def create_room(client):
    response = client.post(
        "/rooms",
        json=ROOM_DATA,
    )
    return response.json()["id"]


def booking_payload(room_id):
    return {
        "aula_id": room_id,
        "usuario": "alumno1",
        "fecha": "2026-11-10",
        "hora_inicio": "10:00:00",
        "hora_fin": "12:00:00",
    }


# comprobamos que se pueda crear una reserva
def test_create_booking(client):
    room_id = create_room(client)

    response = client.post(
        "/bookings",
        json=booking_payload(room_id),
    )

    assert response.status_code == 201
    assert response.json()["aula_id"] == room_id
    assert response.json()["usuario"] == "alumno1"


# comprobamos que se puedan consultar las reservas
def test_get_bookings(client):
    room_id = create_room(client)

    client.post(
        "/bookings",
        json=booking_payload(room_id),
    )

    response = client.get("/bookings")

    assert response.status_code == 200
    assert len(response.json()) == 1


# no se puede reservar un aula inexistente
def test_booking_nonexistent_room(client):
    payload = booking_payload(999)

    response = client.post(
        "/bookings",
        json=payload,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Aula no encontrada"
    }


# la hora de inicio debe ser anterior a la hora de fin
def test_booking_invalid_time(client):
    room_id = create_room(client)

    payload = booking_payload(room_id)
    payload["hora_inicio"] = "13:00:00"
    payload["hora_fin"] = "12:00:00"

    response = client.post(
        "/bookings",
        json=payload,
    )

    assert response.status_code == 400


# no se permiten reservas solapadas
def test_overlapping_booking(client):
    room_id = create_room(client)

    client.post(
        "/bookings",
        json=booking_payload(room_id),
    )

    second_booking = booking_payload(room_id)
    second_booking["usuario"] = "alumno2"
    second_booking["hora_inicio"] = "11:00:00"
    second_booking["hora_fin"] = "13:00:00"

    response = client.post(
        "/bookings",
        json=second_booking,
    )

    assert response.status_code == 409


# dos reservas consecutivas no se consideran solapadas
def test_adjacent_booking_is_allowed(client):
    room_id = create_room(client)

    client.post(
        "/bookings",
        json=booking_payload(room_id),
    )

    second_booking = booking_payload(room_id)
    second_booking["usuario"] = "alumno2"
    second_booking["hora_inicio"] = "12:00:00"
    second_booking["hora_fin"] = "13:00:00"

    response = client.post(
        "/bookings",
        json=second_booking,
    )

    assert response.status_code == 201


# comprobamos que se pueda eliminar una reserva
def test_delete_booking(client):
    room_id = create_room(client)

    create_response = client.post(
        "/bookings",
        json=booking_payload(room_id),
    )

    booking_id = create_response.json()["id"]

    response = client.delete(
        f"/bookings/{booking_id}"
    )

    assert response.status_code == 204
    assert client.get("/bookings").json() == []


# error al eliminar una reserva inexistente
def test_delete_nonexistent_booking(client):
    response = client.delete("/bookings/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Reserva no encontrada"
    }
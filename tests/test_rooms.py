#datos de ejemplo para los tests
ROOM_DATA = {
    "nombre": "Laboratorio de Robótica",
    "edificio": "Edificio A",
    "capacidad": 30,
    "equipamiento": [
        "ordenadores",
        "robots",
        "impresora 3D",
    ],
}


#se comprueba la correcta creacion del aula
def test_create_room(client):
    response = client.post(
        "/rooms",
        json=ROOM_DATA,
    )

    #comprobamos que el codigo HTTP sea 201 Created
    assert response.status_code == 201

    #guardamos la respuesta en formato JSON
    data = response.json()

    #comprobamos que los datos devueltos sean correctos
    assert data["nombre"] == "Laboratorio de Robótica"
    assert data["edificio"] == "Edificio A"
    assert data["capacidad"] == 30
    assert data["id"] is not None


#comprobamos que no se pueda crear un aula con capacidad 0
def test_create_room_invalid_capacity(client):
    invalid_room = {
        "nombre": "Aula incorrecta",
        "edificio": "Edificio B",
        "capacidad": 0,
        "equipamiento": [],
    }

    response = client.post(
        "/rooms",
        json=invalid_room,
    )

    #FastAPI debe rechazar la peticion
    assert response.status_code == 422


#comprobamos que podemos consultar todas las aulas
def test_get_rooms(client):
    #primero creamos un aula
    client.post(
        "/rooms",
        json=ROOM_DATA,
    )

    #consultamos todas las aulas
    response = client.get("/rooms")

    assert response.status_code == 200

    rooms = response.json()

    #debe existir solamente el aula que acabamos de crear
    assert len(rooms) == 1
    assert rooms[0]["nombre"] == "Laboratorio de Robótica"


#comprobamos que podemos consultar un aula con id
def test_get_room_by_id(client):
    #creamos primero el aula
    create_response = client.post(
        "/rooms",
        json=ROOM_DATA,
    )

    #obtenemos el id generado por la base de datos
    room_id = create_response.json()["id"]

    #consultamos el aula con ese id
    response = client.get(
        f"/rooms/{room_id}"
    )

    assert response.status_code == 200
    assert response.json()["id"] == room_id


#comprobamos el error al consultar un aula inexistente
def test_get_nonexistent_room(client):
    response = client.get("/rooms/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Aula no encontrada"
    }


#comprobamos que podemos eliminar un aula 
def test_delete_room(client):
    #creamos primero un aula
    create_response = client.post(
        "/rooms",
        json=ROOM_DATA,
    )

    room_id = create_response.json()["id"]

    #eliminamos el aula creada
    delete_response = client.delete(
        f"/rooms/{room_id}"
    )

    assert delete_response.status_code == 204

    #comprobamos que el aula ya no existe
    get_response = client.get(
        f"/rooms/{room_id}"
    )

    assert get_response.status_code == 404


#comprobamos el error al eliminar un aula inexistente
def test_delete_nonexistent_room(client):
    response = client.delete("/rooms/999")

    assert response.status_code == 404

    assert response.json() == {
        "detail": "Aula no encontrada"
    }
#comprobamos que el endpoint de salud funciona 
def test_health(client):
    #se hace una peticion GET al endpoint /health
    response = client.get("/health")

    #comprobamos que la respuesta tenga codigo 200
    assert response.status_code == 200

    #comprobamos  que el contenido sea el que esperamos
    assert response.json() == {"status": "ok"}
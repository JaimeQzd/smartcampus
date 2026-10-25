## Tests

El proyecto utiliza Pytest para ejecutar pruebas automáticas.

Se han implementado tests unitarios y tests de integración.

### Tests de integración

Los tests de integración comprueban los endpoints HTTP de la aplicación:

- `GET /health`
- `POST /rooms`
- `GET /rooms`
- `GET /rooms/{id}`
- `DELETE /rooms/{id}`

También se comprueban casos de error como:

- Capacidad igual o menor que 0.
- Consulta de un aula inexistente.
- Eliminación de un aula inexistente.

### Tests unitarios

Los tests unitarios comprueban directamente las funciones de `services.py`, incluyendo:

- Creación de aulas.
- Consulta de aulas.
- Consulta por ID.
- Eliminación de aulas.
- Validación de capacidad.

Para ejecutar todos los tests, dentro del proyecyo, en la terminal ejecutamos:

python -m pytest -v

Los 13 test comprobamos se ejecutan de manera correcta.
from pydantic import BaseModel, ConfigDict, Field

# Definimos los datos que el usuario debe enviar
class RoomCreate(BaseModel):
    nombre: str
    edificio: str

    # Establecemos que nuestra capacidad no puede ser menor o igual a 0
    capacidad: int = Field(gt=0)
    equipamiento: list[str] = []


# Datos que devolverá la API.
class RoomResponse(RoomCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)
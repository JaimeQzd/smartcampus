from sqlalchemy import JSON, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# Representamos esta clase como la tabla dentro de nuestra base de datos.
class Room(Base):
    __tablename__ = "rooms"

    #Establecemos un identificador generado por la base de datos para cada aula
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Nombre del aula.
    nombre: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Edificio del aula.
    edificio: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    # Número máximo de personas por aula.
    capacidad: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Lista con el equipamiento en el aula.
    equipamiento: Mapped[list[str]] = mapped_column(
        JSON,
        default=list,
    )
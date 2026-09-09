from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class Editorial(BaseModel):
    """Modelo representativo de una casa editorial (modelo anidado para B10)."""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre de la editorial")
    pais: str = Field(..., min_length=1, max_length=60, description="País de origen")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Editorial Sudamericana",
                "pais": "Argentina",
            }
        }
    )


class Autor(BaseModel):
    """Modelo representativo del recurso Autor (recurso secundario para B9)."""
    nombre: str = Field(..., min_length=1, max_length=120, description="Nombre y apellido del autor")
    nacionalidad: str = Field(..., min_length=1, max_length=60, description="Nacionalidad del autor")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "nombre": "Jorge Luis Borges",
                "nacionalidad": "Argentina",
            }
        }
    )


class LibroBase(BaseModel):
    """Esquema base con atributos comunes para el recurso Libro."""
    titulo: str = Field(..., min_length=1, max_length=150, description="Título único de la obra")
    paginas: int = Field(
        ...,
        gt=0,
        description="Cantidad de páginas del libro. Debe ser un entero estrictamente mayor a 0 (Ejercicio B8)."
    )
    autor: Optional[str] = Field(None, max_length=120, description="Nombre del autor")
    disponible: bool = Field(
        True,
        description="Indica si el ejemplar se encuentra disponible para préstamo (Ejercicio B12)."
    )
    editorial: Optional[Editorial] = Field(
        None,
        description="Información anidada de la editorial (Ejercicio B10)."
    )


class LibroCreate(LibroBase):
    """Esquema para creación de nuevos libros vía POST."""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "titulo": "Ficciones",
                "paginas": 220,
                "autor": "Jorge Luis Borges",
                "disponible": True,
                "editorial": {
                    "nombre": "Sur",
                    "pais": "Argentina",
                },
            }
        }
    )


class LibroUpdate(BaseModel):
    """Esquema para actualización completa o reemplazo de libros vía PUT."""
    titulo: str = Field(..., min_length=1, max_length=150)
    paginas: int = Field(..., gt=0)
    autor: Optional[str] = None
    disponible: bool = True
    editorial: Optional[Editorial] = None


class Libro(LibroBase):
    """Esquema de representación pública del libro devuelto por la API (response_model)."""
    pass

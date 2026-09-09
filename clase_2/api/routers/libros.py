from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status

from clase_2.api.models import Libro, LibroCreate, LibroUpdate, Editorial

router = APIRouter(
    prefix="/libros",
    tags=["Libros"],
)

# Base de datos en memoria para propósitos pedagógicos
_LIBROS_DB_INICIAL: List[Libro] = [
    Libro(
        titulo="Ficciones",
        paginas=220,
        autor="Jorge Luis Borges",
        disponible=True,
        editorial=Editorial(nombre="Sur", pais="Argentina"),
    ),
    Libro(
        titulo="El Aleph",
        paginas=180,
        autor="Jorge Luis Borges",
        disponible=True,
        editorial=Editorial(nombre="Losada", pais="Argentina"),
    ),
    Libro(
        titulo="Rayuela",
        paginas=600,
        autor="Julio Cortázar",
        disponible=False,
        editorial=Editorial(nombre="Sudamericana", pais="Argentina"),
    ),
]

libros_db: List[Libro] = [libro.model_copy() for libro in _LIBROS_DB_INICIAL]


def reiniciar_db_libros() -> None:
    """Restaura la base de datos en memoria a su estado inicial para tests."""
    global libros_db
    libros_db.clear()
    libros_db.extend([libro.model_copy() for libro in _LIBROS_DB_INICIAL])


@router.get(
    "",
    response_model=List[Libro],
    summary="Listar todos los libros con filtro opcional de páginas",
    status_code=status.HTTP_200_OK,
)
def listar_libros(
    paginas_min: Optional[int] = Query(
        None,
        ge=0,
        description="Filtro opcional: retorna solo libros con al menos esta cantidad de páginas (Ejercicio B11)."
    )
) -> List[Libro]:
    """Retorna la colección completa de libros o aquellos que cumplan con paginas_min."""
    if paginas_min is not None:
        return [libro for libro in libros_db if libro.paginas >= paginas_min]
    return libros_db


@router.post(
    "",
    response_model=Libro,
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo libro",
)
def crear_libro(libro_in: LibroCreate) -> Libro:
    """Crea y almacena un nuevo libro validando su esquema."""
    for existente in libros_db:
        if existente.titulo.strip().lower() == libro_in.titulo.strip().lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ya existe un libro registrado con el título '{libro_in.titulo}'."
            )

    nuevo_libro = Libro(**libro_in.model_dump())
    libros_db.append(nuevo_libro)
    return nuevo_libro


@router.get(
    "/{titulo}",
    response_model=Libro,
    summary="Buscar un libro específico por su título",
    status_code=status.HTTP_200_OK,
)
def obtener_libro(titulo: str) -> Libro:
    """Busca y retorna un libro por su título o arroja 404 Not Found."""
    titulo_limpio = titulo.strip().lower()
    for libro in libros_db:
        if libro.titulo.strip().lower() == titulo_limpio:
            return libro

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se encontró el libro con título '{titulo}'."
    )


@router.put(
    "/{titulo}",
    response_model=Libro,
    summary="Reemplazar completamente un libro existente",
    status_code=status.HTTP_200_OK,
)
def actualizar_libro(titulo: str, libro_in: LibroUpdate) -> Libro:
    """Reemplaza los datos de un libro existente o arroja 404 si no existe."""
    titulo_limpio = titulo.strip().lower()
    for idx, libro in enumerate(libros_db):
        if libro.titulo.strip().lower() == titulo_limpio:
            libro_actualizado = Libro(**libro_in.model_dump())
            libros_db[idx] = libro_actualizado
            return libro_actualizado

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se puede actualizar. El libro '{titulo}' no existe."
    )


@router.delete(
    "/{titulo}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un libro por su título",
)
def borrar_libro(titulo: str) -> None:
    """Elimina un libro existente retornando 204 No Content, o 404 si no existe."""
    titulo_limpio = titulo.strip().lower()
    for idx, libro in enumerate(libros_db):
        if libro.titulo.strip().lower() == titulo_limpio:
            libros_db.pop(idx)
            return None

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"No se puede eliminar. El libro '{titulo}' no existe."
    )

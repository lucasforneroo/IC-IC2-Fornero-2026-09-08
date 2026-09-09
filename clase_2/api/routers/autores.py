from typing import List
from fastapi import APIRouter, HTTPException, status

from clase_2.api.models import Autor

router = APIRouter(
    prefix="/autores",
    tags=["Autores"],
)

_AUTORES_DB_INICIAL: List[Autor] = [
    Autor(nombre="Jorge Luis Borges", nacionalidad="Argentina"),
    Autor(nombre="Julio Cortázar", nacionalidad="Argentina"),
    Autor(nombre="Gabriel García Márquez", nacionalidad="Colombia"),
]

autores_db: List[Autor] = [autor.model_copy() for autor in _AUTORES_DB_INICIAL]


def reiniciar_db_autores() -> None:
    """Restaura la base de autores a su estado inicial."""
    global autores_db
    autores_db.clear()
    autores_db.extend([autor.model_copy() for autor in _AUTORES_DB_INICIAL])


@router.get(
    "",
    response_model=List[Autor],
    summary="Listar todos los autores registrados",
    status_code=status.HTTP_200_OK,
)
def listar_autores() -> List[Autor]:
    """Retorna la lista de autores."""
    return autores_db


@router.post(
    "",
    response_model=Autor,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo autor",
)
def crear_autor(autor_in: Autor) -> Autor:
    """Registra un nuevo autor en memoria."""
    for existente in autores_db:
        if existente.nombre.strip().lower() == autor_in.nombre.strip().lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El autor '{autor_in.nombre}' ya se encuentra registrado."
            )

    autores_db.append(autor_in)
    return autor_in

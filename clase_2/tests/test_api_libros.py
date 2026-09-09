"""Tests de integración para la API REST de Libros con TestClient de FastAPI (Clase 2, Parte E).

Implementa:
- E1: GET /libros devuelve status_code 200 y lista de recursos.
- E2: Automatización de la prueba de validación con status_code 422.
- E3: Cobertura de camino feliz (201) y camino con error (422 / 400).
- E4: Prueba de secuencia end-to-end (POST -> persistencia -> GET).
- Pruebas adicionales para PUT, DELETE (204) y query params (?paginas_min=N).
"""

import pytest
from fastapi.testclient import TestClient

from clase_2.api.main import app
from clase_2.api.routers.libros import reiniciar_db_libros

client = TestClient(app)


@pytest.fixture(autouse=True)
def restaurar_estado_db():
    """Restaura la base de datos en memoria antes de cada test para aislar casos."""
    reiniciar_db_libros()
    yield
    reiniciar_db_libros()


def test_e1_listar_libros_status_200():
    """Ejercicio E1: Verifica que GET /libros retorne status 200 y al menos los 3 libros iniciales."""
    response = client.get("/libros")
    assert response.status_code == 200
    datos = response.json()
    assert isinstance(datos, list)
    assert len(datos) >= 3
    titulos = [item["titulo"] for item in datos]
    assert "Ficciones" in titulos


def test_e2_post_libro_invalido_status_422():
    """Ejercicio E2: Valida que un payload con tipo de dato incorrecto o faltante retorne 422."""
    # Falta el campo obligatorio 'paginas'
    payload_incompleto = {
        "titulo": "Libro Incompleto",
        "autor": "Desconocido",
    }
    resp1 = client.post("/libros", json=payload_incompleto)
    assert resp1.status_code == 422

    # 'paginas' viene con tipo inválido (string)
    payload_tipo_erroneo = {
        "titulo": "Libro Erróneo",
        "paginas": "muchas",
        "autor": "Desconocido",
    }
    resp2 = client.post("/libros", json=payload_tipo_erroneo)
    assert resp2.status_code == 422

    # 'paginas' es <= 0 (violación de regla de negocio Pydantic gt=0, Ejercicio B8)
    payload_paginas_cero = {
        "titulo": "Libro Vacío",
        "paginas": 0,
        "autor": "Desconocido",
    }
    resp3 = client.post("/libros", json=payload_paginas_cero)
    assert resp3.status_code == 422


def test_e3_post_libro_valido_status_201():
    """Ejercicio E3: Verifica la creación exitosa de un libro con todos los campos válidos."""
    payload_valido = {
        "titulo": "Cien años de soledad",
        "paginas": 471,
        "autor": "Gabriel García Márquez",
        "disponible": True,
        "editorial": {
            "nombre": "Editorial Sudamericana",
            "pais": "Argentina",
        },
    }
    response = client.post("/libros", json=payload_valido)
    assert response.status_code == 201
    cuerpo = response.json()
    assert cuerpo["titulo"] == "Cien años de soledad"
    assert cuerpo["paginas"] == 471
    assert cuerpo["editorial"]["pais"] == "Argentina"


def test_e4_secuencia_post_luego_get():
    """Ejercicio E4: Encadena POST y GET para comprobar que el libro creado se recupera."""
    nuevo_libro = {
        "titulo": "El Aleph (Edición Aniversario)",
        "paginas": 210,
        "autor": "Jorge Luis Borges",
        "disponible": True,
    }

    # 1. Crear el libro
    resp_post = client.post("/libros", json=nuevo_libro)
    assert resp_post.status_code == 201

    # 2. Consultar por título puntual
    resp_get_uno = client.get(f"/libros/{nuevo_libro['titulo']}")
    assert resp_get_uno.status_code == 200
    assert resp_get_uno.json()["titulo"] == nuevo_libro["titulo"]

    # 3. Consultar la lista general
    resp_get_todos = client.get("/libros")
    assert resp_get_todos.status_code == 200
    titulos = [l["titulo"] for l in resp_get_todos.json()]
    assert nuevo_libro["titulo"] in titulos


def test_get_libro_inexistente_retorna_404():
    """Verifica que solicitar un libro no registrado responda 404."""
    response = client.get("/libros/LibroQueNoExiste123")
    assert response.status_code == 404
    assert "No se encontró" in response.json()["detail"]


def test_put_actualizar_libro():
    """Verifica el reemplazo completo de los datos de un libro (B6)."""
    datos_actualizados = {
        "titulo": "Ficciones",
        "paginas": 250,  # Modificado
        "autor": "Jorge Luis Borges",
        "disponible": False,  # Modificado
    }
    response = client.put("/libros/Ficciones", json=datos_actualizados)
    assert response.status_code == 200
    assert response.json()["paginas"] == 250
    assert response.json()["disponible"] is False


def test_delete_eliminar_libro():
    """Verifica la eliminación mediante DELETE retornando 204 y posterior 404 (B7)."""
    # Eliminar
    resp_delete = client.delete("/libros/Rayuela")
    assert resp_delete.status_code == 204

    # Verificar que ya no existe
    resp_get = client.get("/libros/Rayuela")
    assert resp_get.status_code == 404


def test_filtrar_por_query_param_paginas_min():
    """Verifica el filtro opcional de query param ?paginas_min=N (B11)."""
    # En la base inicial, Rayuela tiene 600 páginas y Ficciones/Aleph tienen < 300
    response = client.get("/libros?paginas_min=300")
    assert response.status_code == 200
    libros = response.json()
    assert len(libros) == 1
    assert libros[0]["titulo"] == "Rayuela"

"""Tests unitarios para el Cliente HTTP (Clase 2, Parte C).

Prueba:
- Consumo exitoso de endpoints GET, POST, PUT, DELETE.
- Respuestas ante códigos de estado 200, 201, 204, 404 y 422.
- Manejo defensivo y captura de excepciones de red (ConnectionError, Timeout).
- Correcto uso y cierre de la sesión requests.Session.
"""

import pytest
from unittest.mock import MagicMock, patch
import requests
from requests.exceptions import ConnectionError, Timeout

from clase_2.cliente.cliente_api import ClienteAPI


@pytest.fixture
def cliente():
    """Fixture que provee una instancia de ClienteAPI."""
    instancia = ClienteAPI(base_url="http://test-server:8000", timeout=2.0)
    yield instancia
    instancia.close()


def test_cliente_saludar_ok(cliente: ClienteAPI):
    """Verifica que saludar() retorne el json cuando el servidor responde 200."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"mensaje": "hola"}

    with patch.object(cliente.session, "get", return_value=mock_resp) as mock_get:
        resultado = cliente.saludar()
        assert resultado == {"mensaje": "hola"}
        mock_get.assert_called_once_with("http://test-server:8000/", timeout=2.0)


def test_cliente_listar_libros_con_filtro(cliente: ClienteAPI):
    """Verifica que listar_libros() pase los parámetros de consulta (?paginas_min)."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = [{"titulo": "Rayuela", "paginas": 600}]

    with patch.object(cliente.session, "get", return_value=mock_resp) as mock_get:
        resultado = cliente.listar_libros(paginas_min=300)
        assert len(resultado) == 1
        assert resultado[0]["titulo"] == "Rayuela"
        mock_get.assert_called_once_with(
            "http://test-server:8000/libros",
            params={"paginas_min": 300},
            timeout=2.0,
        )


def test_cliente_crear_libro_exitoso_201(cliente: ClienteAPI):
    """Verifica la creación exitosa con código 201."""
    datos_libro = {"titulo": "Ficciones", "paginas": 220}
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = datos_libro

    with patch.object(cliente.session, "post", return_value=mock_resp):
        res = cliente.crear_libro(datos_libro)
        assert res == datos_libro


def test_cliente_crear_libro_error_validacion_422(cliente: ClienteAPI):
    """Verifica que ante un error 422 el cliente retorne None sin crashear."""
    datos_invalidos = {"titulo": "Sin Páginas"}
    mock_resp = MagicMock()
    mock_resp.status_code = 422
    mock_resp.json.return_value = {"detail": [{"loc": ["body", "paginas"], "msg": "Field required"}]}

    with patch.object(cliente.session, "post", return_value=mock_resp):
        res = cliente.crear_libro(datos_invalidos)
        assert res is None


def test_cliente_obtener_libro_no_encontrado_404(cliente: ClienteAPI):
    """Verifica que ante un 404 el cliente retorne None de manera controlada."""
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.text = "Not Found"

    with patch.object(cliente.session, "get", return_value=mock_resp):
        res = cliente.obtener_libro("Inexistente")
        assert res is None


def test_cliente_borrar_libro_204(cliente: ClienteAPI):
    """Verifica que borrar_libro retorne True ante un código 204."""
    mock_resp = MagicMock()
    mock_resp.status_code = 204

    with patch.object(cliente.session, "delete", return_value=mock_resp):
        res = cliente.borrar_libro("Rayuela")
        assert res is True


def test_cliente_manejo_connection_error_servidor_apagado(cliente: ClienteAPI):
    """Ejercicio C6: Verifica que capture ConnectionError y retorne None/vacío sin propagar traceback."""
    with patch.object(cliente.session, "get", side_effect=ConnectionError("Connection refused")):
        res_saludo = cliente.saludar()
        assert res_saludo is None

        res_libros = cliente.listar_libros()
        assert res_libros == []


def test_cliente_manejo_timeout_excedido(cliente: ClienteAPI):
    """Ejercicio C7: Verifica que capture Timeout y retorne None/vacío de forma segura."""
    with patch.object(cliente.session, "get", side_effect=Timeout("Request timed out")):
        res = cliente.listar_libros()
        assert res == []

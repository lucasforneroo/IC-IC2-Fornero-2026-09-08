"""Tests unitarios para las funciones de la Clase 1 (Partes D y G).

Cubre los ejercicios de testing:
- G1: Verificación de cálculo de promedio.
- G3 y G7: Pruebas de condición de aprobación parametrizadas con @pytest.mark.parametrize.
- G4: Validación de estructura de diccionario y valores en estadisticas().
- G5: Verificación de manejo de claves faltantes en diccionarios.
- G6: Validación del comportamiento ante listas vacías (caso límite).
"""

import pytest
from typing import List

from clase_1.parte_d_funciones import promedio, aprobo, estadisticas, reporte
from clase_1.parte_c_dicts import c3_obtener_duracion, c1_crear_pelicula


def test_g1_promedio_caso_estandar():
    """Ejercicio G1: Verifica que promedio() calcula correctamente sobre notas estándar."""
    notas = [7.0, 4.0, 9.0, 10.0, 6.0]
    resultado = promedio(notas)
    assert resultado == pytest.approx(7.2)


@pytest.mark.parametrize(
    "notas, minimo, esperado",
    [
        ([8.0, 7.0, 9.0], 6.0, True),     # Caso aprobación clara (promedio 8.0 >= 6.0)
        ([4.0, 5.0, 3.0], 6.0, False),    # Caso desaprobación (promedio 4.0 < 6.0)
        ([6.0, 6.0, 6.0], 6.0, True),     # Caso límite exacto (promedio 6.0 == 6.0)
        ([5.9, 6.0, 6.0], 6.0, False),    # Caso límite inferior (promedio 5.96 < 6.0)
        ([7.0, 7.0, 7.0], 8.0, False),    # Caso con umbral personalizado no alcanzado
        ([8.5, 9.0, 9.5], 8.0, True),     # Caso con umbral personalizado superado
    ],
)
def test_g3_g7_aprobo_parametrizado(notas: List[float], minimo: float, esperado: bool):
    """Ejercicios G3 y G7: Prueba la función aprobo() para múltiples casos usando parametrize."""
    assert aprobo(notas, minimo=minimo) == esperado


def test_g4_estadisticas_estructura_y_valores():
    """Ejercicio G4: Verifica que estadisticas() devuelva el dict con las claves y valores correctos."""
    notas = [10.0, 4.0, 6.0, 8.0]
    resultado = estadisticas(notas)

    assert isinstance(resultado, dict)
    assert "promedio" in resultado
    assert "maximo" in resultado
    assert "minimo" in resultado

    assert resultado["promedio"] == pytest.approx(7.0)
    assert resultado["maximo"] == 10.0
    assert resultado["minimo"] == 4.0


def test_g5_acceso_clave_inexistente():
    """Ejercicio G5: Verifica que el acceso a atributos opcionales no falle y retorne el fallback."""
    pelicula = c1_crear_pelicula(titulo="Dune", anio=2021, director="Denis Villeneuve")
    duracion = c3_obtener_duracion(pelicula, default="desconocido")
    assert duracion == "desconocido"

    pelicula_con_duracion = {"titulo": "Dune", "duracion": "155 min"}
    assert c3_obtener_duracion(pelicula_con_duracion) == "155 min"


def test_g6_promedio_y_estadisticas_lista_vacia():
    """Ejercicio G6: Valida el comportamiento seguro y documentado ante listas vacías."""
    # Promedio de lista vacía retorna 0.0 sin arrojar ZeroDivisionError
    assert promedio([]) == 0.0

    stats = estadisticas([])
    assert stats["promedio"] == 0.0
    assert stats["maximo"] == 0.0
    assert stats["minimo"] == 0.0


def test_reporte_formato_texto():
    """Verifica que reporte() genera la cadena de texto con el formato exigido en D6."""
    notas = [7.0, 4.0, 9.0, 10.0, 6.0]
    texto = reporte(notas)
    assert "Promedio: 7.2" in texto
    assert "Máximo: 10" in texto
    assert "Mínimo: 4" in texto

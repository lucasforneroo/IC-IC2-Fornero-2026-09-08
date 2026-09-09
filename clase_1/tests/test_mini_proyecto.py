"""Tests unitarios para el Mini-Proyecto Integrador (Clase 1, Parte H).

Valida:
- Carga y casteo de tipos desde archivos CSV.
- Métricas estadísticas agregadas sobre el catálogo.
- Ordenamiento y generación de rankings.
- Generación del reporte ejecutivo formateado.
"""

import pytest
from pathlib import Path

from clase_1.parte_h_mini_proyecto import (
    cargar_catalogo,
    calcular_metricas_catalogo,
    ordenar_ranking,
    generar_resumen_ejecutivo,
)


@pytest.fixture
def csv_temporal(tmp_path: Path) -> Path:
    """Fixture que crea un archivo CSV aislado para pruebas unitarias."""
    archivo = tmp_path / "test_peliculas.csv"
    contenido = (
        "titulo,anio,puntaje,genero\n"
        "Matrix,1999,8.7,Sci-Fi\n"
        "Godfather,1972,9.2,Crime\n"
        "Inception,2010,8.8,Sci-Fi\n"
    )
    archivo.write_text(contenido, encoding="utf-8")
    return archivo


def test_cargar_catalogo_tipos_correctos(csv_temporal: Path):
    """Verifica que cargar_catalogo lee el CSV y convierte los tipos a int/float."""
    catalogo = cargar_catalogo(str(csv_temporal))

    assert len(catalogo) == 3
    assert isinstance(catalogo[0]["anio"], int)
    assert isinstance(catalogo[0]["puntaje"], float)
    assert catalogo[0]["titulo"] == "Matrix"
    assert catalogo[0]["anio"] == 1999
    assert catalogo[0]["puntaje"] == 8.7


def test_calcular_metricas_catalogo(csv_temporal: Path):
    """Verifica el cálculo de total, promedio, máximo, mínimo y mejor película."""
    catalogo = cargar_catalogo(str(csv_temporal))
    metricas = calcular_metricas_catalogo(catalogo)

    assert metricas["total"] == 3
    assert metricas["promedio"] == pytest.approx(8.9, 0.05)
    assert metricas["maximo"] == 9.2
    assert metricas["minimo"] == 8.7
    assert metricas["mejor_pelicula"] == "Godfather"


def test_calcular_metricas_catalogo_vacio():
    """Verifica el manejo defensivo cuando el catálogo está vacío."""
    metricas = calcular_metricas_catalogo([])
    assert metricas["total"] == 0
    assert metricas["promedio"] == 0.0
    assert metricas["mejor_pelicula"] is None


def test_ordenar_ranking_descendente(csv_temporal: Path):
    """Verifica que el ranking ordena de mayor a menor por puntaje y soporta límites."""
    catalogo = cargar_catalogo(str(csv_temporal))
    ranking = ordenar_ranking(catalogo)

    assert ranking[0]["titulo"] == "Godfather"
    assert ranking[1]["titulo"] == "Inception"
    assert ranking[2]["titulo"] == "Matrix"

    top_1 = ordenar_ranking(catalogo, limite=1)
    assert len(top_1) == 1
    assert top_1[0]["titulo"] == "Godfather"


def test_generar_resumen_ejecutivo(csv_temporal: Path):
    """Verifica que el reporte ejecutivo contiene los datos clave formateados."""
    catalogo = cargar_catalogo(str(csv_temporal))
    reporte = generar_resumen_ejecutivo(catalogo)

    assert "REPORTE EJECUTIVO" in reporte
    assert "Godfather" in reporte
    assert "8.90" in reporte or "8.89" in reporte or "8.9" in reporte

from typing import List, Dict, Any, Optional
from pathlib import Path

from clase_1.parte_e_archivos import e1_leer_csv, crear_csv_ejemplo
from clase_1.parte_d_funciones import promedio, estadisticas


def cargar_catalogo(ruta_csv: str) -> List[Dict[str, Any]]:
    filas = e1_leer_csv(ruta_csv)
    catalogo: List[Dict[str, Any]] = []

    for fila in filas:
        try:
            catalogo.append({
                "titulo": str(fila["titulo"]).strip(),
                "anio": int(fila["anio"]),
                "puntaje": float(fila["puntaje"]),
                "genero": str(fila.get("genero", "General")).strip(),
            })
        except (ValueError, KeyError):
            # Ignora filas con formato corrupto o datos faltantes
            continue

    return catalogo


def calcular_metricas_catalogo(catalogo: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not catalogo:
        return {
            "total": 0,
            "promedio": 0.0,
            "maximo": 0.0,
            "minimo": 0.0,
            "mejor_pelicula": None,
        }

    puntajes = [p["puntaje"] for p in catalogo]
    stats = estadisticas(puntajes)
    mejor = max(catalogo, key=lambda p: p["puntaje"])

    return {
        "total": len(catalogo),
        "promedio": stats["promedio"],
        "maximo": stats["maximo"],
        "minimo": stats["minimo"],
        "mejor_pelicula": mejor["titulo"],
    }


def ordenar_ranking(
    catalogo: List[Dict[str, Any]],
    limite: Optional[int] = None
) -> List[Dict[str, Any]]:
    ranking = sorted(catalogo, key=lambda p: p["puntaje"], reverse=True)
    if limite is not None:
        return ranking[:limite]
    return ranking


def generar_resumen_ejecutivo(catalogo: List[Dict[str, Any]]) -> str:
    metricas = calcular_metricas_catalogo(catalogo)
    top_3 = ordenar_ranking(catalogo, limite=3)

    lineas = [
        "========================================",
        "   REPORTE EJECUTIVO - ANÁLISIS DE CINE ",
        "========================================",
        f"Total de películas analizadas : {metricas['total']}",
        f"Puntaje promedio global       : {metricas['promedio']:.2f}",
        f"Puntaje máximo registrado     : {metricas['maximo']}",
        f"Puntaje mínimo registrado     : {metricas['minimo']}",
        f"Película destacada (Top 1)    : {metricas['mejor_pelicula']}",
        "----------------------------------------",
        " TOP 3 MEJORES CALIFICADAS:",
    ]

    for idx, pelicula in enumerate(top_3, start=1):
        lineas.append(
            f"  {idx}. {pelicula['titulo']} ({pelicula['anio']}) "
            f"— {pelicula['puntaje']} pts [{pelicula['genero']}]"
        )

    lineas.append("========================================")
    return "\n".join(lineas)


def ejecutar_mini_proyecto(ruta_csv: str = "clase_1/peliculas.csv") -> Dict[str, Any]:
    """Orquesta la ejecución completa del pipeline de procesamiento de datos.

    Args:
        ruta_csv: Ruta del dataset CSV a procesar.

    Returns:
        Diccionario con el catálogo cargado, métricas y el ranking completo.
    """
    crear_csv_ejemplo(ruta_csv)
    catalogo = cargar_catalogo(ruta_csv)
    metricas = calcular_metricas_catalogo(catalogo)
    ranking = ordenar_ranking(catalogo)

    return {
        "catalogo": catalogo,
        "metricas": metricas,
        "ranking": ranking,
    }


if __name__ == "__main__":
    resultado = ejecutar_mini_proyecto("clase_1/peliculas.csv")
    print(generar_resumen_ejecutivo(resultado["catalogo"]))

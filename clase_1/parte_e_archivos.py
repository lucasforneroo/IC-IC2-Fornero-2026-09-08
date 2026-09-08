import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple


DATASET_CSV_DEFAULT = """titulo,anio,puntaje,genero
Inception,2010,8.8,Sci-Fi
Interstellar,2014,8.7,Sci-Fi
The Dark Knight,2008,9.0,Action
Pulp Fiction,1994,8.9,Crime
The Matrix,1999,8.7,Sci-Fi
The Godfather,1972,9.2,Crime
Fight Club,1999,8.8,Drama
Forrest Gump,1994,8.8,Drama
"""


def crear_csv_ejemplo(ruta: str) -> None:
    path = Path(ruta)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(DATASET_CSV_DEFAULT.strip(), encoding="utf-8")


# Ejercicio E1:
def e1_leer_csv(ruta: str) -> List[Dict[str, str]]:
    path = Path(ruta)
    if not path.exists():
        crear_csv_ejemplo(ruta)

    with open(path, mode="r", encoding="utf-8", newline="") as archivo:
        lector = csv.DictReader(archivo)
        return list(lector)


# Ejercicio E2:
def e2_sumar_puntajes(ruta: str) -> float:
    filas = e1_leer_csv(ruta)
    suma = sum(float(fila["puntaje"]) for fila in filas if "puntaje" in fila)
    return round(suma, 2)

# Ejercicio E3:
def e3_reporte_peliculas(ruta: str) -> Dict[str, Any]:
    filas = e1_leer_csv(ruta)
    if not filas:
        return {"total_peliculas": 0, "puntaje_promedio": 0.0, "mejor_pelicula": None}

    total = len(filas)
    suma_puntajes = sum(float(f["puntaje"]) for f in filas)
    promedio = round(suma_puntajes / total, 2)

    mejor = max(filas, key=lambda f: float(f["puntaje"]))

    return {
        "total_peliculas": total,
        "puntaje_promedio": promedio,
        "mejor_pelicula": mejor["titulo"],
        "mejor_puntaje": float(mejor["puntaje"]),
    }

# Ejercicio E4:
def e4_filtrar_por_genero(
    ruta_origen: str,
    ruta_destino: str,
    genero_filtro: str
) -> List[Dict[str, str]]:
    filas = e1_leer_csv(ruta_origen)
    genero_buscado = genero_filtro.strip().lower()

    filtradas = [
        f for f in filas
        if f.get("genero", "").strip().lower() == genero_buscado
    ]

    if filtradas:
        campos = list(filtradas[0].keys())
        path_dest = Path(ruta_destino)
        path_dest.parent.mkdir(parents=True, exist_ok=True)

        with open(path_dest, mode="w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(filtradas)

    return filtradas

# Ejercicio E5:
def e5_promedio_por_genero(ruta: str) -> Dict[str, float]:
    filas = e1_leer_csv(ruta)
    acumuladores: Dict[str, List[float]] = {}

    for fila in filas:
        genero = fila.get("genero", "Desconocido").strip()
        puntaje = float(fila["puntaje"])
        if genero not in acumuladores:
            acumuladores[genero] = []
        acumuladores[genero].append(puntaje)

    promedios: Dict[str, float] = {}
    for genero, puntajes in acumuladores.items():
        promedios[genero] = round(sum(puntajes) / len(puntajes), 2)

    return promedios


if __name__ == "__main__":
    csv_path = "clase_1/peliculas.csv"
    csv_filtradas = "clase_1/filtradas.csv"

    print("Ejercicio E1: Crear y leer CSV")
    crear_csv_ejemplo(csv_path)
    filas = e1_leer_csv(csv_path)
    print(f"Total filas leídas: {len(filas)}")
    for f in filas[:3]:
        print(f"  - {f}")

    print("\nEjercicio E2: Sumar puntajes")
    suma = e2_sumar_puntajes(csv_path)
    print(f"Suma total de puntajes: {suma}")

    print("\nEjercicio E3: Reporte de películas")
    rep = e3_reporte_peliculas(csv_path)
    print(f"Reporte: {rep}")

    print("\nEjercicio E4: Filtrar por género Sci-Fi y guardar")
    filtradas = e4_filtrar_por_genero(csv_path, csv_filtradas, "Sci-Fi")
    print(f"Guardadas {len(filtradas)} películas en {csv_filtradas}")

    print("\nEjercicio E5: Promedio agrupado por género")
    prom_generos = e5_promedio_por_genero(csv_path)
    for g, prom in prom_generos.items():
        print(f"  - {g}: {prom}")

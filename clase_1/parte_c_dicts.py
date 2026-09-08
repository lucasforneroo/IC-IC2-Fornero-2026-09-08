from typing import Dict, List, Any, Optional

# Ejercicio C1:
def c1_crear_pelicula(
    titulo: str = "Inception",
    anio: int = 2010,
    director: str = "Christopher Nolan"
) -> Dict[str, Any]:
    return {
        "titulo": titulo,
        "anio": anio,
        "director": director,
    }

# Ejercicio C2:
def c2_modificar_pelicula(pelicula: Dict[str, Any], puntaje: float, nuevo_anio: int) -> Dict[str, Any]:
    pelicula["puntaje"] = puntaje
    pelicula["anio"] = nuevo_anio
    return pelicula

# Ejercicio C3:
def c3_obtener_duracion(pelicula: Dict[str, Any], default: str = "desconocido") -> Any:
    return pelicula.get("duracion", default)

# Ejercicio C4:
def c4_listar_titulos(peliculas: List[Dict[str, Any]]) -> List[str]:
    return [p["titulo"] for p in peliculas if "titulo" in p]

# Ejercicio C5:
def c5_buscar_por_director(
    peliculas: List[Dict[str, Any]],
    director: str,
    coincidencia_parcial: bool = True
) -> List[Dict[str, Any]]:
    resultados: List[Dict[str, Any]] = []
    director_query = director.strip().lower()

    for p in peliculas:
        dir_p = str(p.get("director", "")).lower()
        if coincidencia_parcial:
            if director_query in dir_p:
                resultados.append(p)
        else:
            if director_query == dir_p:
                resultados.append(p)

    return resultados

# Ejercicio C6:
def c6_combinar_fichas(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    return dict1 | dict2

# Ejercicio C7:
def c7_contador_palabras(frase: str) -> Dict[str, int]:
    palabras = frase.lower().split()
    conteo: Dict[str, int] = {}

    for palabra in palabras:
        palabra_limpia = palabra.strip(".,;:!?\"'()")
        if palabra_limpia:
            conteo[palabra_limpia] = conteo.get(palabra_limpia, 0) + 1

    return conteo

# Ejercicio C8:
def c8_inventario_tienda() -> Dict[str, Dict[str, Any]]:
    inventario = {
        "laptop": {"precio": 1200.0, "stock": 15},
        "teclado": {"precio": 45.0, "stock": 50},
        "monitor": {"precio": 300.0, "stock": 8},
        "mouse": {"precio": 25.0, "stock": 100},
    }
    return inventario


if __name__ == "__main__":
    print("Ejercicio C1")
    peli = c1_crear_pelicula()
    print(f"Película creada: {peli}")
    print(f"Título: {peli['titulo']}")

    print("\nEjercicio C2")
    c2_modificar_pelicula(peli, puntaje=8.8, nuevo_anio=2010)
    print(f"Película modificada: {peli}")

    print("\nEjercicio C3")
    print(f"Duración con fallback: {c3_obtener_duracion(peli)}")

    print("\nEjercicio C4")
    catalogo = [
        {"titulo": "Inception", "anio": 2010, "director": "Christopher Nolan", "puntaje": 8.8},
        {"titulo": "Interstellar", "anio": 2014, "director": "Christopher Nolan", "puntaje": 8.7},
        {"titulo": "Pulp Fiction", "anio": 1994, "director": "Quentin Tarantino", "puntaje": 8.9},
    ]
    print(f"Títulos en catálogo: {c4_listar_titulos(catalogo)}")
    
    print("\nEjercicio C5")
    print(f"Búsqueda parcial 'nolan': {[p['titulo'] for p in c5_buscar_por_director(catalogo, 'nolan')]}")

    print("\nEjercicio C6")
    ficha_a = {"titulo": "Dune", "anio": 2021}
    ficha_b = {"puntaje": 8.0, "anio": 2024}
    print(f"A | B -> {c6_combinar_fichas(ficha_a, ficha_b)}")
    print(f"B | A -> {c6_combinar_fichas(ficha_b, ficha_a)}")

    print("\nEjercicio C7")
    frase_test = "Python es genial y aprender Python con APIs es todavía más genial"
    print(f"Histograma de palabras: {c7_contador_palabras(frase_test)}")

    print("\nEjercicio C8")
    inv = c8_inventario_tienda()
    print(f"Inventario completo: {inv}")
    print(f"Precio del monitor: ${inv['monitor']['precio']}")

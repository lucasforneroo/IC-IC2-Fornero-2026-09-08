from typing import List, Tuple, Any

# Ejercicio B1: 
def b1_playlist() -> Tuple[List[str], str, str]:
    playlist = [
        "Bohemian Rhapsody",
        "Hotel California",
        "Stairway to Heaven",
        "Sweet Child O' Mine",
        "Comfortably Numb",
    ]
    primera = playlist[0]
    ultima = playlist[-1]
    return playlist, primera, ultima

# Ejercicio B2:
def b2_sumar_a_lista(playlist: List[str], nuevas_canciones: List[str]) -> List[str]:
    playlist.extend(nuevas_canciones)
    return playlist

# Ejercicio B3:
def b3_mas_alto_y_mas_bajo(puntajes: List[int]) -> Tuple[int, int, float]:
    if not puntajes:
        raise ValueError("La lista de puntajes no puede estar vacía.")

    maximo = puntajes[0]
    minimo = puntajes[0]
    suma_total = 0

    for puntaje in puntajes:
        if puntaje > maximo:
            maximo = puntaje
        if puntaje < minimo:
            minimo = puntaje
        suma_total += puntaje

    promedio = suma_total / len(puntajes)
    return maximo, minimo, promedio


# Ejercicio B4:
def b4_filtrar_puntajes(puntajes: List[int], umbral: int = 100) -> List[int]:
    return [p for p in puntajes if p > umbral]

# Ejercicio B5:
def b5_ranking(puntajes: List[int], descendente: bool = True) -> List[int]:
    return sorted(puntajes, reverse=descendente)

# Ejercicio B6:
def b6_al_reves(lista: List[Any]) -> List[Any]:
    return lista[::-1]

# Ejercicio B7:
def b7_sin_repetidos(elementos: List[Any], preservar_orden: bool = False) -> List[Any]:
    if preservar_orden:
        return list(dict.fromkeys(elementos))
    return list(set(elementos))

# Ejercicio B8:
def b8_promedio_movil(lecturas: List[float], ventana: int = 3) -> List[float]:
    if len(lecturas) < ventana:
        return []

    promedios: List[float] = []
    for i in range(len(lecturas) - ventana + 1):
        subconjunto = lecturas[i : i + ventana]
        promedio_sub = sum(subconjunto) / ventana
        promedios.append(round(promedio_sub, 2))

    return promedios


if __name__ == "__main__":
    print("Ejercicio B1")
    p, primero, ultimo = b1_playlist()
    print(f"Playlist: {p}\nPrimero: {primero}\nÚltimo: {ultimo}")

    print("\nEjercicio B2")
    b2_sumar_a_lista(p, ["Yesterday", "Imagine"])
    print(f"Playlist extendida (total {len(p)}): {p}")

    print("\nEjercicio B3")
    puntajes = [120, 45, 300, 80, 210]
    max_p, min_p, prom_p = b3_mas_alto_y_mas_bajo(puntajes)
    print(f"Puntajes: {puntajes}")
    print(f"Máximo: {max_p} (max={max(puntajes)}) | Mínimo: {min_p} (min={min(puntajes)}) | Promedio: {prom_p}")

    print("\nEjercicio B4")
    filtrados = b4_filtrar_puntajes(puntajes, 100)
    print(f"Puntajes > 100: {filtrados} (original intacta: {puntajes})")

    print("\nEjercicio B5")
    ranking = b5_ranking(puntajes)
    print(f"Ranking ordenado desc: {ranking}")

    print("\nEjercicio B6")
    print(f"Playlist invertida con slicing: {b6_al_reves(p)}")

    print("\nEjercicio B7")
    nums_dup = [3, 5, 3, 8, 5, 1, 8, 8]
    print(f"Lista original: {nums_dup} -> Sin repetidos (set): {b7_sin_repetidos(nums_dup)}")

    print("\nEjercicio B8")
    lecturas_sensor = [10.0, 12.0, 15.0, 14.0, 16.0, 18.0, 20.0, 22.0, 21.0, 19.0]
    prom_movil = b8_promedio_movil(lecturas_sensor, 3)
    print(f"Lecturas ({len(lecturas_sensor)}): {lecturas_sensor}")
    print(f"Promedio móvil ventana 3 ({len(prom_movil)} elementos): {prom_movil}")

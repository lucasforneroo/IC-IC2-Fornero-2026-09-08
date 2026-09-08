from typing import List, Dict, Union

# Ejercicio D1:
def promedio(notas: List[float]) -> float:
    if not notas:
        return 0.0
    return sum(notas) / len(notas)

# Ejercicio D2:
def aprobo(notas: List[float], minimo: float = 6.0) -> bool:
    return promedio(notas) >= minimo

# Ejercicio D3:
def estadisticas(notas: List[float]) -> Dict[str, float]:
    if not notas:
        return {
            "promedio": 0.0,
            "maximo": 0.0,
            "minimo": 0.0,
        }

    return {
        "promedio": round(promedio(notas), 2),
        "maximo": float(max(notas)),
        "minimo": float(min(notas)),
    }

# Ejercicio D4:
# Ejercicio D5:

def reporte(notas: List[float]) -> str:
    stats = estadisticas(notas)
    prom_str = f"{stats['promedio']:.1f}" if stats['promedio'] != 0.0 else "0.0"
    max_val = int(stats['maximo']) if stats['maximo'].is_integer() else stats['maximo']
    min_val = int(stats['minimo']) if stats['minimo'].is_integer() else stats['minimo']

    return f"Promedio: {prom_str} | Máximo: {max_val} | Mínimo: {min_val}"


if __name__ == "__main__":
    notas_ejemplo = [7.0, 4.0, 9.0, 10.0, 6.0]

    print("Ejercicio D1")
    print(f"Notas: {notas_ejemplo} -> Promedio: {promedio(notas_ejemplo):.2f}")

    print("\nEjercicio D2 y D4: Aprobó")
    print(f"¿Aprobó (min 6.0)? {aprobo(notas_ejemplo)}")
    print(f"¿Aprobó (min 8.0)? {aprobo(notas_ejemplo, minimo=8.0)}")

    print("\nEjercicio D3: Estadísticas")
    print(f"Estadísticas: {estadisticas(notas_ejemplo)}")

    print("\nEjercicio D5: Caso lista vacía")
    print(f"Promedio lista vacía: {promedio([])}")
    print(f"Estadísticas lista vacía: {estadisticas([])}")

    print("\nEjercicio D6: Reporte")
    print(f"Reporte formateado: {reporte(notas_ejemplo)}")

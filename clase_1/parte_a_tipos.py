from typing import List, Tuple, Dict

# Ejercicio A1:
def a1_calculadora_promedio(notas: List[float] = None) -> Tuple[float, bool]:
    if notas is None:
        notas = [7.0, 4.0, 9.0, 10.0, 6.0]

    promedio = sum(notas) / len(notas)
    aprobo = promedio >= 6.0
    return promedio, aprobo

# Ejercicio A2:
def a2_el_tipo_importa() -> Tuple[str, int]:
    cantidad_str = "5"
    precio = 100

    resultado_sin_cast = cantidad_str * precio
    resultado_con_cast = int(cantidad_str) * precio

    return resultado_sin_cast, resultado_con_cast

# Ejercicio A3
def a3_conversion_temperatura(celsius: float) -> float:
    return (celsius * 9.0 / 5.0) + 32.0

# Ejercicio A4
def a4_redondeo_formato(promedio: float) -> str:
    return f"{promedio:.1f}"

# Ejercicio A5
def a5_mayor_o_menor(edad: int) -> str:
    if edad >= 18:
        return "mayor de edad"
    return "menor de edad"

# Ejercicio A6
def a6_par_impar_turnos(total_alumnos: int = 30) -> Tuple[List[int], List[int]]:
    pares: List[int] = []
    impares: List[int] = []

    for numero in range(1, total_alumnos + 1):
        if numero % 2 == 0:
            pares.append(numero)
        else:
            impares.append(numero)

    return pares, impares

# Ejercicio A7
def a7_cadena_conversiones(km: float) -> Dict[str, float]:
    factor_km_a_millas = 0.621371
    factor_millas_a_pies = 5280.0

    millas = km * factor_km_a_millas
    pies = millas * factor_millas_a_pies

    return {
        "kilometros": km,
        "millas": millas,
        "pies": pies,
    }


if __name__ == "__main__":
    print("Ejercicio A1")
    prom, apr = a1_calculadora_promedio()
    print(f"Promedio: {prom} - Aprobó: {apr} ({'Aprobado' if apr else 'Desaprobado'})")

    print("\nEjercicio A2")
    res_str, res_num = a2_el_tipo_importa()
    print(f"Resultado sin cast (longitud {len(res_str)}): {res_str[:15]}...")
    print(f"Resultado con int('5') * 100: {res_num}")

    print("\nEjercicio A3")
    for c in [0, 100, 36.5]:
        print(f"{c} °C = {a3_conversion_temperatura(c)} °F")

    print("\nEjercicio A4")
    print(f"Promedio con 1 decimal: {a4_redondeo_formato(prom)}")

    print("\nEjercicio A5")
    for e in [17, 18, 0, 25]:
        print(f"Edad {e}: {a5_mayor_o_menor(e)}")

    print("\nEjercicio A6")
    pares, impares = a6_par_impar_turnos(30)
    print(f"Total pares: {len(pares)} - Total impares: {len(impares)} - Suma: {len(pares) + len(impares)}")

    print("\nEjercicio A7")
    conv = a7_cadena_conversiones(10.0)
    print(f"10 km = {conv['millas']:.3f} millas = {conv['pies']:.1f} pies")

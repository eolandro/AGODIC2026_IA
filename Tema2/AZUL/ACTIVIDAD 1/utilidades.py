import json
import math
import os


# ---------------------------------------------------------------------
# Entrada / Salida
# ---------------------------------------------------------------------

def cargar_json(ruta):
    if not os.path.exists(ruta):
        return None
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_json(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=4)


# ---------------------------------------------------------------------
# Teoría de la información
# ---------------------------------------------------------------------

def entropia_uniforme(n):
    if n <= 1:
        return 0.0
    return math.log2(n)


def ganancia_informacion(caracteristica, animales):
    n = len(animales)
    if n == 0:
        return 0.0

    si = [a for a in animales.values() if a.get(caracteristica) is True]
    no = [a for a in animales.values() if a.get(caracteristica) is False]

    n_si, n_no = len(si), len(no)

    h_actual = entropia_uniforme(n)
    h_esperada = (n_si / n) * entropia_uniforme(n_si) + \
                 (n_no / n) * entropia_uniforme(n_no)

    ganancia = h_actual - h_esperada
    # Corrección de errores de punto flotante muy pequeños
    if abs(ganancia) < 1e-12:
        ganancia = 0.0
    return ganancia


def preguntar_si_no(texto):
    while True:
        resp = input(texto + " (s/n): ").strip().lower()
        if resp in ("s", "si", "sí", "y", "yes"):
            return True
        if resp in ("n", "no"):
            return False
        print("  -> Respuesta no reconocida, escribe 's' (sí) o 'n' (no).")

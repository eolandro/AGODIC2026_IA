import os
from utilidades import cargar_json, guardar_json, ganancia_informacion

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_ANIMALES = os.path.join(DIR_BASE, "animales.json")
ARCHIVO_PESOS = os.path.join(DIR_BASE, "pesos.json")


def calcular_tabla_pesos(datos):

    animales = datos["animales"]
    caracteristicas = datos["caracteristicas"]

    pesos = []
    for clave in caracteristicas:
        g = ganancia_informacion(clave, animales)
        pesos.append((clave, g))

    pesos.sort(key=lambda par: par[1], reverse=True)
    return pesos


def entrenar():
    datos = cargar_json(ARCHIVO_ANIMALES)
    if datos is None:
        print("ERROR: No existe 'animales.json'.")
        print("Ejecuta primero 'inicializador.py' para crear la base de conocimiento.")
        return None

    if len(datos.get("animales", {})) < 2:
        print("ERROR: Se necesitan al menos 2 animales en 'animales.json'.")
        return None

    pesos = calcular_tabla_pesos(datos)

    print("\n=== ENTRENADOR: Tabla de pesos (ganancia de información) ===")
    print(f"{'Característica':25s} {'Pregunta':45s} {'Ganancia (bits)'}")
    print("-" * 90)
    for clave, g in pesos:
        pregunta = datos["caracteristicas"].get(clave, "")
        print(f"{clave:25s} {pregunta[:43]:45s} {g:.4f}")
    print("-" * 90)
    print("(Mayor ganancia = mejor pregunta para separar animales)\n")

    guardar_json(ARCHIVO_PESOS, {"pesos": pesos})
    print(f"-> Tabla de pesos guardada en '{ARCHIVO_PESOS}'.")
    print("-> Ejecuta ahora 'adivinador.py' para jugar.")
    return pesos


if __name__ == "__main__":
    entrenar()

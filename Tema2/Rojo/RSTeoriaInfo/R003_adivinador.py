import json
import math
import sys
from pathlib import Path

ARCHIVO = Path("tabla_pesos.json")


def entropia(n):
    return math.log2(n) if n > 1 else 0.0


def ganancia(candidatos, clave):
    total = len(candidatos)
    si = sum(1 for a in candidatos if a["caracteristicas"][clave])
    no = total - si
    if si == 0 or no == 0:
        return None
    return entropia(total) - si / total * entropia(si) - no / total * entropia(no)


def elegir_pregunta(candidatos, pendientes, orden):
    opciones = []
    for clave in pendientes:
        g = ganancia(candidatos, clave)
        if g is not None:
            opciones.append((round(g, 9), -orden[clave], clave))
    if not opciones:
        return None
    g, _, clave = max(opciones)
    return clave, g


def contradicciones(animal, respuestas):
    return sum(1 for clave, r in respuestas.items() if animal["caracteristicas"][clave] != r)


def filtrar_candidatos(animales, respuestas):
    conteo = [(contradicciones(a, respuestas), a) for a in animales]
    minimo = min(c for c, _ in conteo)
    return [a for c, a in conteo if c == minimo], minimo


def cargar_tabla():
    if not ARCHIVO.exists():
        sys.exit("No existe tabla_pesos.json. Ejecuta primero R002_entrenador.py")
    try:
        datos = json.loads(ARCHIVO.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"tabla_pesos.json no es un JSON válido: {e}")
    if not isinstance(datos, dict) or not datos.get("animales") or not datos.get("preguntas"):
        sys.exit("tabla_pesos.json no tiene el formato esperado. Vuelve a ejecutar R002_entrenador.py")
    return datos


def preguntar(texto):
    while True:
        respuesta = input(f"¿{texto}? [s/n]: ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta inválida, escribe s o n.")


def main():
    datos = cargar_tabla()
    animales = datos["animales"]
    textos = {p["clave"]: p["pregunta"] for p in datos["preguntas"]}
    orden = {p["clave"]: i for i, p in enumerate(datos["preguntas"])}
    pendientes = list(textos)
    respuestas = {}

    print("Piensa en uno de los animales de la tabla y responde con s o n.\n")

    candidatos, fallos = filtrar_candidatos(animales, respuestas)
    while len(candidatos) > 1:
        eleccion = elegir_pregunta(candidatos, pendientes, orden)
        if eleccion is None:
            break
        clave, g = eleccion
        print(f"Pregunta {len(respuestas) + 1} (ganancia de información: {g:.4f})")
        respuestas[clave] = preguntar(textos[clave])
        pendientes.remove(clave)
        candidatos, fallos = filtrar_candidatos(animales, respuestas)
        print("Candidatos:", ", ".join(a["animal"] for a in candidatos), "\n")

    nombres = ", ".join(a["animal"] for a in candidatos)
    if len(candidatos) == 1 and fallos == 0:
        print(f"Animal adivinado: {nombres.upper()}")
    elif len(candidatos) == 1:
        print(f"Sin coincidencia exacta, el más parecido es {nombres.upper()} ({fallos} respuesta(s) no coinciden).")
    elif fallos == 0:
        print(f"Empate, no se pudo distinguir entre: {nombres}")
    else:
        print(f"Sin coincidencia exacta y con empate entre los más parecidos: {nombres} ({fallos} respuesta(s) no coinciden).")
    print(f"Preguntas realizadas: {len(respuestas)}")


if __name__ == "__main__":
    main()
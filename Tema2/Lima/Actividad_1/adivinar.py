
import json
import sys
from math import ceil, log2
from pathlib import Path

CARPETA = Path(__file__).parent
ARCHIVO_RED = CARPETA / "red_semantica.json"
ARCHIVO_ENTRENAMIENTO = CARPETA / "entrenamiento.json"


def cargar(ruta, programa):
    if not ruta.exists():
        sys.exit(f"Falta {ruta.name}. Ejecuta primero: python {programa}")
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


def entropia(cantidad_si, total):
    if cantidad_si == 0 or cantidad_si == total:
        return 0.0
    p = cantidad_si / total
    return -p * log2(p) - (1 - p) * log2(1 - p)


def mejor_pregunta(candidatos, pendientes):
    mejor = None
    mayor_entropia = 0.0
    for pregunta in pendientes:
        cantidad_si = sum(a["valores"][pregunta["posicion"]] for a in candidatos)
        h = entropia(cantidad_si, len(candidatos))
        if h > mayor_entropia:
            mayor_entropia = h
            mejor = pregunta
    return mejor, mayor_entropia


def adivinar(animales, preguntas, responder, mostrar=True):
    candidatos = list(animales)
    pendientes = list(preguntas)
    realizadas = 0

    while len(candidatos) > 1:
        pregunta, h = mejor_pregunta(candidatos, pendientes)
        if pregunta is None:
            break
        pendientes.remove(pregunta)
        realizadas += 1
        if mostrar:
            print(f"\nPregunta {realizadas} "
                  f"(candidatos: {len(candidatos)}, aporta {h:.2f} bits)")
        respuesta = responder(pregunta)
        candidatos = [a for a in candidatos
                      if a["valores"][pregunta["posicion"]] == respuesta]

    return candidatos, realizadas


def leer_si_no(texto):
    equivalencias = {"s": 1, "si": 1, "sí": 1, "1": 1, "n": 0, "no": 0, "0": 0}
    respuesta = input(texto).strip().lower()
    while respuesta not in equivalencias:
        respuesta = input("  Escribe s (sí) o n (no): ").strip().lower()
    return equivalencias[respuesta]


def jugar(animales, preguntas):
    print("\nAnimales:", ", ".join(a["nombre"] for a in animales))
    print("Piensa en uno y responde s (sí) o n (no).")

    candidatos, realizadas = adivinar(
        animales, preguntas,
        lambda pregunta: leer_si_no(f"  {pregunta['pregunta']} (s/n): "))

    if len(candidatos) == 1:
        print(f"\nTu animal es: {candidatos[0]['nombre'].upper()}")
        if leer_si_no("¿Adiviné? (s/n): "):
            print(f"Adivinado en {realizadas} preguntas.")
        else:
            print("No acerté: alguna respuesta no coincide con la tabla de la red.")
    elif not candidatos:
        print("\nNingún animal de la red coincide con esas respuestas.")
    else:
        print("\nNo puedo distinguir entre:",
              ", ".join(a["nombre"] for a in candidatos))
    print(f"Preguntas realizadas: {realizadas}")


def prueba(animales, preguntas):
    print(f"{'Animal':13} | Preguntas | Resultado")
    print("-" * 40)
    suma = 0
    for animal in animales:
        candidatos, realizadas = adivinar(
            animales, preguntas,
            lambda pregunta: animal["valores"][pregunta["posicion"]],
            mostrar=False)
        correcto = len(candidatos) == 1 and candidatos[0]["nombre"] == animal["nombre"]
        suma += realizadas
        print(f"{animal['nombre']:13} | {realizadas:9} | "
              f"{'correcto' if correcto else 'FALLÓ'}")

    total = len(animales)
    print(f"\nPromedio: {suma / total:.2f} preguntas por animal.")
    print(f"Límite teórico: log2({total}) = {log2(total):.2f} bits "
          f"(ningún método baja de ese promedio; peor caso mínimo: {ceil(log2(total))}).")
    print(f"Preguntar todo sin optimizar: {len(preguntas)} preguntas.")


def main():
    red = cargar(ARCHIVO_RED, "inicializador.py")
    entrenamiento = cargar(ARCHIVO_ENTRENAMIENTO, "entrenador.py")
    animales = red["animales"]
    preguntas = entrenamiento["preguntas"]

    if "--prueba" in sys.argv:
        prueba(animales, preguntas)
        return

    print("=" * 40)
    print("        ADIVINA EL ANIMAL")
    print("=" * 40)
    seguir = 1
    while seguir:
        jugar(animales, preguntas)
        seguir = leer_si_no("\n¿Jugar otra vez? (s/n): ")
    print("Gracias por jugar.")


if __name__ == "__main__":
    main()

"""Paso 3: juego de adivinar animales."""
import json
from pathlib import Path

CARPETA = Path(__file__).parent
with open(CARPETA / "conocimiento.json", encoding="utf-8") as archivo:
    animales = json.load(archivo)
with open(CARPETA / "modelo.json", encoding="utf-8") as archivo:
    orden_preguntas = json.load(archivo)


def respuesta_si_no(texto):
    while True:
        respuesta = input(texto).strip().lower()
        if respuesta in ("s", "si", "sí"):
            return True
        if respuesta in ("n", "no"):
            return False
        print("  Escribe s para sí o n para no.")


def jugar():
    candidatos = list(animales)
    preguntas = orden_preguntas.copy()
    cantidad = 0
    print("\nPiensa en uno de los animales de la lista... ¡No me digas cuál!")
    input("Presiona Enter cuando estés listo para empezar. ")

    while len(candidatos) > 1 and preguntas:
        # La mejor pregunta separa los candidatos en grupos similares.
        def separacion(pregunta):
            si = sum(animales[a][pregunta] for a in candidatos)
            return min(si, len(candidatos) - si)

        pregunta = max(preguntas, key=separacion)
        if separacion(pregunta) == 0:
            break
        preguntas.remove(pregunta)
        cantidad += 1
        print(f"\nPregunta {cantidad} | Animales posibles: {len(candidatos)}")
        respuesta = respuesta_si_no(
            f"  ¿Tu animal tiene {pregunta.replace('_', ' ')}? (s/n): "
        )
        candidatos = [a for a in candidatos if animales[a][pregunta] == respuesta]
        if not candidatos:
            print("\n¡Me dejaste sin candidatos! Alguna respuesta no coincide con la tabla.")
            return False, cantidad

    if len(candidatos) != 1:
        print("\nMe faltan pistas para elegir entre:", ", ".join(candidatos))
        return False, cantidad

    elegido = candidatos[0]
    print(f"\nMi respuesta final es... ¡{elegido.upper()}!")
    acierto = respuesta_si_no("¿Adiviné? (s/n): ")
    if acierto:
        print(f"¡Bien! Lo logré en {cantidad} preguntas.")
    else:
        print("Vaya, me ganaste. Revisa las respuestas de la tabla en inicializador.py.")
    return acierto, cantidad


def menu():
    partidas = 0
    aciertos = 0
    mejor = None
    while True:
        print("\n" + "=" * 42)
        print("       ADIVINA EL ANIMAL")
        print("=" * 42)
        print("1. Jugar")
        print("2. Ver animales disponibles")
        print("3. Cómo jugar")
        print("4. Salir")
        opcion = input("Elige una opción (1-4): ").strip()

        if opcion == "1":
            while True:
                acierto, cantidad = jugar()
                partidas += 1
                if acierto:
                    aciertos += 1
                    mejor = cantidad if mejor is None else min(mejor, cantidad)
                print(f"Marcador: {aciertos}/{partidas} aciertos", end="")
                if mejor is not None:
                    print(f" | Récord: {mejor} preguntas")
                else:
                    print()
                if not respuesta_si_no("¿Quieres volver a jugar? (s/n): "):
                    break
        elif opcion == "2":
            print("\nAnimales:", ", ".join(animales))
        elif opcion == "3":
            print("\nElige mentalmente un animal de la lista y responde s o n.")
            print("Cada respuesta descarta animales. Al final confirmarás mi intento.")
        elif opcion == "4":
            print("¡Hasta la próxima!")
            break
        else:
            print("Elige un número del 1 al 4.")


if __name__ == "__main__":
    menu()

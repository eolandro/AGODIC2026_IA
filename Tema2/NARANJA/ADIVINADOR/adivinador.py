import json
import math
import os
import sys

ARCHIVO_PESOS = "pesos.json"


def entropia(p):
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def mejor_pregunta(candidatos, disponibles, tabla, orden):
    mejor, mejor_h = None, 0.0
    for nom in orden:
        if nom not in disponibles:
            continue
        si = sum(1 for a in candidatos if tabla[a][nom])
        h = entropia(si / len(candidatos))
        if h > mejor_h:
            mejor, mejor_h = nom, h
    return mejor, mejor_h


def si_no(mensaje):
    while True:
        r = input(mensaje + " (s/n): ").strip().lower()
        if r in ("s", "si", "sí"):
            return True
        if r in ("n", "no"):
            return False
        print("  Contesta s o n.")


def main():
    if not os.path.exists(ARCHIVO_PESOS):
        sys.exit(f"No existe {ARCHIVO_PESOS}. Corre primero entrenador.py")

    with open(ARCHIVO_PESOS, encoding="utf-8") as f:
        datos = json.load(f)

    tabla = datos["tabla"]
    total = datos["total"]
    orden = datos["orden_preguntas"]
    texto = {c["nombre"]: f"{c['relacion']} {c['valor']}" for c in datos["caracteristicas"]}

    candidatos = list(tabla)
    disponibles = set(orden)
    preguntas = 0

    print("=== A D I V I N A D O R   E Q U I P O  N A R A N J A ===")
    print("Piensa en uno de estos animales:", ", ".join(candidatos))
    input("Presiona Enter cuando estes listo...")

    while len(candidatos) > 1:
        nom, h = mejor_pregunta(candidatos, disponibles, tabla, orden)
        if nom is None:
            break
        disponibles.discard(nom)
        preguntas += 1
        tiene = si_no(f"\n{preguntas}. ¿Tu animal {texto[nom]}?")
        candidatos = [a for a in candidatos if bool(tabla[a][nom]) == tiene]
        print(f"   (quedan {len(candidatos)}, la pregunta valia {h:.2f} bits)")

    confirmado = False
    if len(candidatos) > 1:
        print(f"\nQuedan animales con el mismo total ({total[candidatos[0]]}): "
              f"{', '.join(candidatos)}")
        while len(candidatos) > 1:
            preguntas += 1
            if si_no(f"\n{preguntas}. ¿Tu animal es {candidatos[0]}?"):
                candidatos = candidatos[:1]
                confirmado = True
            else:
                candidatos = candidatos[1:]

    if not candidatos:
        print("\nCon esas respuestas no coincide ningun animal de la tabla.")
    else:
        animal = candidatos[0]
        print(f"\nTu animal es: {animal.upper()}  (total {total[animal]})")
        if confirmado or si_no("¿Adivine?"):
            print("¡Lo sabia!")
        else:
            print("Entonces alguna respuesta no coincide con la tabla.")

    print(f"\nPreguntas usadas: {preguntas}   "
          f"Minimo teorico: {datos['minimo_teorico_preguntas']} "
          f"(log2 de {len(tabla)} animales)")


if __name__ == "__main__":
    main()

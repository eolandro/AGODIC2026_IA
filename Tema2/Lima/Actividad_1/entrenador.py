import json
import sys
from math import log2
from pathlib import Path

CARPETA = Path(__file__).parent
ARCHIVO_RED = CARPETA / "red_semantica.json"
ARCHIVO_ENTRENAMIENTO = CARPETA / "entrenamiento.json"


def entropia(cantidad_si, total):
    if cantidad_si == 0 or cantidad_si == total:
        return 0.0
    p = cantidad_si / total
    return -p * log2(p) - (1 - p) * log2(1 - p)


def entrenar():
    if not ARCHIVO_RED.exists():
        sys.exit("Falta red_semantica.json. Ejecuta primero: python inicializador.py")

    with open(ARCHIVO_RED, encoding="utf-8") as archivo:
        red = json.load(archivo)

    animales = red["animales"]
    total = len(animales)

    preguntas = []
    for posicion, caracteristica in enumerate(red["caracteristicas"]):
        cantidad_si = sum(animal["valores"][posicion] for animal in animales)
        preguntas.append({
            "posicion": posicion,
            "caracteristica": f"{caracteristica['relacion']} {caracteristica['objeto']}",
            "pregunta": caracteristica["pregunta"],
            "cantidad_si": cantidad_si,
            "cantidad_no": total - cantidad_si,
            "entropia": round(entropia(cantidad_si, total), 4),
        })

    preguntas.sort(key=lambda p: p["entropia"], reverse=True)

    entrenamiento = {
        "total_animales": total,
        "bits_necesarios": round(log2(total), 4),
        "preguntas": preguntas,
    }
    with open(ARCHIVO_ENTRENAMIENTO, "w", encoding="utf-8") as archivo:
        json.dump(entrenamiento, archivo, ensure_ascii=False, indent=2)

    print(f"{'Característica':24} | Sí | No | Entropía (bits)")
    print("-" * 55)
    for p in preguntas:
        print(f"{p['caracteristica']:24} | {p['cantidad_si']:2} | "
              f"{p['cantidad_no']:2} | {p['entropia']:.4f}")

    print(f"\nAnimales: {total}. Información necesaria: log2({total}) = "
          f"{log2(total):.2f} bits.")
    print(f"Entrenamiento guardado en {ARCHIVO_ENTRENAMIENTO.name}")


if __name__ == "__main__":
    entrenar()

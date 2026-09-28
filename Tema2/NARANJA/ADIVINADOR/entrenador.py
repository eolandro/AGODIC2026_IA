import csv
import json
import math
import os
import sys

ARCHIVO_ENTRADA = "animales.json"
ARCHIVO_SALIDA = "pesos.json"
ARCHIVO_CSV = "pesos.csv"


def entropia(p):
    if p == 0 or p == 1:
        return 0.0
    return -p * math.log2(p) - (1 - p) * math.log2(1 - p)


def main():
    if not os.path.exists(ARCHIVO_ENTRADA):
        sys.exit(f"No existe {ARCHIVO_ENTRADA}. Corre primero inicializador.py")

    with open(ARCHIVO_ENTRADA, encoding="utf-8") as f:
        datos = json.load(f)

    caracteristicas = datos["caracteristicas"]
    nombres = [c["nombre"] for c in caracteristicas]
    animales = datos["animales"]
    k, n = len(nombres), len(animales)

    peso = {nom: 2 ** (k - 1 - i) for i, nom in enumerate(nombres)}

    tabla, total = {}, {}
    for animal, rasgos in animales.items():
        tabla[animal] = {nom: (peso[nom] if nom in rasgos else 0) for nom in nombres}
        total[animal] = sum(tabla[animal].values())

    por_total = {}
    for animal, t in total.items():
        por_total.setdefault(t, []).append(animal)
    colisiones = [grupo for grupo in por_total.values() if len(grupo) > 1]

    ent = {}
    for nom in nombres:
        p = sum(1 for a in animales if tabla[a][nom]) / n
        ent[nom] = round(entropia(p), 4)
    orden = sorted(nombres, key=lambda nom: ent[nom], reverse=True)

    resultado = {
        "caracteristicas": caracteristicas,
        "peso_caracteristica": peso,
        "tabla": tabla,
        "total": total,
        "colisiones": colisiones,
        "entropia_caracteristica": ent,
        "orden_preguntas": orden,
        "entropia_total": round(math.log2(n), 4),
        "minimo_teorico_preguntas": math.ceil(math.log2(n)),
    }
    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump(resultado, f, indent=2, ensure_ascii=False)

    with open(ARCHIVO_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["ANIMAL"] + nombres + ["total"])
        for animal in animales:
            w.writerow([animal.upper()] + [tabla[animal][nom] for nom in nombres]
                       + [total[animal]])
        w.writerow(["VALOR DE CADA CARACTERISTICA"] + [peso[nom] for nom in nombres]
                   + [sum(peso.values())])

    print("=== E N T R E N A D O R   E Q U I P O  N A R A N J A ===\n")
    print(f"{'ANIMAL':<14}{'total':>7}   binario")
    for animal in animales:
        print(f"{animal.upper():<14}{total[animal]:>7}   {total[animal]:0{k}b}")

    print(f"\n{'CARACTERISTICA':<20}{'peso':>6}{'H (bits)':>10}")
    for nom in orden:
        print(f"{nom:<20}{peso[nom]:>6}{ent[nom]:>10.3f}")

    print(f"\nAnimales: {n}   Entropia total: {math.log2(n):.3f} bits   "
          f"Minimo teorico: {math.ceil(math.log2(n))} preguntas")
    for grupo in colisiones:
        print(f"AVISO: {', '.join(grupo)} tienen el mismo total "
              f"({total[grupo[0]]}); el adivinador los separara preguntando por nombre.")
    print(f"\nTabla de pesos guardada en {ARCHIVO_SALIDA} y {ARCHIVO_CSV}")


if __name__ == "__main__":
    main()

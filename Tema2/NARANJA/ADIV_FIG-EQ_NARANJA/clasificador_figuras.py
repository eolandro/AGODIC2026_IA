import json
from collections import defaultdict

ARCHIVO = "grafo_figuras.json"
QUITAR_ACENTOS = str.maketrans("ÁÉÍÓÚ", "AEIOU")


def normalizar(texto):
    """'Sí ' -> 'SI', 3 -> '3'."""
    return str(texto).strip().upper().translate(QUITAR_ACENTOS)


def cargar_grafo(ruta):
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    textos = {p["id"]: p["texto"] for p in datos["preguntas"]}
    siguiente = {(t["origen"], normalizar(t["respuesta"])): t["destino"]
                 for t in datos["transiciones"]}

    opciones = defaultdict(list)          
    for t in datos["transiciones"]:
        opciones[t["origen"]].append(normalizar(t["respuesta"]))

    return textos, siguiente, opciones


def preguntar(actual, textos, siguiente, opciones):
    respuesta = normalizar(input(f"{textos[actual]} ({' / '.join(opciones[actual])}): "))
    return siguiente.get((actual, respuesta), actual)


def clasificar(textos, siguiente, opciones, inicio=0):
    actual = inicio
    while actual in opciones:
        actual = preguntar(actual, textos, siguiente, opciones)
    return textos[actual]


def figuras_disponibles(textos, opciones):
    hojas = sorted(set(textos) - set(opciones))
    return [textos[i] for i in hojas]


def main():
    textos, siguiente, opciones = cargar_grafo(ARCHIVO)
    print(f"\n ------ F I G U R A S  G E O M E T R I C A S  -  E Q U I P O   N A R A N J A ----- ")
    print("Piensa en una figura geométrica y responde las preguntas.")
    print("\nFiguras Geometricas:")
    print("\n".join(f"  - {figura}" for figura in figuras_disponibles(textos, opciones)))
    otra = "SI"
    try:
        while otra.startswith("S"):
            print(f"\n La figura es: {clasificar(textos, siguiente, opciones)}\n")
            print("------------------------------------------------------------------" )
            otra = normalizar(input("¿Quieres volver a jugar? (SI / NO): "))
    except (KeyboardInterrupt, EOFError):
        pass
    print("\nHasta luego.")


main()

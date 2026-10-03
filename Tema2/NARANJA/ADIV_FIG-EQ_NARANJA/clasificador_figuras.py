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

    siguiente = {(t["origen"], normalizar(t["respuesta"])): t["destino"]
                 for t in datos["transiciones"]}

    opciones = defaultdict(list)          
    for t in datos["transiciones"]:
        opciones[t["origen"]].append(normalizar(t["respuesta"]))
    opciones = dict(opciones)

   
    mensajes = {p["id"]: f"{p['texto']} ({' / '.join(opciones.get(p['id'], []))}): "
                for p in datos["preguntas"]}
    mensajes.update({f["id"]: f"\n La figura es: {f['texto']}\n{'-' * 40}"
                     for f in datos["figuras"]})
    leer = {p["id"]: input for p in datos["preguntas"]}
    leer.update({f["id"]: (lambda mensaje: print(mensaje) or "") for f in datos["figuras"]})

    textos = {n["id"]: n["texto"] for n in datos["preguntas"] + datos["figuras"]}
    figuras = [f["texto"] for f in datos["figuras"]]
    return mensajes, leer, siguiente, opciones, textos, figuras


def recorrer(mensajes, leer, siguiente, opciones, inicio=0):
    actual = inicio
    while actual in opciones:
        respuesta = normalizar(leer[actual](mensajes[actual]))
        actual = siguiente.get((actual, respuesta), actual)
    return actual


def main():
    mensajes, leer, siguiente, opciones, textos, figuras = cargar_grafo(ARCHIVO)
    print(f"\n ------ F I G U R A S  G E O M E T R I C A S  -  E Q U I P O   N A R A N J A----- ")
    print("Piensa en una figura geométrica y responde las preguntas.")
    print("\nFiguras Geometricas:")
    print("\n".join(f"  - {figura}" for figura in figuras))
    print()
    try:
        print(textos[recorrer(mensajes, leer, siguiente, opciones)])
    except (KeyboardInterrupt, EOFError):
        print("\n¡Hasta luego!")


main()

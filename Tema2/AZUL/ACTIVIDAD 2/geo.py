import json


ARCHIVO_GRAFO = "figuras.json"


with open(ARCHIVO_GRAFO, "r", encoding="utf-8") as archivo:
    Datos = json.load(archivo)


Preguntas = Datos["Preguntas"]
Trans = Datos["Transiciones"]
PPregunta = "A"
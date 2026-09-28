"""Paso 2: calcular el peso de cada pregunta y ordenarlas."""
import json
from math import log2

with open("conocimiento.json", encoding="utf-8") as archivo:
    animales = json.load(archivo)

preguntas = list(next(iter(animales.values())))
total = len(animales)
pesos = {}

for pregunta in preguntas:
    si = sum(datos[pregunta] for datos in animales.values())
    no = total - si
    if si == 0 or no == 0:
        peso = 0.0
    else:
        p = si / total
        peso = -p * log2(p) - (1 - p) * log2(1 - p)
    pesos[pregunta] = round(peso, 4)

orden = sorted(preguntas, key=lambda p: pesos[p], reverse=True)
with open("modelo.json", "w", encoding="utf-8") as archivo:
    json.dump(orden, archivo, ensure_ascii=False, indent=2)

print("Peso de cada pregunta (en bits):")
for pregunta in orden:
    print(f"{pregunta.replace('_', ' '):20} {pesos[pregunta]:.4f}")
print("Preguntas ordenadas en modelo.json")

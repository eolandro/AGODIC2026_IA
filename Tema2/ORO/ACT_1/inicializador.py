"""Paso 1: pasar la tabla de S/N a conocimiento.json."""
import json

caracteristicas = [
    "leal", "vuela", "bigotes", "dientes_grandes", "salta",
    "tranquilo", "pone_huevos", "galopa", "colmillos_largos", "lento",
    "orejas_largas", "semiacuatico",
]

# Primeras diez respuestas: foto del pizarrón. Últimas dos: extras.
tabla = {
    "perro":       "S N S N S N N N S N N N",
    "mariposa":   "N S N N N S S N N N N N",
    "gato":        "N N S N S S N N S N N N",
    "tuza":        "N N S S S S N N N N N N",
    "conejo":      "N N S S S S N N N N S N",
    "capibara":    "N N S S S S N N N N N S",
    "ornitorrinco": "N N N N N S S N N N N S",
    "caballo":     "S N S S S N N S N N N N",
    "mamut":       "N N N N N N N N S N N N",
    "tortuga":     "N N N N N S S N N S N N",
}

animales = {}
for animal, fila in tabla.items():
    respuestas = fila.split()
    if len(respuestas) != len(caracteristicas):
        raise ValueError(f"Revisa la fila de {animal}")
    animales[animal] = dict(zip(caracteristicas, (r == "S" for r in respuestas)))

with open("conocimiento.json", "w", encoding="utf-8") as archivo:
    json.dump(animales, archivo, ensure_ascii=False, indent=2)

print("Tabla guardada en conocimiento.json")

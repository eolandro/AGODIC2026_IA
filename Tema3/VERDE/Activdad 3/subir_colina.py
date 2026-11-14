import json
import random

TAMANO_CACHE = 3
LIMITE_REPETICIONES = 10
with open("caminos.json", encoding="utf-8") as archivo:
    caminos = json.load(archivo)

def elegir_siguiente(actual, estrategia, cache):
    opciones = caminos[actual]
    candidatos = [d for d in opciones if d not in cache]
    if len(candidatos) == 0:
        candidatos = list(opciones)
    if estrategia == "corta":
        mejor = min(opciones[d] for d in candidatos)
    else:
        mejor = max(opciones[d] for d in candidatos)
    empatados = [d for d in candidatos if opciones[d] == mejor]
    return random.choice(empatados)

def recorrer(actual, meta, estrategia, cache, recorrido, repeticiones):
    if actual == meta:
        print("¡Llegó a la meta " + meta + "!")
        return recorrido
    if len(caminos[actual]) == 0:
        print(actual + " no tiene más caminos. No se llegó a la meta.")
        return recorrido
    siguiente = elegir_siguiente(actual, estrategia, cache)
    tramo = actual + "->" + siguiente
    repeticiones[tramo] = repeticiones.get(tramo, 0) + 1
    if repeticiones[tramo] >= LIMITE_REPETICIONES:
        print("⚠ El tramo " + tramo + " se repitió 10 veces. Se detiene.")
        return recorrido
    print(actual + " -> " + siguiente)
    recorrido.append(siguiente)
    nueva_cache = (cache + [actual])[-TAMANO_CACHE:]
    return recorrer(siguiente, meta, estrategia, nueva_cache, recorrido, repeticiones)
def jugar():
    print("Lugares disponibles:", ", ".join(caminos))
    inicio = input("Lugar de inicio: ").strip().upper()
    while inicio not in caminos:
        inicio = input("Ese lugar no existe. Lugar de inicio: ").strip().upper()
    meta = input("Lugar de meta: ").strip().upper()
    while meta not in caminos:
        meta = input("Ese lugar no existe. Lugar de meta: ").strip().upper()
    estrategia = input("Estrategia (corta/larga): ").strip().lower()
    while estrategia != "corta" and estrategia != "larga":
        estrategia = input("Opción inválida. Estrategia (corta/larga): ").strip().lower()
    print("\n=== Estrategia " + estrategia.upper() + " | " + inicio + " -> " + meta + " ===")
    recorrido = recorrer(inicio, meta, estrategia, [], [inicio], {})
    return "Camino recorrido: " + " -> ".join(recorrido)

print("Escribe jugar() para empezar, o q para salir.")
while True:
    command = input(">")
    if command == "q":
        break
    try:
        T = eval(command)
        print(T)
    except Exception as e:
        print("Error:", e)
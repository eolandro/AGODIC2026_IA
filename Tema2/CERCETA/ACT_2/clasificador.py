import json

with open("grafo.json", encoding="utf-8") as archivo:
    grafo = json.load(archivo)

nodos = grafo["nodos"]
transiciones = grafo["transiciones"]
etiquetas = {"s": "s = Sí", "n": "n = No"}

print("ADIVINA LA FIGURA")
print("\nFiguras que puedo identificar:")
for figura in sorted(n["texto"] for n in nodos.values() if n["tipo"] == "resultado"):
    print(" -", figura)
print("\nPiensa en una de ellas y responde las preguntas (escribe salir para terminar).")

otra = "s"
while otra == "s":
    actual = str(grafo["inicio"])
    hechos = []

    while actual in transiciones:
        opciones = transiciones[actual]
        print(f"\nPregunta {len(hechos) + 1}: {nodos[actual]['texto']}")
        print("  Opciones:", ", ".join(etiquetas.get(clave, clave) for clave in opciones))
        respuesta = input("Tu respuesta: ").strip().lower()
        respuesta = {"si": "s", "sí": "s", "no": "n"}.get(respuesta, respuesta)
        if respuesta == "salir":
            break
        if respuesta not in opciones:
            print("Opción no válida.")
            continue
        hechos.append(f"{nodos[actual]['texto']} -> {etiquetas.get(respuesta, respuesta)}")
        actual = str(opciones[respuesta])
    else:
        print(f"\n¡Tu figura es: {nodos[actual]['texto']}!")
        print("\nRazonamiento seguido:")
        for numero, hecho in enumerate(hechos, 1):
            print(f"  {numero}. {hecho}")
        otra = ""
        while otra not in ("s", "n"):
            otra = input("\n¿Quieres adivinar otra figura? (s = sí, n = salir): ").strip().lower()
            otra = {"si": "s", "sí": "s", "no": "n"}.get(otra, otra)
        continue
    break

print("\n¡Hasta la próxima!")

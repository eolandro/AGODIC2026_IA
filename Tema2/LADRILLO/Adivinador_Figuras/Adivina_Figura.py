import json

with open('ramas_grafo.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

preguntas = {int(id_pregunta): texto for id_pregunta, texto in datos["preguntas"].items()}

trans = {(t["origen"], str(t["respuesta"]).strip().lower()): t["destino"] for t in datos["transiciones"]}
nodos_origen = {orig for orig, _ in trans}
figuras = [texto for id_pregunta, texto in preguntas.items() if id_pregunta not in nodos_origen]

jugar = "si"
while jugar == "si":
    print("\n==========================================")
    print("      ¡INICIA EL JUEGO: ADIVINA LA FIGURA!    ")
    print("==========================================")
    print("=== CLASIFICADOR DE FIGURAS GEOMÉTRICAS ===")
    print("Figuras registradas:")
    for fig in figuras:
        print(f" - {fig}")
    print("===========================================\n")

    nodo = datos.get("PPregunta", 0)
    
    while nodo in nodos_origen:
        opciones = [resp for orig, resp in trans if orig == nodo]
        formato = f"[{'/'.join(opciones)}]"
        resp = input(f"{preguntas[nodo]} {formato}: ").strip().lower()
        
        resp = {"s": "si", "n": "no"}.get(resp, resp)
        
        nodo = trans.get((nodo, resp), nodo)

    print(f"\n¡La figura en la que piensas es: {preguntas[nodo]}!")
    jugar = ""
    while jugar not in ["si", "no"]:
        jugar = input("\n¿Deseas volver a jugar? [si/no]: ").strip().lower()

print("\n¡Gracias por jugar! Hasta luego.")
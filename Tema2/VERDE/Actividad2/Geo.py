import json

with open("datos.json", encoding="utf-8") as archivo:
    datos = json.load(archivo)
preguntas = dict(datos["preguntas"])  
transiciones = datos["trans"]         

def tiene_transiciones(nodo):
    for origen, respuesta, destino in transiciones:
        if origen == nodo:
            return True
    return False

def buscar_siguiente(nodo, respuesta_usuario):
    for origen, respuesta, destino in transiciones:
        if origen == nodo and str(respuesta).lower() == respuesta_usuario:
            return destino
    return nodo

print("Figuras que puedo identificar:")
for numero, texto in preguntas.items():
    if not tiene_transiciones(numero):
        print(" -", texto)
nodo_actual = 0  
while tiene_transiciones(nodo_actual):
    pregunta = preguntas[nodo_actual]
    opciones = [str(r) for o, r, d in transiciones if o == nodo_actual]  
    respuesta_usuario = input(pregunta + "? \n " + str(opciones) + ": ").strip().lower()
    nodo_actual = buscar_siguiente(nodo_actual, respuesta_usuario)
figura = preguntas[nodo_actual]  
print("\n Resultado:", figura,"\n")
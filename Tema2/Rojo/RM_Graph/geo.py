import json

EQUIVALENTES = {"s": "si", "n": "no"}


def leer_grafo():
    archivo = open("grafo.json", encoding="utf-8")
    grafo = json.load(archivo)
    archivo.close()
    return grafo


def preparar_grafo(grafo):
    preguntas = dict(grafo["Preguntas"])
    transiciones = {}

    for origen, respuesta, destino in grafo["Trans"]:
        opciones = transiciones.setdefault(origen, {})
        opciones[str(respuesta).lower()] = destino

    return preguntas, transiciones


def mostrar_bienvenida(preguntas, transiciones):
    hojas = sorted(set(preguntas) - set(transiciones))
    nombres = []

    for hoja in hojas:
        texto = preguntas[hoja].replace("Es un ", "").replace("Es ", "")
        nombres.append(texto)

    print()
    print("Soy un adivino de figuras geometricas")
    print("Puedo adivinar estas figuras:")
    print(", ".join(nombres))
    print()
    print("Piensa en una de ellas")
    print("Responde con una de las opciones")


def leer_respuesta():
    respuesta = input("Tu respuesta: ")
    respuesta = respuesta.strip().lower()
    return EQUIVALENTES.get(respuesta, respuesta)


def pedir_respuesta(pregunta, opciones):
    print()
    print(pregunta)
    print("Opciones:", list(opciones))
    respuesta = leer_respuesta()

    while respuesta not in opciones:
        print("Esa opcion no existe, intenta otra vez")
        respuesta = leer_respuesta()

    return respuesta


def adivinar(preguntas, transiciones, inicio):
    actual = inicio

    while actual in transiciones:
        opciones = transiciones[actual]
        respuesta = pedir_respuesta(preguntas[actual], opciones)
        actual = opciones[respuesta]

    return preguntas[actual]


def main():
    grafo = leer_grafo()
    preguntas, transiciones = preparar_grafo(grafo)
    inicio = grafo["PPregunta"]
    otra = "s"

    while otra == "s":
        mostrar_bienvenida(preguntas, transiciones)
        resultado = adivinar(preguntas, transiciones, inicio)
        print()
        print("Resultado:", resultado)
        otra = input("\nJugar otra vez? (s/n): ")
        otra = otra.strip().lower()


main()

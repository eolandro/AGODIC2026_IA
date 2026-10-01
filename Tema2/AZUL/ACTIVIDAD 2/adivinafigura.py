from geo import Preguntas, Trans, PPregunta


def organizar_transiciones(transiciones):
    """Convierte las transiciones en un diccionario key-value."""
    grafo = {}

    for origen, respuesta, destino in transiciones:
        grafo.setdefault(origen, {})[respuesta.upper()] = destino

    return grafo


def solicitar_respuesta(pregunta, opciones):
    """Solicita una respuesta hasta obtener una transición válida."""
    opciones_validas = [opcion.upper() for opcion in opciones]

    while True:
        print(f"\n{pregunta}")
        respuesta = input("> ").strip().upper()

        if respuesta in opciones_validas:
            return respuesta

        print(f"Elige una opción válida: {opciones_validas}")


def adivinar(grafo):
    """Recorre el grafo desde PPregunta hasta encontrar una figura."""
    pregunta_actual = PPregunta

    while pregunta_actual in grafo:
        opciones = list(grafo[pregunta_actual].keys())
        respuesta = solicitar_respuesta(
            Preguntas[pregunta_actual],
            opciones
        )
        pregunta_actual = grafo[pregunta_actual][respuesta]

    return Preguntas[pregunta_actual]


def mostrar_figuras():
    print("- Círculo, Elipse")
    print("- Triángulos: Equilátero, Isósceles, Rectángulo, Escaleno")
    print("- Cuadriláteros: Cuadrado, Rectángulo, Rombo, Trapecio rectángulo")
    print("- Pentágono, Hexágono, Decágono, Estrella")


def main():
    grafo = organizar_transiciones(Trans)

    print('Bienvenido al juego "Adivina la Figura"')
    print("Piensa en una de las siguientes figuras y yo intentaré adivinarla:")
    mostrar_figuras()

    continuar = "S"

    while continuar == "S":
        resultado = adivinar(grafo)
        print(f"\nResultado: {resultado}")

        continuar = solicitar_respuesta(
            "¿Quieres volver a jugar? (Sí/No):",
            ["S", "N"]
        )


if __name__ == "__main__":
    main()
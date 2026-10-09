import json
from pathlib import Path

ARCHIVO_MODELO = Path("modelo_entrenado.json")


def obtener_respuesta(pregunta):
    while True:
        respuesta = input(
            f"{pregunta} [s/n]: "
        ).strip().lower()

        if respuesta in ["s", "si", "sí"]:
            return True

        if respuesta in ["n", "no"]:
            return False

        print("Respuesta inválida. Escribe s o n.")


def recorrer_arbol(nodo, preguntas_realizadas):
    if nodo["tipo"] == "animal":
        print("\n===================================")
        print(f"Creo que el animal es: {nodo['animal']}")
        print("===================================")
        return nodo["animal"]

    if nodo["tipo"] == "empate":
        print("\nNo fue posible distinguir entre:")

        for animal in nodo["animales"]:
            print(f"- {animal}")

        return None

    if nodo["tipo"] == "sin_resultado":
        print("\nNo encontré un animal compatible.")
        return None

    preguntas_realizadas.append({
        "pregunta": nodo["descripcion"],
        "ganancia": nodo["ganancia"]
    })

    respuesta = obtener_respuesta(nodo["descripcion"])

    if respuesta:
        return recorrer_arbol(
            nodo["si"],
            preguntas_realizadas
        )

    return recorrer_arbol(
        nodo["no"],
        preguntas_realizadas
    )


def mostrar_historial(preguntas):
    print("\nPreguntas realizadas:")

    for indice, pregunta in enumerate(preguntas, start=1):
        print(
            f"{indice}. {pregunta['pregunta']} "
            f"(ganancia: {pregunta['ganancia']})"
        )


def main():
    if not ARCHIVO_MODELO.exists():
        print("Error: primero ejecuta inicializador.py y entrenador.py")
        return

    modelo = json.loads(
        ARCHIVO_MODELO.read_text(encoding="utf-8")
    )

    print("===================================")
    print(" SISTEMA EXPERTO: ADIVINA EL ANIMAL")
    print("===================================")
    print(
        f"Entropía inicial del sistema: "
        f"{modelo['entropia_inicial']}"
    )

    preguntas_realizadas = []

    animal = recorrer_arbol(
        modelo["arbol"],
        preguntas_realizadas
    )

    mostrar_historial(preguntas_realizadas)

    print(
        f"\nNúmero total de preguntas: "
        f"{len(preguntas_realizadas)}"
    )

    if animal:
        print(f"Resultado final: {animal}")


if __name__ == "__main__":
    main()
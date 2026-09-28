import json

from entrenador import (
    ARCHIVO_ANIMALES,
    cargar_animales,
    cargar_pesos,
    obtener_preguntas,
    filtrar,
    mejor_pregunta,
)


NOMBRES = {
    "leal": "¿Es leal?",
    "vuela": "¿Vuela?",
    "bigotes": "¿Tiene bigotes?",
    "granja": "¿Es un animal de granja?",
    "salta": "¿Salta?",
    "tranquilo": "¿Es tranquilo?",
    "pone_huevo": "¿Pone huevos?",
    "galopa": "¿Galopa?",
    "cola_larga": "¿Tiene cola larga?",
    "lentitud": "¿Es lento?",
}


def preguntar(texto):
    """Solicita una respuesta válida: S o N."""
    while True:
        respuesta = input(texto + " (S/N): ").strip().upper()

        if respuesta in ("S", "N"):
            return respuesta

        print("Por favor, responde únicamente S o N.")


def mostrar_tabla(animales):
    """Muestra únicamente los nombres de los animales."""
    if not animales:
        print("No hay animales registrados.")
        return

    ancho = max(
        len("Animal"),
        max(len(animal["animal"]) for animal in animales),
    )

    separador = "+-" + "-" * ancho + "-+"

    print(separador)
    print("| " + "Animal".ljust(ancho) + " |")
    print(separador)

    for animal in animales:
        print("| " + animal["animal"].ljust(ancho) + " |")

    print(separador)
    print()


def registrar_animal():
    """Agrega un animal a la base de conocimiento."""
    animales = cargar_animales()

    while True:
        nombre = input("\n¿Qué animal estabas pensando?: ").strip().lower()

        if not nombre:
            print("Escribe el nombre del animal.")
            continue

        if any(
            animal["animal"].strip().lower() == nombre
            for animal in animales
        ):
            print(f"El animal '{nombre}' ya está registrado.")
            print("Revisa sus características en animales.json.")
            return

        break

    nuevo_animal = {"animal": nombre}

    print(f"\nIndica las características de: {nombre}")

    caracteristicas = obtener_preguntas(animales) or list(NOMBRES)

    for caracteristica in caracteristicas:
        nuevo_animal[caracteristica] = preguntar(
            NOMBRES.get(caracteristica, caracteristica)
        )

    animales.append(nuevo_animal)

    with open(ARCHIVO_ANIMALES, "w", encoding="utf-8") as archivo:
        json.dump(
            animales,
            archivo,
            ensure_ascii=False,
            indent=4,
        )

    print(f"\n¡Registrado! Ahora conozco al animal: {nombre}.")
    print("Ejecuta entrenador.py de nuevo para que se tome en cuenta al adivinar.")


def adivinar():
    animales = cargar_animales()

    print("\n=== ADIVINADOR DE ANIMALES ===")

    if not animales:
        print("No hay animales registrados. Ejecuta inicializador.py primero.")
        return

    pesos = cargar_pesos()

    if pesos is None:
        print("No se encontró pesos.json.")
        print("Ejecuta entrenador.py antes de jugar para optimizar las preguntas.")
        return

    orden_global = pesos["orden_preguntas"]
    preguntas_restantes = obtener_preguntas(animales)

    mostrar_tabla(animales)
    print("Piensa en uno de los animales de la tabla.")
    input("Cuando estés listo, presiona ENTER...")

    num_preguntas = 0

    # Preguntar solo características que distingan a los candidatos,
    # eligiendo siempre la más informativa (teoría de la información).
    while len(animales) > 1 and preguntas_restantes:
        pregunta = mejor_pregunta(animales, preguntas_restantes, orden_global)

        if pregunta is None:
            break

        respuesta = preguntar(NOMBRES.get(pregunta, pregunta))
        num_preguntas += 1
        animales = filtrar(animales, pregunta, respuesta)
        preguntas_restantes.remove(pregunta)

        if not animales:
            print("\nNo encontré un animal que coincida con esas respuestas.")
            return

        print(f"Posibilidades restantes: {len(animales)}")

    for candidato in animales:
        animal = candidato["animal"]

        confirmacion = preguntar(
            f"¿El animal que estás pensando es {animal}?"
        )
        num_preguntas += 1

        if confirmacion == "S":
            plural = "s" if num_preguntas != 1 else ""
            print(f"\n¡Adiviné! Tu animal es {animal}.")
            print(f"(Usé {num_preguntas} pregunta{plural})")
            return

    print("\nNo pude adivinar: descartaste todos los animales que coincidían.")

    if preguntar("¿Quieres registrar el animal que pensaste?") == "S":
        registrar_animal()


if __name__ == "__main__":
    adivinar()

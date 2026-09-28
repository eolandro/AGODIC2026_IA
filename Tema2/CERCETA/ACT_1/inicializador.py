import json

ARCHIVO = "animales.json"

CARACTERISTICAS = [
    ("leal", "¿Es leal?"),
    ("vuela", "¿Vuela?"),
    ("bigotes", "¿Tiene bigotes?"),
    ("granja", "¿Es un animal de granja?"),
    ("salta", "¿Salta?"),
    ("tranquilo", "¿Es tranquilo?"),
    ("pone_huevo", "¿Pone huevos?"),
    ("galopa", "¿Galopa?"),
    ("cola_larga", "¿Tiene cola larga?"),
    ("lentitud", "¿Es lento?")
]


def pedir_si_no(pregunta):
    while True:
        respuesta = input(pregunta + " (S/N): ").strip().upper()

        if respuesta == "S" or respuesta == "N":
            return respuesta

        print("Respuesta no válida. Escribe S para Sí o N para No.")


def inicializar():

    print("\n==============================")
    print("      INICIALIZADOR")
    print("==============================")
    print("Registro de animales")
    print()

    # Pedir cantidad de animales
    while True:
        try:
            cantidad = int(
                input("¿Cuántos animales desea registrar? ")
            )

            if cantidad > 0:
                break

            print("La cantidad debe ser mayor que 0.")

        except ValueError:
            print("Escribe un número válido.")

    animales = []

    # Registrar cada animal
    for numero in range(1, cantidad + 1):

        print("\n------------------------------")
        print(f"ANIMAL {numero}")
        print("------------------------------")

        nombre = input("Nombre del animal: ").strip().lower()

        animal = {
            "animal": nombre
        }

        # Preguntar características
        for clave, pregunta in CARACTERISTICAS:

            respuesta = pedir_si_no(pregunta)

            animal[clave] = respuesta

        animales.append(animal)

    # Guardar información en JSON
    with open(ARCHIVO, "w", encoding="utf-8") as archivo:

        json.dump(
            animales,
            archivo,
            ensure_ascii=False,
            indent=4
        )

    print("\n==============================")
    print("REGISTRO COMPLETADO")
    print("==============================")
    print(f"Se registraron {cantidad} animales.")
    print(f"La información se guardó en: {ARCHIVO}")


if __name__ == "__main__":
    inicializar()

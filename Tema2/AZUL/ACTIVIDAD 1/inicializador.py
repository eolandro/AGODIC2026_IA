import os
from utilidades import cargar_json, guardar_json, preguntar_si_no

ARCHIVO_DATOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "animales.json")


DATOS_POR_DEFECTO = {
    "caracteristicas": {
        "colmillos_grandes":         "¿Tiene comillos garndes?",
        "leal":            "¿Es leal a los humanos?",
        "vuela":           "¿Puede volar?",
        "bigotes":         "¿Tiene bigotes?",
        "dientes_grandes": "¿Tiene dientes grandes o prominentes?",
        "salta":           "¿Se desplaza principalmente saltando?",
        "tranquilo":       "¿Es un animal tranquilo o dócil?",
        "pone_huevos":     "¿Pone huevos?",
        "galopa":          "¿Galopa?",
        "cola_larga":      "¿Tiene cola larga?",
        "lentitud":        "¿Es un animal lento?"
    },
    "animales": {
        "Perro":        {"colmillos_grandes": True,  "leal": True,  "vuela": False, "bigotes": True,  "dientes_grandes": False, "salta": True,  "tranquilo": False, "pone_huevos": False, "galopa": False, "cola_larga": True,  "lentitud": False},
        "Mariposa":     {"colmillos_grandes": False, "leal": False, "vuela": True,  "bigotes": False, "dientes_grandes": False, "salta": False, "tranquilo": True,  "pone_huevos": True,  "galopa": False, "cola_larga": False, "lentitud": False},
        "Gato":         {"colmillos_grandes": True,  "leal": False, "vuela": False, "bigotes": True,  "dientes_grandes": False, "salta": True,  "tranquilo": True,  "pone_huevos": False, "galopa": False, "cola_larga": True,  "lentitud": False},
        "Tuza":         {"colmillos_grandes": True,  "leal": False, "vuela": False, "bigotes": True,  "dientes_grandes": True,  "salta": True,  "tranquilo": True,  "pone_huevos": False, "galopa": False, "cola_larga": False, "lentitud": False},
        "Conejo":       {"colmillos_grandes": False, "leal": False, "vuela": False, "bigotes": True,  "dientes_grandes": True,  "salta": True,  "tranquilo": True,  "pone_huevos": False, "galopa": False, "cola_larga": False, "lentitud": False},
        "Capibara":     {"colmillos_grandes": False, "leal": False, "vuela": False, "bigotes": True,  "dientes_grandes": True,  "salta": True,  "tranquilo": True,  "pone_huevos": False, "galopa": False, "cola_larga": False, "lentitud": False},
        "Ornitorrinco": {"colmillos_grandes": True,  "leal": False, "vuela": False, "bigotes": False, "dientes_grandes": False, "salta": False, "tranquilo": True,  "pone_huevos": True,  "galopa": False, "cola_larga": False, "lentitud": False},
        "Caballo":      {"colmillos_grandes": True,  "leal": True,  "vuela": False, "bigotes": True,  "dientes_grandes": True,  "salta": True,  "tranquilo": False, "pone_huevos": False, "galopa": True,  "cola_larga": False, "lentitud": False},
        "Mamut":        {"colmillos_grandes": True,  "leal": False, "vuela": False, "bigotes": False, "dientes_grandes": False, "salta": False, "tranquilo": False, "pone_huevos": False, "galopa": False, "cola_larga": True,  "lentitud": False},
        "Tortuga":      {"colmillos_grandes": False, "leal": False, "vuela": False, "bigotes": False, "dientes_grandes": False, "salta": False, "tranquilo": True,  "pone_huevos": True,  "galopa": False, "cola_larga": False, "lentitud": True}
    }
}


def mostrar_tabla(datos):
    caracteristicas = list(datos["caracteristicas"].keys())
    print("\n" + "-" * 70)
    encabezado = "Animal".ljust(15) + "".join(c[:10].ljust(11) for c in caracteristicas)
    print(encabezado)
    print("-" * 70)
    for animal, attrs in datos["animales"].items():
        fila = animal.ljust(15) + "".join(
            ("Si" if attrs.get(c) else "No").ljust(11) for c in caracteristicas
        )
        print(fila)
    print("-" * 70)
    print(f"Total: {len(datos['animales'])} animales, "
          f"{len(caracteristicas)} características.\n")


def agregar_caracteristica(datos):
    clave = input("Clave interna de la característica (sin espacios, ej. 'nada'): ").strip().lower().replace(" ", "_")
    if not clave:
        print("  -> Clave vacía, se cancela.")
        return
    if clave in datos["caracteristicas"]:
        print("  -> Ya existe esa característica.")
        return
    pregunta = input("Texto de la pregunta que se hará al usuario (ej. '¿Nada?'): ").strip()
    if not pregunta:
        pregunta = f"¿{clave}?"
    datos["caracteristicas"][clave] = pregunta
    # Para no romper la tabla, se pregunta el valor para cada animal existente
    for animal in datos["animales"]:
        datos["animales"][animal][clave] = preguntar_si_no(f"  {animal}: {pregunta}")
    print(f"  -> Característica '{clave}' agregada.")


def agregar_animal(datos):
    nombre = input("Nombre del nuevo animal: ").strip()
    if not nombre:
        print("  -> Nombre vacío, se cancela.")
        return
    if nombre in datos["animales"]:
        print("  -> Ese animal ya existe.")
        return
    attrs = {}
    print(f"Responde las características de '{nombre}':")
    for clave, pregunta in datos["caracteristicas"].items():
        attrs[clave] = preguntar_si_no(f"  {pregunta}")
    datos["animales"][nombre] = attrs
    print(f"  -> Animal '{nombre}' agregado.")


def eliminar_animal(datos):
    nombre = input("Nombre del animal a eliminar: ").strip()
    if nombre in datos["animales"]:
        del datos["animales"][nombre]
        print(f"  -> Animal '{nombre}' eliminado.")
    else:
        print("  -> No se encontró ese animal.")


def editar_pregunta(datos):
    clave = input("Clave interna de la característica a editar: ").strip().lower()
    if clave not in datos["caracteristicas"]:
        print("  -> No existe esa característica.")
        return
    print(f"  Texto actual: {datos['caracteristicas'][clave]}")
    nuevo = input("  Nuevo texto de la pregunta: ").strip()
    if nuevo:
        datos["caracteristicas"][clave] = nuevo
        print("  -> Pregunta actualizada.")


def menu():
    datos = cargar_json(ARCHIVO_DATOS)
    if datos is None:
        print("No existe 'animales.json' todavía.")
        usar_default = preguntar_si_no(
            "¿Cargar el conjunto de animales definido en clase (tabla base) "
            "como punto de partida?"
        )
        datos = DATOS_POR_DEFECTO.copy() if usar_default else {"caracteristicas": {}, "animales": {}}
        # copia profunda simple
        import copy
        datos = copy.deepcopy(datos)


    while True:
        print("\n=== INICIALIZADOR: Supervisor del Sistema Experto ===")
        print("1) Ver tabla de animales y características")
        print("2) Agregar animal")
        print("3) Agregar característica")
        print("4) Editar el texto de una pregunta")
        print("5) Eliminar animal")
        print("6) Guardar y salir")
        print("0) Salir sin guardar")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_tabla(datos)
        elif opcion == "2":
            agregar_animal(datos)
        elif opcion == "3":
            agregar_caracteristica(datos)
        elif opcion == "4":
            editar_pregunta(datos)
        elif opcion == "5":
            eliminar_animal(datos)
        elif opcion == "6":
            if len(datos["animales"]) < 2:
                print("  -> Se necesitan al menos 2 animales para que el "
                      "sistema pueda distinguir. No se guardó.")
                continue
            guardar_json(ARCHIVO_DATOS, datos)
            print(f"  -> Guardado en '{ARCHIVO_DATOS}'.")
            print("  -> Ejecuta ahora 'entrenador.py' para la siguiente etapa.")
            break
        elif opcion == "0":
            print("  -> Saliendo sin guardar cambios.")
            break
        else:
            print("  -> Opción no válida.")


if __name__ == "__main__":
    menu()

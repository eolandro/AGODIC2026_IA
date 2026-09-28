import json
from pathlib import Path

ARCHIVO = Path("animales.json")
DANADO = Path("animales_danado.json")

CARACTERISTICAS = [
    ("granja", "Se encuentra en granja"),
    ("cola_larga", "Cola larga"),
    ("leal", "Leal"),
    ("vuela", "Vuela"),
    ("bigotes", "Bigotes"),
    ("dientes_grandes", "Dientes grandes"),
    ("salta", "Salta"),
    ("tranquilidad", "Tranquilidad"),
    ("pone_huevos", "Pone huevos"),
    ("galopa", "Galopa"),
    ("colmillos_largos", "Colmillos largos"),
    ("lenta", "Lenta"),
]


def preguntar_si_no(texto):
    while True:
        respuesta = input(f"¿{texto}? [s/n]: ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta inválida, escribe s o n.")


def cargar_animales():
    if not ARCHIVO.exists():
        return []
    try:
        animales = json.loads(ARCHIVO.read_text(encoding="utf-8"))
        valido = isinstance(animales, list) and all(
            isinstance(a, dict) and isinstance(a.get("animal"), str) for a in animales
        )
    except json.JSONDecodeError:
        valido = False
    if not valido:
        ARCHIVO.replace(DANADO)
        print(f"No se pudo leer {ARCHIVO}. Se movió a {DANADO} y se empieza con una tabla vacía.")
        return []
    return animales


def guardar_animales(animales):
    ARCHIVO.write_text(json.dumps(animales, ensure_ascii=False, indent=2), encoding="utf-8")


def pedir_cantidad():
    while True:
        try:
            cantidad = int(input("¿Cuántos animales nuevos vas a registrar? "))
        except ValueError:
            print("Escribe un número entero.")
            continue
        if cantidad > 0:
            return cantidad
        print("La cantidad debe ser mayor que 0.")


def pedir_nombre(usados):
    while True:
        nombre = input("Nombre del animal: ").strip().lower()
        if not nombre:
            print("El nombre no puede estar vacío.")
        elif nombre in usados:
            print(f"'{nombre}' ya está registrado, usa otro nombre.")
        else:
            return nombre


def capturar_caracteristicas():
    return {clave: preguntar_si_no(texto) for clave, texto in CARACTERISTICAS}


def main():
    animales = cargar_animales()
    if animales:
        nombres = ", ".join(a["animal"] for a in animales)
        print(f"Animales guardados ({len(animales)}): {nombres}")

    usados = {a["animal"].strip().lower() for a in animales}
    cantidad = pedir_cantidad()

    for i in range(cantidad):
        print(f"\nAnimal {i + 1} de {cantidad}")
        nombre = pedir_nombre(usados)
        usados.add(nombre)
        animales.append({"animal": nombre, "caracteristicas": capturar_caracteristicas()})
        guardar_animales(animales)

    print(f"\nTotal de animales en {ARCHIVO}: {len(animales)}")
    print("Siguiente paso: python3 R002_entrenador.py")


if __name__ == "__main__":
    main()
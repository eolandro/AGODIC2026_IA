import json

ARCHIVO_SALIDA = "animales.json"

CARACTERISTICAS_CLASE = [
    ("COLA LARGA", "tiene", "cola larga"),
    ("LEAL", "es", "leal"),
    ("VUELA", "puede", "volar"),
    ("BIGOTES", "tiene", "bigotes"),
    ("DIENTES GRANDES", "tiene", "dientes grandes"),
    ("SALTA", "puede", "saltar"),
    ("TRANQUILO", "es", "tranquilo"),
    ("PONE HUEVO", "pone", "huevos"),
    ("GALOPA", "puede", "galopar"),
    ("COLMILLOS LARGOS", "tiene", "colmillos largos"),
    ("LENTA", "es", "lento"),
]

ANIMALES_CLASE = {
    "perro":        ["COLA LARGA", "LEAL", "BIGOTES", "SALTA", "COLMILLOS LARGOS"],
    "mariposa":     ["VUELA", "TRANQUILO", "PONE HUEVO"],
    "gato":         ["COLA LARGA", "BIGOTES", "SALTA", "TRANQUILO", "COLMILLOS LARGOS"],
    "tuza":         ["COLA LARGA", "BIGOTES", "DIENTES GRANDES", "SALTA", "TRANQUILO"],
    "conejo":       ["BIGOTES", "DIENTES GRANDES", "SALTA", "TRANQUILO"],
    "capibara":     ["BIGOTES", "DIENTES GRANDES", "SALTA", "TRANQUILO"],
    "ornitorrinco": ["COLA LARGA", "TRANQUILO", "PONE HUEVO"],
    "caballo":      ["COLA LARGA", "LEAL", "BIGOTES", "DIENTES GRANDES", "SALTA", "GALOPA"],
    "mamut":        ["COLA LARGA", "COLMILLOS LARGOS"],
    "tortuga":      ["TRANQUILO", "PONE HUEVO", "LENTA"],
}


def leer(mensaje):
    return input(mensaje).strip()


def si_no(mensaje):
    while True:
        r = leer(mensaje + " (s/n): ").lower()
        if r in ("s", "si", "sí"):
            return True
        if r in ("n", "no"):
            return False


def cargar_tabla_clase():
    caracteristicas = [{"nombre": n, "relacion": r, "valor": v}
                       for n, r, v in CARACTERISTICAS_CLASE]
    return caracteristicas, dict(ANIMALES_CLASE)


CANTIDAD_ANIMALES = 10

VERBOS = ("es", "tiene", "puede", "pone", "vive", "come", "hace", "usa")


def pedir_caracteristica(animal):
    while True:
        texto = leer(f"  ¿Que caracteristica tiene {animal}? "
                     "(ej. tiene alas, es miedoso, puede volar): ").lower()
        partes = texto.split(" ", 1)
        if len(partes) == 2 and partes[0] in VERBOS and partes[1].strip():
            return partes[0], partes[1].strip()
        print("  Escribela empezando con un verbo: " + ", ".join(VERBOS)
              + "  (ej. 'tiene garras')")


def pedir_numeros(mensaje, maximo):
    while True:
        texto = leer(mensaje)
        if texto == "":
            return set()
        try:
            numeros = {int(x) for x in texto.replace(" ", "").split(",") if x}
        except ValueError:
            print("  Solo numeros separados por coma, ej. 1,4,7")
            continue
        if all(1 <= x <= maximo for x in numeros):
            return numeros
        print(f"  Los numeros van del 1 al {maximo}.")


def capturar_desde_cero():
    print(f"\nPiensa en {CANTIDAD_ANIMALES} animales y una caracteristica de cada uno.")

    animales = {}
    caracteristicas = []
    while len(animales) < CANTIDAD_ANIMALES:
        print(f"\nAnimal {len(animales) + 1} de {CANTIDAD_ANIMALES}")
        animal = leer("  Nombre del animal: ").lower()
        if animal == "":
            print("  El nombre no puede ir vacio.")
            continue
        if animal in animales:
            print("  Ese animal ya esta.")
            continue
        relacion, valor = pedir_caracteristica(animal)
        nombre = f"{relacion} {valor}".upper()
        if any(c["nombre"] == nombre for c in caracteristicas):
            print(f"  {nombre} ya existia, se marca tambien para {animal}.")
        else:
            caracteristicas.append({"nombre": nombre, "relacion": relacion, "valor": valor})
        animales[animal] = [nombre]

    if not si_no("\n¿Algun animal comparte alguna de estas caracteristicas con otro?"):
        return caracteristicas, animales
    lista = list(animales)
    print("\n--- Completar la tabla ---")
    for i, animal in enumerate(lista, start=1):
        print(f"  {i}. {animal}")
    for c in caracteristicas:
        ya = [a for a in lista if c["nombre"] in animales[a]]
        print(f"\n'{c['nombre']}'  (ya la tiene: {', '.join(ya)})")
        numeros = pedir_numeros("  ¿Que otros animales la tienen? "
                                "(numeros separados por coma, Enter = ninguno): ",
                                len(lista))
        for x in numeros:
            animal = lista[x - 1]
            if c["nombre"] not in animales[animal]:
                animales[animal].append(c["nombre"])
    return caracteristicas, animales


def mostrar_tabla(caracteristicas, animales):
    nombres = [c["nombre"] for c in caracteristicas]
    k = len(nombres)
    peso = {nom: 2 ** (k - 1 - i) for i, nom in enumerate(nombres)}
    letras = [chr(65 + i) for i in range(k)]
    ancho_animal = max(len("VALOR"), *(len(a) for a in animales))
    ancho = max(len(str(peso[nombres[0]])), 1) + 1
    ancho_total = len(str(sum(peso.values()))) + 2

    print("\n" + "ANIMAL".ljust(ancho_animal) + "".join(l.rjust(ancho) for l in letras)
          + "total".rjust(ancho_total + 1))
    print("-" * (ancho_animal + ancho * k + ancho_total))
    for animal, rasgos in animales.items():
        valores = [peso[nom] if nom in rasgos else 0 for nom in nombres]
        print(animal.upper().ljust(ancho_animal)
              + "".join(str(v).rjust(ancho) for v in valores)
              + str(sum(valores)).rjust(ancho_total))
    print("-" * (ancho_animal + ancho * k + ancho_total))
    print("VALOR".ljust(ancho_animal) + "".join(str(peso[nom]).rjust(ancho) for nom in nombres)
          + str(sum(peso.values())).rjust(ancho_total))

    print()
    for letra, nom in zip(letras, nombres):
        print(f"  {letra} = {nom} ({peso[nom]})")


def revisar_iguales(animales):
    vistos = {}
    for animal, rasgos in animales.items():
        firma = frozenset(rasgos)
        if firma in vistos:
            print(f"AVISO: '{animal}' y '{vistos[firma]}' tienen exactamente las mismas "
                  "caracteristicas; el adivinador los separara preguntando por nombre.")
        else:
            vistos[firma] = animal


def main():
    print("=== I N I C I A L I Z A D O R   E Q U I P O   N A R A N J A ===")
    print("1) Cargar la tabla de la clase")
    print("2) Capturar desde cero")
    opcion = leer("Opcion: ")

    if opcion == "1":
        caracteristicas, animales = cargar_tabla_clase()
    else:
        caracteristicas, animales = capturar_desde_cero()

    if len(caracteristicas) < 1 or len(animales) < 2:
        print("Se necesita al menos 1 caracteristica y 2 animales. No se guardo nada.")
        return

    with open(ARCHIVO_SALIDA, "w", encoding="utf-8") as f:
        json.dump({"caracteristicas": caracteristicas, "animales": animales},
                  f, indent=2, ensure_ascii=False)
    print(f"\nTabla registrada: {len(animales)} animales y {len(caracteristicas)} "
          f"caracteristicas guardados en {ARCHIVO_SALIDA}")

    mostrar_tabla(caracteristicas, animales)

    revisar_iguales(animales)


if __name__ == "__main__":
    main()

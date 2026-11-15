import json
import os
import sys

TAM_CACHE = 3
MAX_PASOS = 50
ARCHIVO_GRAFO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "grafo.json")


def cargar_grafo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No se encontro el archivo: {ruta}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"El archivo JSON no es valido: {e}")
        sys.exit(1)


def pedir_opcion(mensaje, opciones):
    """Muestra una lista numerada y devuelve la opcion elegida."""
    print(f"\n{mensaje}")
    for i, op in enumerate(opciones, start=1):
        print(f"  {i}) {op}")
    while True:
        entrada = input("Selecciona una opcion: ").strip()
        if entrada.isdigit() and 1 <= int(entrada) <= len(opciones):
            return opciones[int(entrada) - 1]
        print("Opcion invalida, intenta de nuevo.")


def formatear_cache(cache):
    return "(" + ", ".join(cache) + ")" if cache else "()"


def subir_la_colina(grafo, raiz, meta, estrategia):
    """
    estrategia: 1 = corta (menor peso), 2 = larga (mayor peso)
    """
    nombre = "CORTA (menor peso)" if estrategia == 1 else "LARGA (mayor peso)"
    elegir = min if estrategia == 1 else max

    actual = raiz
    cache = []
    paso = 0

    print("\n" + "=" * 60)
    print(f"Estrategia: {nombre} | Raiz: {raiz} | Buscando: {meta}")
    print(f"Cache de {TAM_CACHE} letras | Maximo de {MAX_PASOS} pasos")
    print("=" * 60)

    while True:
        vecinos = grafo[actual]

        print(f"\n--- Paso {paso} ---")
        print(f"Letra actual: {actual}")

        # Caminos disponibles (se marcan los bloqueados por el cache)
        disponibles = {v: w for v, w in vecinos.items() if v not in cache}
        bloqueados = {v: w for v, w in vecinos.items() if v in cache}

        texto_disp = ", ".join(f"{v}({w})" for v, w in disponibles.items()) or "ninguno"
        print(f"Caminos disponibles: {texto_disp}")
        if bloqueados:
            texto_bloq = ", ".join(f"{v}({w})" for v, w in bloqueados.items())
            print(f"Caminos bloqueados por el cache: {texto_bloq}")

        # Condicion de exito
        if actual == meta:
            print(f"\nCamino que va a tomar: ninguno (ya se encontro la letra)")
            print(f"Cache actual: {formatear_cache(cache)}")
            print("\nTrue")
            return True

        # Limite de pasos
        if paso >= MAX_PASOS:
            print("\nFalse")
            return False

        # Sin movimientos posibles
        if not disponibles:
            print("Camino que va a tomar: ninguno")
            print(f"Cache actual: {formatear_cache(cache)}")
            print("\nFalse")
            return False

        # Seleccion greedy: menor o mayor peso (en empate gana el primero del JSON)
        siguiente = elegir(disponibles, key=lambda v: disponibles[v])
        peso = disponibles[siguiente]
        print(f"Camino que va a tomar: {actual} -> {siguiente} (peso {peso})")

        # Actualizar cache: entra la letra que se deja, sale la mas antigua
        cache.append(actual)
        if len(cache) > TAM_CACHE:
            cache.pop(0)
        print(f"Cache actual: {formatear_cache(cache)}")

        actual = siguiente
        paso += 1


def main():
    grafo = cargar_grafo(ARCHIVO_GRAFO)
    letras = list(grafo.keys())

    estrategia_txt = pedir_opcion(
        "¿Deseas hacerlo por la estrategia corta o larga?",
        ["Estrategia corta", "Estrategia larga"],
    )
    estrategia = 1 if estrategia_txt == "Estrategia corta" else 2

    raiz = pedir_opcion("¿Cual va a ser tu raiz?", letras)

    restantes = [l for l in letras if l != raiz]
    meta = pedir_opcion("¿Cual es la letra a buscar?", restantes)

    subir_la_colina(grafo, raiz, meta, estrategia)


if __name__ == "__main__":
    main()
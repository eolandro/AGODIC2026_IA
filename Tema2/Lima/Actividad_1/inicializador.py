import json
from pathlib import Path

CARPETA = Path(__file__).parent
ARCHIVO_RED = CARPETA / "red_semantica.json"

CARACTERISTICAS = [
    ("es",     "leal",             "¿Es considerado un animal leal?"),
    ("puede",  "volar",            "¿Puede volar?"),
    ("tiene",  "bigotes",          "¿Tiene bigotes?"),
    ("tiene",  "dientes grandes",  "¿Tiene dientes grandes?"),
    ("puede",  "saltar",           "¿Puede saltar?"),
    ("es",     "tranquilo",        "¿Generalmente es tranquilo?"),
    ("pone",   "huevos",           "¿Pone huevos?"),
    ("puede",  "galopar",          "¿Puede galopar?"),
    ("tiene",  "colmillos largos", "¿Tiene colmillos largos?"),
    ("es",     "lento",            "¿Se mueve lentamente?"),
    ("es",     "mascota común",    "¿Es una mascota común en las casas?"),
    ("excava", "túneles",          "¿Excava túneles o madrigueras?"),
]

TABLA = {
    "Perro":        "1 0 1 0 1 0 0 0 1 0 1 0",
    "Mariposa":     "0 1 0 0 0 1 1 0 0 0 0 0",
    "Gato":         "0 0 1 0 1 1 0 0 1 0 1 0",
    "Tuza":         "0 0 1 1 1 1 0 0 0 0 0 1",
    "Conejo":       "0 0 1 1 1 1 0 0 0 0 1 1",
    "Capibara":     "0 0 1 1 1 1 0 0 0 0 0 0",
    "Ornitorrinco": "0 0 0 0 0 1 1 0 0 0 0 1",
    "Caballo":      "1 0 1 1 1 0 0 1 0 0 0 0",
    "Mamut":        "0 0 0 0 0 0 0 0 1 0 0 0",
    "Tortuga":      "0 0 0 0 0 1 1 0 0 1 1 0",
}


def inicializar():
    total = len(CARACTERISTICAS)
    pesos = [2 ** (total - 1 - i) for i in range(total)]

    caracteristicas = []
    for i, (relacion, objeto, pregunta) in enumerate(CARACTERISTICAS):
        caracteristicas.append({
            "relacion": relacion,
            "objeto": objeto,
            "pregunta": pregunta,
            "peso": pesos[i],
        })

    animales = []
    arcos = []
    vistos = {}

    print(f"{'Animal':13} | {'Binario':12} | Valor agregado")
    print("-" * 45)
    for nombre, fila in TABLA.items():
        valores = [int(v) for v in fila.split()]
        if len(valores) != total:
            raise ValueError(f"La fila de {nombre} debe tener {total} valores.")

        binario = "".join(str(v) for v in valores)
        valor_agregado = sum(p for p, v in zip(pesos, valores) if v == 1)

        arcos.append([nombre, "es_un", "animal"])
        for (relacion, objeto, _), valor in zip(CARACTERISTICAS, valores):
            if valor == 1:
                arcos.append([nombre, relacion, objeto])

        if valor_agregado in vistos:
            print(f"AVISO: {nombre} y {vistos[valor_agregado]} son idénticos; "
                  "no se podrán distinguir.")
        vistos[valor_agregado] = nombre

        animales.append({
            "nombre": nombre,
            "valores": valores,
            "binario": binario,
            "valor_agregado": valor_agregado,
        })
        print(f"{nombre:13} | {binario} | {valor_agregado}")

    red = {"caracteristicas": caracteristicas, "animales": animales, "arcos": arcos}
    with open(ARCHIVO_RED, "w", encoding="utf-8") as archivo:
        json.dump(red, archivo, ensure_ascii=False, indent=2)

    print(f"\nRed semántica: {len(animales)} animales, {len(arcos)} arcos.")
    print(f"Guardada en {ARCHIVO_RED.name}")


if __name__ == "__main__":
    inicializar()

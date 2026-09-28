import json
import os

ArchivoSalida = "animales.json"

def texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El espacio no puede estar vacío, ingresa un texto válido :()")

def AñadirMás(mensaje):
    while True:
        valor = input(mensaje).strip().upper()
        if valor in ("S", "N"):
            return valor
        print("Respuesta inválida, ingresa 'S' para Sí o 'N' para No. :)")

def guardar_json(registros, ruta=ArchivoSalida):
    data = {"tabla_animales": registros}
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return os.path.abspath(ruta)

#-------------------------------------- MAIN --------------------------------------#
registros = []
nombres_existentes = set()
caracteristicas_existentes = set()
print("* * * INICIALIZADOR: Registro de animales y su característica * * *\n")

while True:
    print(f"--- Animal #{len(registros) + 1} ---")
    nombre = texto("Nombre del animal: ")

    if nombre in nombres_existentes:
        print(f"'{nombre}' ya está registrado, ingresa un nombre distinto.\n")
        continue
    característica = texto(
        f"Cuál es la característica propia de '{nombre}'?: ")

    if característica in caracteristicas_existentes:
        print("Esa característica ya existe, ingresa una distinta.\n")
        continue
    registros.append({"animal": nombre, "caracteristica": característica})
    nombres_existentes.add(nombre)
    caracteristicas_existentes.add(característica)
    otro = AñadirMás("\n¿Deseas añadir otro animal? (S/N): ")
    if otro == "N":
        break

if not registros:
    print("No se registró ningún animal. No se generó archivo.")
else:
    ruta_final = guardar_json(registros)

    print("\n----- Registro finalizado -----")
    print(f"Animales registrados ({len(registros)}):")
    for r in registros:
        print(f"  - {r['animal']}, {r['caracteristica']}")
    print(f"\nArchivo JSON generado en: {ruta_final}")
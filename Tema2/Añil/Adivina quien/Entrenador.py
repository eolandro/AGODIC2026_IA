import json
import os

ArchivoEntrada = "animales.json"
ArchivoSalida = "tabla_pesos.json"

def texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("El espacio no puede estar vacío, ingresa un texto válido :(")

def si_no(mensaje):
    while True:
        valor = input(mensaje).strip().upper()
        if valor in ("S", "N"):
            return valor
        print("Respuesta inválida, ingresa 'S' para Sí o 'N' para No. :)")

def cargar_json(ruta):
    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_json(data, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return os.path.abspath(ruta)

def calcular_sumas(animales, respuestas, pesos):
    sumas = {}
    for animal in animales:
        sumas[animal] = sum(
            pesos[car] for car, val in respuestas[animal].items() if val == "S")
    return sumas

def encontrar_grupo_empatado(sumas):
    grupos = {}
    for animal, suma in sumas.items():
        grupos.setdefault(suma, []).append(animal)
    grupos_grandes = [g for g in grupos.values() if len(g) >= 3]
    if not grupos_grandes:
        return None
    return grupos_grandes[0]

#-------------------------------------- MAIN --------------------------------------#
datos = cargar_json(ArchivoEntrada)
tabla_animales = datos["tabla_animales"]
animales = [r["animal"] for r in tabla_animales]
caracteristicas_propias = [r["caracteristica"] for r in tabla_animales]
N0 = len(caracteristicas_propias)

pesos = {}
for i, característica in enumerate(caracteristicas_propias):
    pesos[característica] = 2 ** (N0 - 1 - i)

respuestas = {animal: {} for animal in animales}
for r in tabla_animales:
    respuestas[r["animal"]][r["caracteristica"]] = "S"

print("* * * ENTRENADOR: Cálculo de pesos * * *\n")
print("Ahora responde, para cada animal, si cumple o no con las demás características.")

for animal in animales:
    print(f"\n----- {animal} -----")
    for característica in caracteristicas_propias:
        if característica not in respuestas[animal]:
            resp = si_no(f"¿Cumple con: '{característica}'? (S/N): ")
            respuestas[animal][característica] = resp

while True:
    sumas = calcular_sumas(animales, respuestas, pesos)
    grupo = encontrar_grupo_empatado(sumas)
    if grupo is None:
        break

    print(f"\n¡Empate detectado entre {len(grupo)} animales!: {', '.join(grupo)}")
    nueva_car = texto("Escribe una característica extra para desempatar: ")
    if nueva_car in pesos:
        print("Esa característica ya existe, ingresa una distinta.\n")
        continue

    nuevo_peso = 2 ** len(pesos)
    pesos[nueva_car] = nuevo_peso
    print(f"\nResponde para TODOS los animales la nueva característica: '{nueva_car}'")
    for animal in animales:
        resp = si_no(f"¿{animal} cumple con: '{nueva_car}'? (S/N): ")
        respuestas[animal][nueva_car] = resp

sumas = calcular_sumas(animales, respuestas, pesos)
caracteristicas_ordenadas = sorted(pesos.items(), key=lambda par: -par[1])
tabla_final = []
for animal in animales:
    fila = {"animal": animal}
    for característica, peso in caracteristicas_ordenadas:
        fila[característica] = respuestas[animal][característica]
    fila["suma_total"] = sumas[animal]
    tabla_final.append(fila)

resultado = {
    "caracteristicas": [{"nombre": c, "peso": p} for c, p in caracteristicas_ordenadas],
    "tabla": tabla_final,
}

ruta_final = guardar_json(resultado, ArchivoSalida)

print("\n----- Cálculo finalizado -----")
for fila in tabla_final:
    print(f"  - {fila['animal']}: suma total = {fila['suma_total']}")
grupos_finales = {}
for animal, suma in sumas.items():
    grupos_finales.setdefault(suma, []).append(animal)
for suma, animales_grupo in grupos_finales.items():
    if len(animales_grupo) > 1:
        print(f"  * Empate de {len(animales_grupo)} sin resolver (se decidirá al azar en el juego): {', '.join(animales_grupo)}")
print(f"\nArchivo JSON generado en: {ruta_final}")
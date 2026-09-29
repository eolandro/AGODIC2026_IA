import json 
archivo = open("Tabla_Animales_Características.json", "r", encoding="utf-8")
info_recabada = json.load(archivo)
archivo.close()

animales = info_recabada["animales"]
caracteristicas = info_recabada["caracteristicas"]

print("\n Datos cargados correctamente desde el archivo 'Tabla_Animales_Caracteristicas.json': ")
print("Animales: ", animales)
print("Caracteristicas: ", caracteristicas)

pesos = []
TotalCaract = len(caracteristicas)

for i in range(TotalCaract):
    potencia = TotalCaract - 1 - i
    peso_columna = 2 ** potencia
    pesos.append(peso_columna)

print("\nPesos binarios asignados a cada caracteristica: ")
for i in range(TotalCaract):
    print("- " + caracteristicas[i] + ": " + str(pesos[i]))

print("\nPor cada pregunta responder (1 = SI , 0 = NO) SOLO EL NUMERO ")
cap_resp = {}
TotalPesos = {}

for animal in animales:
    print("\n ********** RESPUESTAS PARA : "+ animal + " *************\n")
    respuestas_animal = []
    suma_peso = 0

    for i in range(TotalCaract):
        carac = caracteristicas[i]
        peso_actual = pesos[i]

        while True:
            resp = input("Tiene/cumple con la caracteristica " + carac + " : ").strip()

            if resp == "1":
                respuestas_animal.append(1)
                suma_peso = suma_peso + peso_actual
                break
            elif resp == "0":
                respuestas_animal.append(0)
                break
            else:
                print("Respuesta no valida. Debe ser exclusivamente 1 (SI) o 0 (NO)")

    cap_resp[animal] = respuestas_animal
    TotalPesos[animal] = suma_peso
    print("Peso total de " + animal + ":" + str(suma_peso))


hay_empate = True

while hay_empate:
    print("\n--- RESUMEN ACTUAL DE PESOS TOTALES ---")
    for animal in animales:
        print(animal + " => " + str(TotalPesos[animal]))

    pesos_vistos = []
    pesos_repetidos = []

    for animal in animales:
        peso = TotalPesos[animal]
        if peso in pesos_vistos and peso not in pesos_repetidos:
            pesos_repetidos.append(peso)
        pesos_vistos.append(peso)

    if len(pesos_repetidos) == 0:
        hay_empate = False
        print("\n ¡Excelente! Todos los animales tienen pesos únicos.")
    else:
        pesos_iguales = pesos_repetidos[0]
        
        animales_empatados = []
        for animal in animales:
            if TotalPesos[animal] == pesos_iguales:
                animales_empatados.append(animal)
                
        print("\n****************************************")
        print("¡ATENCIÓN! Los siguientes animales tienen el mismo peso (" + str(pesos_iguales) + "): ", animales_empatados)
        print("******************************************")

        while True:
            new_carac = input("Ingrese una NUEVA caracteristica\n SOLO INGRESE LA PALABRA CLAVE: ").strip()
            if new_carac == "":
                print("La caracteristica no puede estar vacia.")
            elif new_carac in caracteristicas:
                print("Esa caracteristica ya existe. Ingrese otra. ")
            else:
                break

        caracteristicas.insert(0, new_carac)

        pesos = []
        TotalCaract = len(caracteristicas)
        for i in range(TotalCaract):
            potencia = TotalCaract - 1 - i
            peso_columna = 2 ** potencia 
            pesos.append(peso_columna)

        print("\nEvaluando la nueva característica '" + new_carac + "':")
        for animal in animales:
            while True:
                resp = input(animal + " tiene/cumple con la caracteristica " + new_carac + " ? ").strip()
                if resp == "1":
                    cap_resp[animal].insert(0, 1)
                    break
                elif resp == "0":
                    cap_resp[animal].insert(0, 0)
                    break
                else:
                    print("Respuesta no valida, debe ser 1 o 0")

        for animal in animales:
            suma_peso = 0
            for i in range(len(caracteristicas)):
                if cap_resp[animal][i] == 1:
                    suma_peso = suma_peso + pesos[i]
            TotalPesos[animal] = suma_peso


print("\n==========================================================================================")
print("                                MATRIZ FINAL DE PESOS DE ENTRENAMIENTO                   ")
print("==========================================================================================")

encabezado = f"{'ANIMAL':<15}"
for carac in caracteristicas:
    encabezado += f" | {carac[:10]:^10}"  # Recorta texto si supera 10 caracteres
encabezado += " | TOTAL"
print(encabezado)
print("-" * len(encabezado))

linea_pesos = f"{'PESO BINARIO':<15}"
for p in pesos:
    linea_pesos += f" | {p:^10}"

linea_pesos += " | --"
print(linea_pesos)
print("-" * len(encabezado))

for animal in animales:
    fila = f"{animal:<15}"
    for resp in cap_resp[animal]:
        fila += f" | {resp:^10}"
    fila += f" | {TotalPesos[animal]:^5}"
    print(fila)

print("=" * len(encabezado))


modelo_entrenado = {
    "caracteristicas": caracteristicas,
    "pesos_caracteristicas": pesos,
    "animales": cap_resp,
    "pesos_totales": TotalPesos
}

archivo_salida = open("TablaPesos.json", "w", encoding="utf-8")
json.dump(modelo_entrenado, archivo_salida, indent=4, ensure_ascii=False)
archivo_salida.close()

print("\n¡Éxito! Datos exportados correctamente a 'TablaPesos.json'")
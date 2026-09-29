import json 

def cargar_datos():
    try:
        archivo = open("TablaPesos.json", "r", encoding="utf-8")
        datos = json.load(archivo)
        archivo.close()
        return datos
    except FileNotFoundError:
        print("No se encontró el archivo 'TablaPesos.json'")
        return None

def selec_carac(candidatos, carac_rest, map_res):
    total_cand = len(candidatos)
    mejor_carac = carac_rest[0]
    menor_dif = total_cand + 1

    for carac in carac_rest:
        con_si = 0
        for animal in candidatos:
            if map_res[animal][carac] == 1:
                con_si += 1

        con_no = total_cand - con_si
        diferencia = abs(con_si - con_no)

        if diferencia < menor_dif:
            menor_dif = diferencia
            mejor_carac = carac
            
    return mejor_carac

def jugar():
    datos = cargar_datos()
    if datos is None:
        return

    lista_caracteristicas = datos["caracteristicas"]
    mapa_animales_vector = datos["animales"]

    map_res = {}
    for animal, vector in mapa_animales_vector.items():
        map_res[animal] = {}
        for i in range(len(lista_caracteristicas)):
            carac = lista_caracteristicas[i]
            map_res[animal][carac] = vector[i]

    while True:
        print("\n==========================================")
        print("      ¡INICIA EL JUEGO: ADIVINA QUIÉN!    ")
        print("==========================================")
        
        candidatos = list(map_res.keys())
        print("Animales disponibles:", candidatos)
        
        carac_rest = list(lista_caracteristicas)
        num_preg = 1

        while len(candidatos) > 1 and len(carac_rest) > 0:
            mejor_carac = selec_carac(candidatos, carac_rest, map_res)
            
            while True:
                resp = input("¿Cumple con la caracteristica o tiene " + mejor_carac + " (S|N): ").strip().upper()
                if resp in ["S", "N"]:
                    break
                print("Respuesta no válida. Ingrese S o N.")

            val_esp = 1 if resp == "S" else 0

            nuevos_cand = []
            for animal in candidatos:
                if map_res[animal][mejor_carac] == val_esp:
                    nuevos_cand.append(animal)
            
            candidatos = nuevos_cand
            carac_rest.remove(mejor_carac)
            num_preg += 1

        print("\n==========================================")
        if len(candidatos) == 1:
            print(" Tu animal es: " + candidatos[0])
        elif len(candidatos) == 0:
            print(" No se encontró ningún animal con esas características.")
        else:
            print(" Quedaron opciones posibles: ", candidatos)
        print("==========================================")

        opcion = input("\n¿Desea volver a jugar? (S/N): ").strip().upper()
        if opcion != "S":
            print("¡Juego terminado!")
            break

if __name__ == "__main__":
    jugar()
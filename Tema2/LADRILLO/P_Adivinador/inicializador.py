import json 

total_animales = int(input("\n Cuántos animales desea agregar: "))

lista_animales = []

for i in range(total_animales):
    while True:
        nombre_animal = input("\n Ingrese el nombre del animal "+ str(i + 1) + ": ")
        #if nombre_animal in lista_animales:
        if nombre_animal == "":
            print("Por favor, ingrese un nombre no debe dejar en blanco el nombre del animal.")
        elif nombre_animal in lista_animales:
            print("\n El animal ya ha sido agregado. Por favor, ingrese otro nombre.")
        else:
            lista_animales.append(nombre_animal)
            break
print("Animales agregados correctamente")
print(lista_animales)

print("\n A continuación, ingrese las caracteristícas de cada animal: ")
print("\nPor ejemplo si el animal es un perro, una caracteristica puede ser que tiene 'cola' o es 'peludo' \n Solo ingrese la palabra clave.\n")

lista_caracteristicas = []

for animal in lista_animales:
    while True:
        caracteristica = input("\n Ingrese la caracteristica del animal " + animal + ": ")
        if caracteristica == "":
            print("\n Por favor, ingrese una caracteristica no debe dejar en blanco la caracteristica del animal.")
        elif caracteristica in lista_caracteristicas:
            print("\n La caracteristica ya ha sido agregada. Por favor, ingrese otra caracteristica.")
        else:
            lista_caracteristicas.append(caracteristica)
            break
print("\n Caracteristicas agregadas correctamente")
print(lista_caracteristicas)


datos = {
    "animales": lista_animales,
    "caracteristicas": lista_caracteristicas
}

file = open("Tabla_Animales_Características.json", "w",encoding="utf-8")
json.dump(datos, file)
file.close()


print(" ¡Listo! Archivo 'Tabla_Animales_Características.json' generado.")

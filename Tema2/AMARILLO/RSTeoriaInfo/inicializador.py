import json


class Animal:
    def __init__(self, nombre, valores, pesos):
        self.nombre = nombre
        self.valores = valores
        self.pesos = pesos

    def calcular_binario(self):
        binario = ""
        for valor in self.valores:
            binario = binario + str(valor)
        return binario

    def calcular_valor(self):
        valor_agregado = 0
        for posicion in range(len(self.valores)):
            if self.valores[posicion] == 1:
                valor_agregado = valor_agregado + self.pesos[posicion]
        return valor_agregado


caracteristicas = [
    "Se encuentra en granja",
    "Cola larga",
    "Leal",
    "Vuela",
    "Bigotes",
    "Dientes grandes",
    "Salta",
    "Tranquilidad",
    "Pone huevos",
    "Galopa",
    "Colmillos largos",
    "Lenta"
]
pesos = [2048, 1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]
animales = {
    "Perro":        [1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    "Mariposa":     [1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0],
    "Gato":         [1, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0],
    "Tuza":         [0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    "Conejo":       [1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    "Capibara":     [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
    "Ornitorrinco": [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
    "Caballo":      [1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0],
    "Mamut":        [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    "Tortuga":      [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1]
}
base_conocimiento = {
    "caracteristicas": caracteristicas,
    "pesos": pesos,
    "animales": []
}
print("Animal | Binario | Valor agregado")
for nombre in animales:
    objeto_animal = Animal(nombre, animales[nombre], pesos)
    binario = objeto_animal.calcular_binario()
    valor_agregado = objeto_animal.calcular_valor()
    animal = {
        "nombre": objeto_animal.nombre,
        "valores": objeto_animal.valores,
        "binario": binario,
        "valor_agregado": valor_agregado
    }
    base_conocimiento["animales"].append(animal)
    print(nombre, "|", binario, "|", valor_agregado)
with open("base_conocimiento.json", "w", encoding="utf-8") as archivo:
    json.dump(base_conocimiento, archivo, ensure_ascii=False, indent=4)
print("\nBase de conocimiento guardada en base_conocimiento.json")

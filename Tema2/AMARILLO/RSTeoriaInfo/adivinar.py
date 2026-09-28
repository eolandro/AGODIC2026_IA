import json


class Adivinador:
    def __init__(self):
        with open("base_conocimiento.json", "r", encoding="utf-8") as archivo:
            self.base_conocimiento = json.load(archivo)
        with open("entrenamiento.json", "r", encoding="utf-8") as archivo:
            self.entrenamiento = json.load(archivo)
        self.animales = self.base_conocimiento["animales"]
        self.caracteristicas = self.base_conocimiento["caracteristicas"]
        self.pesos = self.base_conocimiento["pesos"]
        self.preguntas = {}
        for resultado in self.entrenamiento:
            self.preguntas[resultado["caracteristica"]] = resultado["pregunta"]
        self.candidatos = self.animales
        self.preguntas_utilizadas = []
        self.preguntas_realizadas = 0

    def leer_respuesta(self):
        respuesta = input("1 = Sí, 0 = No: ")
        while respuesta != "1" and respuesta != "0":
            print("Respuesta inválida. Escribe solamente 1 o 0.")
            respuesta = input("1 = Sí, 0 = No: ")

        if respuesta == "1":
            return 1
        else:
            return 0

    def buscar_mejor_pregunta(self):
        mejor_posicion = -1
        menor_diferencia = len(self.candidatos) + 1

        for posicion in range(len(self.caracteristicas)):
            if posicion not in self.preguntas_utilizadas:
                cantidad_si = 0
                cantidad_no = 0
                for animal in self.candidatos:
                    if animal["valores"][posicion] == 1:
                        cantidad_si = cantidad_si + 1
                    else:
                        cantidad_no = cantidad_no + 1

                if cantidad_si > 0 and cantidad_no > 0:
                    diferencia = abs(cantidad_si - cantidad_no)
                    # Usar < conserva el orden original en los empates.
                    if diferencia < menor_diferencia:
                        menor_diferencia = diferencia
                        mejor_posicion = posicion

        return mejor_posicion

    def filtrar_animales(self, posicion, respuesta):
        nuevos_candidatos = []
        for animal in self.candidatos:
            if animal["valores"][posicion] == respuesta:
                nuevos_candidatos.append(animal)
        self.candidatos = nuevos_candidatos

    def adivinar(self):
        self.candidatos = self.animales
        self.preguntas_utilizadas = []
        self.preguntas_realizadas = 0
        hay_pregunta = True
        print("Piensa en uno de los animales registrados.")

        while len(self.candidatos) > 1 and hay_pregunta:
            mejor_posicion = self.buscar_mejor_pregunta()
            if mejor_posicion == -1:
                hay_pregunta = False
            else:
                caracteristica = self.caracteristicas[mejor_posicion]
                print(self.preguntas[caracteristica])
                respuesta = self.leer_respuesta()
                self.filtrar_animales(mejor_posicion, respuesta)
                self.preguntas_utilizadas.append(mejor_posicion)
                self.preguntas_realizadas = self.preguntas_realizadas + 1

        if len(self.candidatos) == 1:
            print("Creo que tu animal es:", self.candidatos[0]["nombre"])
            print("¿Adiviné correctamente?")
            respuesta = self.leer_respuesta()
            if respuesta == 1:
                print("Animal adivinado correctamente.")
            else:
                print("No adiviné tu animal.")
                print("¿Quieres agregar tu animal a la base de conocimiento?")
                respuesta = self.leer_respuesta()
                if respuesta == 1:
                    self.agregar_animal()
        else:
            if len(self.candidatos) == 0:
                print("No pude identificar el animal con las respuestas proporcionadas.")
                print("¿Quieres agregar tu animal a la base de conocimiento?")
                respuesta = self.leer_respuesta()
                if respuesta == 1:
                    self.agregar_animal()
            else:
                print("No puedo diferenciar entre:")
                for animal in self.candidatos:
                    print(animal["nombre"])

        print("Preguntas realizadas:", self.preguntas_realizadas)

    def agregar_animal(self):
        nombre = input("Nombre del nuevo animal: ").strip()
        nombre_repetido = True
        while nombre_repetido:
            nombre_repetido = False
            for animal in self.animales:
                if animal["nombre"].strip().lower() == nombre.lower():
                    nombre_repetido = True

            if nombre_repetido:
                print("Ya existe un animal con ese nombre. Escribe otro.")
                nombre = input("Nombre del nuevo animal: ").strip()

        valores = []
        binario = ""
        valor_agregado = 0
        for posicion in range(len(self.caracteristicas)):
            caracteristica = self.caracteristicas[posicion]
            print(self.preguntas[caracteristica])
            respuesta = self.leer_respuesta()
            valores.append(respuesta)
            if respuesta == 1:
                binario = binario + "1"
                valor_agregado = valor_agregado + self.pesos[posicion]
            else:
                binario = binario + "0"

        animal = {
            "nombre": nombre,
            "valores": valores,
            "binario": binario,
            "valor_agregado": valor_agregado
        }
        self.base_conocimiento["animales"].append(animal)
        with open("base_conocimiento.json", "w", encoding="utf-8") as archivo:
            json.dump(self.base_conocimiento, archivo, ensure_ascii=False, indent=4)

        self.actualizar_entrenamiento()
        print("Animal agregado correctamente.")
        print("Base de conocimiento actualizada.")
        print("Entrenamiento actualizado.")
        print("\nAnimal:", nombre)
        print("Binario:", binario)
        print("Valor agregado:", valor_agregado)

    def actualizar_entrenamiento(self):
        resultados = []
        # Se cuentan todos los animales, incluido el recién agregado.
        for posicion in range(len(self.caracteristicas)):
            caracteristica = self.caracteristicas[posicion]
            cantidad_si = 0
            cantidad_no = 0
            for animal in self.animales:
                if animal["valores"][posicion] == 1:
                    cantidad_si = cantidad_si + 1
                else:
                    cantidad_no = cantidad_no + 1

            diferencia = abs(cantidad_si - cantidad_no)
            resultado = {
                "caracteristica": caracteristica,
                "pregunta": self.preguntas[caracteristica],
                "cantidad_si": cantidad_si,
                "cantidad_no": cantidad_no,
                "diferencia": diferencia
            }
            resultados.append(resultado)

        resultados_ordenados = []
        while len(resultados) > 0:
            posicion_menor = 0
            for posicion in range(len(resultados)):
                if resultados[posicion]["diferencia"] < resultados[posicion_menor]["diferencia"]:
                    posicion_menor = posicion
            resultados_ordenados.append(resultados[posicion_menor])
            resultados.pop(posicion_menor)

        self.entrenamiento = resultados_ordenados
        with open("entrenamiento.json", "w", encoding="utf-8") as archivo:
            json.dump(self.entrenamiento, archivo, ensure_ascii=False, indent=4)

adivinador = Adivinador()
seguir_jugando = 1
while seguir_jugando == 1:
    adivinador.adivinar()
    print("¿Quieres seguir jugando?")
    seguir_jugando = adivinador.leer_respuesta()
print("Gracias por jugar.")


import json


class Entrenador:
    def __init__(self):
        with open("base_conocimiento.json", "r", encoding="utf-8") as archivo:
            self.base_conocimiento = json.load(archivo)
        
        self.caracteristicas = self.base_conocimiento["caracteristicas"]
        self.animales = self.base_conocimiento["animales"]
        
        self.preguntas = {
            "Se encuentra en granja": "¿Se encuentra comúnmente en una granja?",
            "Cola larga": "¿Tiene la cola larga?",
            "Leal": "¿Es considerado un animal leal?",
            "Vuela": "¿Puede volar?",
            "Bigotes": "¿Tiene bigotes?",
            "Dientes grandes": "¿Tiene dientes grandes?",
            "Salta": "¿Puede saltar?",
            "Tranquilidad": "¿Generalmente es tranquilo?",
            "Pone huevos": "¿Pone huevos?",
            "Galopa": "¿Puede galopar?",
            "Colmillos largos": "¿Tiene colmillos largos?",
            "Lenta": "¿Se mueve lentamente?"
        }

    def entrenar(self):
        resultados = []
        
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
                # Usar < conserva el primero cuando las diferencias son iguales.
                if resultados[posicion]["diferencia"] < resultados[posicion_menor]["diferencia"]:
                    posicion_menor = posicion
        
            resultados_ordenados.append(resultados[posicion_menor])
            resultados.pop(posicion_menor)
        
        print("Característica | Sí | No | Diferencia")
        
        for resultado in resultados_ordenados:
            print(
                resultado["caracteristica"], "|",
                resultado["cantidad_si"], "|",
                resultado["cantidad_no"], "|",
                resultado["diferencia"]
            )
        
        with open("entrenamiento.json", "w", encoding="utf-8") as archivo:
            json.dump(resultados_ordenados, archivo, ensure_ascii=False, indent=4)
        
        print("\nEntrenamiento guardado en entrenamiento.json")


entrenador = Entrenador()
entrenador.entrenar()

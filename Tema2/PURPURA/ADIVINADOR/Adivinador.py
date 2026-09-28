
import json
import os


class Adivinador:

    def __init__(self, archivo_matriz="matriz_entrenamiento.json", caracteristicas=None):
        self.archivo_matriz = archivo_matriz
        self.matriz = self._cargar_matriz()
        # Si no se pasan explícitamente, se toman del primer animal
        # (todos los animales deben tener las mismas columnas/orden)
        self.caracteristicas = caracteristicas or self._extraer_caracteristicas()
        self.animales_ordenados = self._ordenar_por_peso()

    def _cargar_matriz(self):
        if os.path.exists(self.archivo_matriz):
            with open(self.archivo_matriz, "rt", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        print(f"No se encontró el archivo {self.archivo_matriz}")
        return {}

    def _extraer_caracteristicas(self):
        for valores in self.matriz.values():
            return list(valores.keys())
        return []

    def _obtener_binario(self, animal):
        valores = self.matriz.get(animal, {})
        return "".join(str(valores.get(c, 0)) for c in self.caracteristicas)

    def _obtener_peso(self, animal):
        binario = self._obtener_binario(animal)
        return int(binario, 2) if binario else 0

    def _ordenar_por_peso(self):
        resultado = [
            (animal, self._obtener_binario(animal), self._obtener_peso(animal))
            for animal in self.matriz
        ]
        resultado.sort(key=lambda tupla: tupla[2], reverse=True)
        return resultado

    def _pedir_respuesta(self, caracteristica):
        while True:
            resp = input(f"Tu animal ¿{caracteristica}? (Si/No): ").strip().lower()
            if resp in ("si", "s"):
                return 1
            elif resp in ("no", "n"):
                return 0
            print("Respuesta no válida, escribe 'Si' o 'No'.")

    def mostrar_animales(self):
        print("\nEstos son los animales que conozco:")
        for animal, binario, peso in self.animales_ordenados:
            print(f" - {animal}")
        print("\nPiensa en uno de ellos... ¡yo lo voy a adivinar!\n")

    def adivinar(self):
        self.mostrar_animales()

        candidatos = list(self.animales_ordenados)  # [(animal, binario, peso), ...]

        for indice, caracteristica in enumerate(self.caracteristicas):
            if len(candidatos) <= 1:
                break

            respuesta = self._pedir_respuesta(caracteristica)
            candidatos = [c for c in candidatos if int(c[1][indice]) == respuesta]

            if not candidatos:
                print("\nMmm, no logré identificar tu animal con esas respuestas.")
                return None

        if len(candidatos) == 1:
            animal_adivinado = candidatos[0][0]
            print(f"\n¡Tu animal es el {animal_adivinado}! 🎉")
            return animal_adivinado

        nombres = ", ".join(c[0] for c in candidatos)
        print(f"\nNo pude decidir entre: {nombres}")
        return None

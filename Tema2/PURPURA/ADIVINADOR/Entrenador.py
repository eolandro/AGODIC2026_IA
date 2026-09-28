import json
import os


class Entrenador:
 
    def __init__(self, datos_origen, archivo_salida="matriz_entrenamiento.json"):
        self.datos_origen = datos_origen
        self.archivo_salida = archivo_salida
        self.animales = self._extraer_animales()
        self.caracteristicas = self._extraer_caracteristicas()
        self.matriz = self._cargar_matriz_existente()

    def _extraer_animales(self):
        vistos = []
        for item in self.datos_origen:
            animal = item["Animal"].strip().capitalize()
            if animal not in vistos:
                vistos.append(animal)
        return vistos

    def _extraer_caracteristicas(self):
        vistos = []
        for item in self.datos_origen:
            carac = item["Caracteristica"].strip().capitalize()
            if carac not in vistos:
                vistos.append(carac)
        return vistos

    def _cargar_matriz_existente(self):
        if os.path.exists(self.archivo_salida):
            with open(self.archivo_salida, "rt", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _pedir_respuesta(self, animal, caracteristica):
        while True:
            resp = input(
                f"¿El {animal} tiene la característica '{caracteristica}'? (Si/No): "
            ).strip().lower()
            if resp in ("si", "s"):
                return 1
            elif resp in ("no", "n"):
                return 0
            print("Respuesta no válida, escribe 'Si' o 'No'.")

    def generar_preguntas(self):
		
        print("G E N E R A D O R   D E   M A T R I Z   B I N A R I A")
        for animal in self.animales:
            if animal not in self.matriz:
                self.matriz[animal] = {}
            for carac in self.caracteristicas:
                if carac in self.matriz[animal]:
                    continue
                valor = self._pedir_respuesta(animal, carac)
                self.matriz[animal][carac] = valor

    def obtener_binario(self, animal):
        if animal not in self.matriz:
            return None
        return "".join(str(self.matriz[animal].get(c, 0)) for c in self.caracteristicas)

    def generar_tabla_binaria(self):
        return {animal: self.obtener_binario(animal) for animal in self.animales}

    def obtener_peso(self, animal):
        binario = self.obtener_binario(animal)
        if not binario:
            return 0
        return int(binario, 2)

    def ordenar_por_peso(self, descendente=True):
        resultado = [
            (animal, self.obtener_binario(animal), self.obtener_peso(animal))
            for animal in self.animales
        ]
        resultado.sort(key=lambda tupla: tupla[2], reverse=descendente)
        return resultado

    def mostrar_ranking_por_peso(self):
        ranking = self.ordenar_por_peso()
        print("\nR A N K I N G   P O R   P E S O   B I N A R I O")
        print("Animal".ljust(15) + "Binario".ljust(15) + "Peso")
        print("-" * 40)
        for animal, binario, peso in ranking:
            print(animal.ljust(15) + str(binario).ljust(15) + str(peso))

    def _hay_empates(self):
        pesos = {}
        for animal in self.animales:
            peso = self.obtener_peso(animal)
            pesos.setdefault(peso, []).append(animal)
        return {peso: anims for peso, anims in pesos.items() if len(anims) > 1}

    def _agregar_caracteristica(self, nueva_caracteristica):
        nueva_caracteristica = nueva_caracteristica.strip().capitalize()
        if nueva_caracteristica not in self.caracteristicas:
            self.caracteristicas.append(nueva_caracteristica)

        for animal in self.animales:
            if animal not in self.matriz:
                self.matriz[animal] = {}
            if nueva_caracteristica in self.matriz[animal]:
                continue
            valor = self._pedir_respuesta(animal, nueva_caracteristica)
            self.matriz[animal][nueva_caracteristica] = valor

    def validar_pesos_unicos(self):
        empates = self._hay_empates()
        while empates:
            for peso, anims in empates.items():
                print(f"\nEmpate detectado (peso {peso}) entre: {', '.join(anims)}")
                nueva = input(
                    "Agrega una característica nueva para diferenciarlos: "
                ).strip()
                if nueva:
                    self._agregar_caracteristica(nueva)
            empates = self._hay_empates()
        print("\nTodos los animales tienen un peso binario único.")

    def guardar_matriz(self):
        with open(self.archivo_salida, "wt", encoding="utf-8") as f:
            json.dump(self.matriz, f, ensure_ascii=False, indent=4)
        print(f"Matriz guardada en {self.archivo_salida}")

    def mostrar_tabla(self):
        encabezado = "Animal".ljust(15) + "".join(c[:8].ljust(10) for c in self.caracteristicas)
        print(encabezado)
        print("-" * len(encabezado))
        for animal in self.animales:
            fila = animal.ljust(15)
            for carac in self.caracteristicas:
                valor = self.matriz.get(animal, {}).get(carac, 0)
                fila += str(valor).ljust(10)
            print(fila)

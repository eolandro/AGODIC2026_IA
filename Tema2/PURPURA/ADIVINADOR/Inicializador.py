import json
import os


class RegistroAnimales:
    def __init__(self, archivo="animales.json"):
        self.archivo = archivo
        self.datos = self.cargar_datos()

    def cargar_datos(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "rt", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def guardar_datos(self):
       
        with open(self.archivo, "wt", encoding="utf-8") as f:
            json.dump(self.datos, f, ensure_ascii=False, indent=4)
        print("Datos guardados correctamente")

    def agregar_animal(self, animal, caracteristica):
        carg_an = {"Animal": animal, "Caracteristica": caracteristica}
        self.datos.append(carg_an)

    def registrar_interactivo(self):
        resp = "Si"
        while resp == "Si":
            print("B I E N V E N I D O     A L    A D I V I N A D O R")
            print("Registro de animales y caracteristicas")
            animal = input("\nDigita el nombre del Animal: ")
            carac = input("\nDigita la caracteristica del Animal: ")
            self.agregar_animal(animal, carac)
            resp = input("\nDesea agregar otro animal Si o No ")

    def obtener_datos(self):
        return self.datos
			

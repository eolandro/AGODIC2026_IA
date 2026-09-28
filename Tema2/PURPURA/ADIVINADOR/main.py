from Inicializador import RegistroAnimales
from Entrenador import Entrenador
from Adivinador import Adivinador

ARCHIVO_ANIMALES = "animales.json"
ARCHIVO_MATRIZ = "matriz_entrenamiento.json"


def registrar_y_entrenar():
    registro = RegistroAnimales(ARCHIVO_ANIMALES)
    registro.registrar_interactivo()
    registro.guardar_datos()

    datos = registro.obtener_datos()

    entrenador = Entrenador(datos, archivo_salida=ARCHIVO_MATRIZ)
    entrenador.generar_preguntas()
    entrenador.validar_pesos_unicos()
    entrenador.guardar_matriz()
    entrenador.mostrar_tabla()

    print("\nTabla binaria por animal:")
    print(entrenador.generar_tabla_binaria())

    entrenador.mostrar_ranking_por_peso()


def jugar_adivinador():
    juego = Adivinador(ARCHIVO_MATRIZ)
    juego.adivinar()


def main():
    while True:
        print("\n1) Registrar animales y entrenar la matriz")
        print("2) Jugar a adivinar")
        print("3) Salir")
        opcion = input("Elige una opcion: ").strip()

        if opcion == "1":
            registrar_y_entrenar()
        elif opcion == "2":
            jugar_adivinador()
        elif opcion == "3":
            break
        else:
            print("Opcion no valida.")


if __name__ == "__main__":
    main()

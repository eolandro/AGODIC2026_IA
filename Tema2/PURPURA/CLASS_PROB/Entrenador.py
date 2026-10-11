
import json

ARCHIVO_MENSAJES = "mensajes_entrenamiento.txt"
ARCHIVO_CONOCIMIENTO = "conocimiento_entrenamiento.json"
def cargar_mensajes():
    try:
        with open(ARCHIVO_MENSAJES,"r",encoding="utf-8") as archivo:
            mensajes = [linea.strip() for linea in archivo if linea.strip()]
        if len(mensajes) != 10:
            print()
            print("ERROR: El archivo debe contener exactamente 10 mensajes.")
            print(f"Se encontraron {len(mensajes)}.")
            return None
        return mensajes
    except FileNotFoundError:
        print()
        print("ERROR:")
        print(f"No se encontró el archivo {ARCHIVO_MENSAJES}.")
        return None

def solicitar_clasificacion():
    while True:
        clasificacion = input("Clasificación [S = Spam / N = No Spam]: ").strip().lower()
        if clasificacion == "s":
            return "Spam"
        elif clasificacion == "n":
            return "No Spam"
        else:
            print("Opción no válida.Escribe S o N. ")

def guardar_conocimiento(conocimiento):
    try:
        with open(ARCHIVO_CONOCIMIENTO,"w",encoding="utf-8") as archivo:
            json.dump(conocimiento,archivo,ensure_ascii=False,indent=4)
        print("       ARCHIVO DE CONOCIMIENTO GENERADO")
        print(f"Archivo: {ARCHIVO_CONOCIMIENTO}")
        print(f"Mensajes guardados: {len(conocimiento)}")
    except Exception as error:
        print()
        print("ERROR al guardar el archivo.")
        print(f"Detalle: {error}")

def entrenar():
    mensajes = cargar_mensajes()
    if mensajes is None:
        return
    conocimiento = []
    print("             CLASS_PROB -  ENTRENADOR")
    for i, mensaje in enumerate(mensajes, start=1):
        print(f"\n Mensaje {i} de 10: {mensaje}")
        clasificacion = solicitar_clasificacion()
        registro = {"id": i,"mensaje": mensaje,"clasificacion": clasificacion}
        conocimiento.append(registro)
        print()

        print()
    guardar_conocimiento(conocimiento)
def main():
    entrenar()
if __name__ == "__main__":
    main()


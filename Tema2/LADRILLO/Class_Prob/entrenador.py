import json

def ejecutar_entrenador():
    print("\n ********************* ENTRENADOR ***********************")
    archivo = open("msg0.json", "r", encoding="utf-8")
    mensajes = json.load(archivo)
    archivo.close()

    mensajes_etiquetados = []
    print(" \n Por favor lea los siguientes mensajes y clasifiquelos si es Spam o no es Spam")
    
    for msg in mensajes:
        id_msg = msg["id"]
        texto = msg["msg0"]

        print("\nMensaje", id_msg, ":", texto)
        
        etiqueta = input("¿Es Spam (1) o No Spam (0)?: ").strip()
        while etiqueta != "0" and etiqueta != "1":
            print("Entrada inválida. Por favor ingresa solo 0 o 1.")
            etiqueta = input("¿Es Spam (1) o No Spam (0)?: ").strip()

        nuevo_item = {
            "id": id_msg,
            "msg0": texto,
            "es_noes": int(etiqueta)
        }
        
        mensajes_etiquetados.append(nuevo_item)

    archivo_guardar = open("msg0_etiquetados.json", "w", encoding="utf-8")
    json.dump(mensajes_etiquetados, archivo_guardar, ensure_ascii=False, indent=4)
    archivo_guardar.close()

    print("\n Listo Se guardó el archivo msg0_etiquetados.json XD")

if __name__ == "__main__":
    ejecutar_entrenador()
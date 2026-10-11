import json
import re

from detoquenizador import trash_basura, obtener_tokens

def ejecutar_clasificador():
    print("\n ********************* CLASIFICADOR (MEDIA) ***********************")

    archivo_msg1 = open("msg_new.json", "r", encoding="utf-8")
    nuevos_mensajes = json.load(archivo_msg1)
    archivo_msg1.close()

    archivo_probs = open("tabla_probabilidades.json", "r", encoding="utf-8")
    tabla_probabilidades = json.load(archivo_probs)
    archivo_probs.close()

    msg1_sistema = []

    print("Analizando mensajes con Consenso por Media...")

    for msg in nuevos_mensajes:
        id_msg = msg["id"]
        
        if "msg1" in msg:
            texto = msg["msg1"]
        else:
            texto = msg["new_mensaje"]

        tokens = obtener_tokens(texto)

        probabilidades_encontradas = []
        for token in tokens:
            if token in tabla_probabilidades:
                probabilidades_encontradas.append(tabla_probabilidades[token])
            else:
                probabilidades_encontradas.append(0.0)

        conteo_tokens = len(tokens)
        if conteo_tokens > 0:
            suma_probs = sum(probabilidades_encontradas)
            media = suma_probs / conteo_tokens
        else:
            media = 0.0

        if media > 0.05:
            es_noes = 1
        else:
            es_noes = 0

        nuevo_item = {
            "id": id_msg,
            "msg1": texto,
            "es_noes": es_noes
        }
        msg1_sistema.append(nuevo_item)

    archivo_guardar = open("msg1_sistema.json", "w", encoding="utf-8")
    json.dump(msg1_sistema, archivo_guardar, ensure_ascii=False, indent=4)
    archivo_guardar.close()

    print("\n ¡Listo! Se generó 'msg1_sistema.json' con éxito XD")

if __name__ == "__main__":
    ejecutar_clasificador()
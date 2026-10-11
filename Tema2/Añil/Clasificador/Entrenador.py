import json
import sys

num_mensajes = 10
archivo_entrada = "mensajes_entrenamiento.txt"
archivo_salida = "entrenamiento_etiquetado.json"
spam = "spam"
NOspam = "no_spam"


def leer_mensajes(ruta):
    with open(ruta, encoding="utf-8") as f:
        return [linea.strip() for linea in f if linea.strip()]

def etiquetar(mensaje):
    while True:
        respuesta = input(f'\n"{mensaje}"\n¿Es spam? (S/N): ').strip().upper()
        if respuesta == "S":
            return spam
        if respuesta == "N":
            return NOspam
        print("Opción inválida. Escribe S o N.")

def guardar(registros, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)

#-------------------------------------- MAIN --------------------------------------#
ruta_entrada = sys.argv[1] if len(sys.argv) > 1 else archivo_entrada
ruta_salida = sys.argv[2] if len(sys.argv) > 2 else archivo_salida

print("* * * ENTRENADOR * * *")
try:
    mensajes = leer_mensajes(ruta_entrada)
except FileNotFoundError:
    print(f"No se encontró el archivo '{ruta_entrada}'.")
    sys.exit()

if len(mensajes) != num_mensajes:
    print(f"Aviso: se esperaban {num_mensajes} mensajes y el archivo tiene {len(mensajes)}.")
registros = [{"mensaje": m, "etiqueta": etiquetar(m)} for m in mensajes]
guardar(registros, ruta_salida)
total_spam = sum(1 for r in registros if r["etiqueta"] == spam)
print(f"\nArchivo '{ruta_salida}' generado.")
print(f"Spam: {total_spam} | No spam: {len(registros) - total_spam} | Total: {len(registros)}")
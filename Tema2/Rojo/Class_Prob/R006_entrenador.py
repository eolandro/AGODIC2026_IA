import json
import sys
from pathlib import Path

ENTRADA = Path("mensajes_entrenamiento.txt")
SALIDA = Path("mensajes_etiquetados.json")
CANTIDAD = 10


def preguntar_si_no(texto):
    while True:
        respuesta = input(f"¿{texto}? [s/n]: ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta inválida, escribe s o n.")


def cargar_mensajes():
    if not ENTRADA.exists():
        sys.exit(f"No existe {ENTRADA}. Crea el archivo con un mensaje por línea.")
    lineas = ENTRADA.read_text(encoding="utf-8").splitlines()
    mensajes = [linea.strip() for linea in lineas if linea.strip()]
    if len(mensajes) != CANTIDAD:
        sys.exit(f"{ENTRADA} debe tener exactamente {CANTIDAD} mensajes (tiene {len(mensajes)}).")
    return mensajes


def main():
    mensajes = cargar_mensajes()
    etiquetados = []

    print("El supervisor debe clasificar cada mensaje.\n")
    for i, mensaje in enumerate(mensajes, start=1):
        print(f"Mensaje {i} de {CANTIDAD}: {mensaje}")
        etiquetados.append({"mensaje": mensaje, "spam": preguntar_si_no("Es spam")})
        print()

    SALIDA.write_text(json.dumps(etiquetados, ensure_ascii=False, indent=2), encoding="utf-8")

    spam = sum(1 for m in etiquetados if m["spam"])
    
    print(f"Spam: {spam} | No spam: {CANTIDAD - spam}")
    print(f"\n Archivo generado: {SALIDA}")
    print(" Siguiente paso: R007_detokenizador.py")


if __name__ == "__main__":
    main()

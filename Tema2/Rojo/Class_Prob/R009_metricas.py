import json
import sys
from pathlib import Path

ENTRADA = Path("mensajes_clasificados.json")


def preguntar_si_no(texto):
    while True:
        respuesta = input(f"¿{texto}? [s/n]: ").strip().lower()
        if respuesta in ("s", "n"):
            return respuesta == "s"
        print("Respuesta inválida, escribe s o n.")


def dividir(a, b):
    return a / b if b else None


def formatear(valor):
    return "indefinido" if valor is None else f"{valor:.2%}"


def cargar_clasificados():
    if not ENTRADA.exists():
        sys.exit(f"No existe {ENTRADA}. Ejecuta primero R008_clasificador.py")
    try:
        mensajes = json.loads(ENTRADA.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.exit(f"{ENTRADA} no es un JSON válido: {e}")
    valido = isinstance(mensajes, list) and mensajes and all(
        isinstance(m, dict) and isinstance(m.get("mensaje"), str) and isinstance(m.get("spam"), bool)
        for m in mensajes
    )
    if not valido:
        sys.exit(f"{ENTRADA} no tiene el formato esperado. Vuelve a ejecutar R008_clasificador.py")
    return mensajes


def main():
    mensajes = cargar_clasificados()
    total = len(mensajes)

    print("Clasifica cada mensaje como lo haría el usuario.\n")
    real = []
    for i, m in enumerate(mensajes, start=1):
        print(f"Mensaje {i} de {total}: {m['mensaje']}")
        real.append(preguntar_si_no("Es spam"))
        print()

    vp = fp = fn = vn = 0
    for m, es_spam_real in zip(mensajes, real):
        if m["spam"] and es_spam_real:
            vp += 1
        elif m["spam"] and not es_spam_real:
            fp += 1
        elif not m["spam"] and es_spam_real:
            fn += 1
        else:
            vn += 1

    accuracy = dividir(vp + vn, total)
    precision = dividir(vp, vp + fp)
    recall = dividir(vp, vp + fn)
    prevalence = dividir(vp + fn, total)


    print(f"{'':32}{'Real: spam':>12}{'Real: no spam':>15}")
    print(f"{' spam':24}{vp:>12}{fp:>15}")
    print(f"{' no spam':22}{fn:>12}{vn:>15}")

    print(f"\nVP (Verdadero Positivo)={vp},  FP (Falso Positivo)={fp},  FN (Falso Negativo)={fn},  VN (Verdadero Negativo)={vn}, Total ={total}")
    
    print(f"\nAccuracy   = (VP+VN)/total = {formatear(accuracy)}")
    print(f"Precision  = VP/(VP+FP)    = {formatear(precision)}")
    print(f"Recall     = VP/(VP+FN)    = {formatear(recall)}")
    print(f"Prevalence = (VP+FN)/total = {formatear(prevalence)}")


if __name__ == "__main__":
    main()
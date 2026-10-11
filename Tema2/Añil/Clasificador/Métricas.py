import json
import sys

archivo_entrada = "mensajes_clasificados.json"
spam = "spam"
NOspam = "no_spam"

def leer_registros(ruta):
    with open(ruta, encoding="utf-8") as f:
        return json.load(f)

def etiquetar(mensaje):
    while True:
        respuesta = input(f'\n"{mensaje}"\n¿Es spam? (S/N): ').strip().upper()
        if respuesta == "S":
            return spam
        if respuesta == "N":
            return NOspam
        print("Opción inválida. Escribe S o N.")

def dividir(numerador, denominador):
    """División segura: devuelve None si el denominador es 0 (métrica no calculable)."""
    return numerador / denominador if denominador > 0 else None

def formato(valor):
    return "N/A" if valor is None else f"{valor:.4f}  ({valor * 100:.2f}%)"

#-------------------------------------- MAIN --------------------------------------#
ruta_entrada = sys.argv[1] if len(sys.argv) > 1 else archivo_entrada

print("* * * MÉTRICAS * * *")
try:
    registros = leer_registros(ruta_entrada)
except FileNotFoundError:
    print(f"\nNo se encontró el archivo '{ruta_entrada}'. Ejecuta primero el Clasificador.")
    sys.exit()

# El usuario etiqueta cada mensaje y se compara contra la etiqueta del Clasificador
vp = fp = fn = vn = 0
for r in registros:
    usuario = etiquetar(r["mensaje"])
    clasificador = r["etiqueta"]
    if clasificador == spam and usuario == spam:
        vp += 1        # verdadero positivo
    elif clasificador == spam and usuario == NOspam:
        fp += 1        # falso positivo
    elif clasificador == NOspam and usuario == spam:
        fn += 1        # falso negativo
    else:
        vn += 1        # verdadero negativo

total = vp + fp + fn + vn
precision = dividir(vp, vp + fp)
recall = dividir(vp, vp + fn)
prevalencia = dividir(vp + fn, total)
accuracy = dividir(vp + vn, total)

print("\n\n* * * MATRIZ DE CONFUSIÓN * * *")
print(f"{'':<22}{'Usuario':^18}")
print(f"{'':<22}{'spam':>8}{'no_spam':>10}")
print(f"{'Clasificador spam':<22}{vp:>8}{fp:>10}   (VP, FP)")
print(f"{'Clasificador no_spam':<22}{fn:>8}{vn:>10}   (FN, VN)")

print("\n* * * MÉTRICAS * * *")
print(f"Precision   = VP / (VP + FP)    = {vp}/{vp + fp}  -> {formato(precision)}")
print(f"Recall      = VP / (VP + FN)    = {vp}/{vp + fn}  -> {formato(recall)}")
print(f"Prevalence  = (VP + FN) / total = {vp + fn}/{total}  -> {formato(prevalencia)}")
print(f"Accuracy    = (VP + VN) / total = {vp + vn}/{total}  -> {formato(accuracy)}")
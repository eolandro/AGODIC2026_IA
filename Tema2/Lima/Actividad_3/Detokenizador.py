import json
import sys

from texto import tokenizar

ENTRADA = "entrenamiento_etiquetado.json"
SALIDA = "tabla_probabilidades.json"


def main():
    print("* * * DETOKENIZADOR * * *\n")
    try:
        with open(ENTRADA, encoding="utf-8") as archivo:
            registros = json.load(archivo)
    except FileNotFoundError:
        sys.exit(f"No se encontró '{ENTRADA}'. Ejecuta primero Entrenador.py")

    conteo = {}
    for registro in registros:
        for token in tokenizar(registro["mensaje"]):
            conteo.setdefault(token, {"spam": 0, "no_spam": 0})
            conteo[token][registro["etiqueta"]] += 1

    total = len(registros)
    total_spam = sum(r["etiqueta"] == "spam" for r in registros)

    tokens = {}
    for token, c in conteo.items():
        apariciones = c["spam"] + c["no_spam"]
        tokens[token] = {
            "spam": c["spam"],
            "no_spam": c["no_spam"],
            "p_spam": round((c["spam"] + 1) / (apariciones + 2), 4),
        }

    tokens = dict(sorted(tokens.items(),
                         key=lambda t: (-t[1]["p_spam"],
                                        -(t[1]["spam"] + t[1]["no_spam"]), t[0])))

    tabla = {
        "totales": {
            "mensajes": total,
            "spam": total_spam,
            "no_spam": total - total_spam,
            "p_spam": round(total_spam / total, 4),
        },
        "tokens": tokens,
    }
    with open(SALIDA, "w", encoding="utf-8") as archivo:
        json.dump(tabla, archivo, ensure_ascii=False, indent=2)

    print(f"Mensajes: {total} | Spam: {total_spam} | No spam: {total - total_spam}")
    print(f"Tokens distintos (sin palabras vacías): {len(tokens)}\n")
    print(f"{'Token':16}{'Spam':>5}{'No spam':>9}{'P(spam|token)':>15}")
    print("-" * 45)
    for token, d in tokens.items():
        print(f"{token:16}{d['spam']:>5}{d['no_spam']:>9}{d['p_spam']:>15.4f}")
    print(f"\nArchivo '{SALIDA}' generado.")


if __name__ == "__main__":
    main()

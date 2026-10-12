import json
import sys
from statistics import mean, median, multimode

from texto import tokenizar

ENTRADA = "mensajes_nuevos.txt"
TABLA = "tabla_probabilidades.json"
SALIDA = "mensajes_clasificados.json"
UMBRAL = 0.5


def decidir(valor):
    return "spam" if valor > UMBRAL else "no_spam"


def democracia(probs):
    votos_spam = sum(p > UMBRAL for p in probs)
    votos_no = sum(p < UMBRAL for p in probs)
    return "spam" if votos_spam > votos_no else "no_spam"


def por_media(probs):
    return decidir(mean(probs))


def por_mediana(probs):
    return decidir(median(probs))


def por_moda(probs):
    return decidir(mean(multimode(probs)))


METODOS = {"democracia": democracia, "media": por_media,
           "mediana": por_mediana, "moda": por_moda}


def main():
    metodo = sys.argv[1] if len(sys.argv) > 1 else "democracia"
    if metodo not in METODOS:
        sys.exit(f"Método desconocido. Usa uno de: {', '.join(METODOS)}")

    print("* * * CLASIFICADOR * * *")
    try:
        with open(ENTRADA, encoding="utf-8") as archivo:
            mensajes = [l.strip() for l in archivo if l.strip()]
        with open(TABLA, encoding="utf-8") as archivo:
            tabla = json.load(archivo)["tokens"]
    except FileNotFoundError as error:
        sys.exit(f"No se encontró '{error.filename}'. Ejecuta primero Detokenizador.py")

    print(f"Método de consenso elegido: {metodo}\n")
    print(f"{'#':>2} {'Dem':>8} {'Media':>8} {'Mediana':>8} {'Moda':>8}  Tokens  Mensaje")
    print("-" * 90)

    registros = []
    for numero, mensaje in enumerate(mensajes, 1):
        conocidos = {t: tabla[t]["p_spam"] for t in sorted(tokenizar(mensaje)) if t in tabla}
        probs = list(conocidos.values())
        if probs:
            resultados = {nombre: f(probs) for nombre, f in METODOS.items()}
        else:
            resultados = {nombre: "no_spam" for nombre in METODOS}

        registros.append({
            "mensaje": mensaje,
            "tokens_conocidos": conocidos,
            "metodos": resultados,
            "etiqueta": resultados[metodo],
        })
        corto = mensaje if len(mensaje) <= 42 else mensaje[:39] + "..."
        celdas = " ".join(f"{('SPAM' if r == 'spam' else 'no'):>8}" for r in resultados.values())
        print(f"{numero:>2} {celdas}  {len(probs):>6}  {corto}")

    with open(SALIDA, "w", encoding="utf-8") as archivo:
        json.dump({"metodo": metodo, "mensajes": registros}, archivo,
                  ensure_ascii=False, indent=2)

    spam = sum(r["etiqueta"] == "spam" for r in registros)
    print(f"\nCon {metodo}: Spam {spam} | No spam {len(registros) - spam}")
    print(f"Archivo '{SALIDA}' generado.")


if __name__ == "__main__":
    main()


import json
import re
ARCHIVO_ENTRENAMIENTO = "conocimiento_entrenamiento.json"
ARCHIVO_PROBABILIDADES = "tabla_probabilidades.json"
PALABRAS_IGNORADAS = {
    # Artículos
    "el", "la", "los", "las",
    "un", "una", "unos", "unas",

    # Preposiciones
    "a", "ante", "bajo", "con", "contra",
    "de", "desde", "durante", "en", "entre",
    "hacia", "hasta", "mediante", "para",
    "por", "según", "sin", "sobre", "tras",

    # Conectores y palabras frecuentes
    "y", "e", "o", "u", "ni",
    "que", "pero", "aunque",
    "porque", "como", "cuando",
    "donde", "si", "mientras",

    # Pronombres / palabras auxiliares
    "yo", "tu", "tú", "el", "ella",
    "nosotros", "ellos", "ellas",
    "me", "te", "se", "nos", "les",
    "lo", "le"
}
def cargar_conocimiento():
    try:
        with open(
            ARCHIVO_ENTRENAMIENTO,
            "r",
            encoding="utf-8"
        ) as archivo:
            conocimiento = json.load(archivo)
        print("Archivo de entrenamiento cargado correctamente.")
        return conocimiento
    except FileNotFoundError:
        print()
        print("ERROR:")
        print(f"No se encontró el archivo '{ARCHIVO_ENTRENAMIENTO}'.")
        print()
        print("Primero debes ejecutar Entrenador.py.")
        return None
    except json.JSONDecodeError:
        print()
        print("ERROR:")
        print("El archivo JSON tiene un formato incorrecto.")
        return None

def tokenizar(mensaje):
    mensaje = mensaje.lower()
    mensaje = re.sub(r"[^\w\sáéíóúüñ]", " ", mensaje)
    tokens = mensaje.split()
    tokens_filtrados = []
    for token in tokens:
        if token not in PALABRAS_IGNORADAS:
            tokens_filtrados.append(token)
    return tokens_filtrados

def procesar_mensajes(conocimiento):
    datos = []
    for registro in conocimiento:
        mensaje = registro["mensaje"]
        clasificacion = registro["clasificacion"]
        tokens = tokenizar(mensaje)
        datos.append({
            "id": registro["id"],
            "clasificacion": clasificacion,
            "tokens": tokens
        })
    return datos

def contar_tokens(datos):
    spam_tokens = {}
    no_spam_tokens = {}
    total_spam = 0
    total_no_spam = 0
    for registro in datos:
        tokens = registro["tokens"]
        clasificacion = registro["clasificacion"]
        tokens_unicos = set(tokens)
        for token in tokens_unicos:
            if clasificacion == "Spam":
                if token not in spam_tokens:
                    spam_tokens[token] = 0
                spam_tokens[token] += 1
                total_spam += 1
            else:
                if token not in no_spam_tokens:
                    no_spam_tokens[token] = 0
                no_spam_tokens[token] += 1
                total_no_spam += 1
    return (
        spam_tokens,
        no_spam_tokens,
        total_spam,
        total_no_spam
    )

def calcular_probabilidades(
    spam_tokens,
    no_spam_tokens,
    total_spam,
    total_no_spam
):

    todos_tokens = set(spam_tokens.keys())
    todos_tokens.update(no_spam_tokens.keys())
    probabilidades = {}
    for token in sorted(todos_tokens):
        frecuencia_spam = spam_tokens.get(token, 0)
        frecuencia_no_spam = no_spam_tokens.get(token, 0)
        prob_spam = (
            (frecuencia_spam + 1)
            / (total_spam + 2)
        )
        prob_no_spam = (
            (frecuencia_no_spam + 1)
            / (total_no_spam + 2)
        )
        probabilidades[token] = {
            "frecuencia_spam": frecuencia_spam,
            "frecuencia_no_spam": frecuencia_no_spam,
            "probabilidad_token_dado_spam": round(
                prob_spam, 6
            ),
            "probabilidad_token_dado_no_spam": round(
                prob_no_spam, 6
            )
        }
    return probabilidades

def calcular_probabilidad_clases(datos):
    total_mensajes = len(datos)
    mensajes_spam = 0
    mensajes_no_spam = 0
    for registro in datos:
        if registro["clasificacion"] == "Spam":
            mensajes_spam += 1
        else:
            mensajes_no_spam += 1
    if total_mensajes > 0:
        prob_spam = mensajes_spam / total_mensajes
        prob_no_spam = mensajes_no_spam / total_mensajes
    else:
        prob_spam = 0
        prob_no_spam = 0
    return {
        "total_mensajes": total_mensajes,
        "mensajes_spam": mensajes_spam,
        "mensajes_no_spam": mensajes_no_spam,
        "probabilidad_spam": round(prob_spam, 6),
        "probabilidad_no_spam": round(prob_no_spam, 6)
    }
def guardar_probabilidades(
    probabilidades,
    probabilidades_clases,
    datos
):
    resultado = {
        "descripcion":
            "Tabla de probabilidades condicionales "
            "generada por DeTokenizador",
        "probabilidades_clases":
            probabilidades_clases,
        "mensajes_procesados":
            datos,
        "tabla_tokens":
            probabilidades
    }
    try:
        with open(
            ARCHIVO_PROBABILIDADES,
            "w",
            encoding="utf-8"
        ) as archivo:
            json.dump(
                resultado,
                archivo,
                ensure_ascii=False,
                indent=4
            )
        print()
        print("=" * 60)
        print("       TABLA DE PROBABILIDADES GENERADA")
        print("=" * 60)
        print()
        print(
            f"Archivo generado: "
            f"{ARCHIVO_PROBABILIDADES}"
        )
        print(
            f"Tokens encontrados: "
            f"{len(probabilidades)}"
        )
    except Exception as error:

        print()
        print("ERROR al guardar el archivo.")
        print(f"Detalle: {error}")


def mostrar_resultados(
    datos,
    probabilidades,
    probabilidades_clases
):
    print()
    print("=" * 60)
    print("              TOKENS GENERADOS")
    print("=" * 60)
    for registro in datos:
        print()
        print(
            f"Mensaje {registro['id']} "
            f"({registro['clasificacion']}):"
        )
        print(
            "Tokens:",
            ", ".join(registro["tokens"])
        )
    print()
    print("=" * 60)
    print("          PROBABILIDADES DE LAS CLASES")
    print("=" * 60)
    print(
        f"Spam: "
        f"{probabilidades_clases['probabilidad_spam']}"
    )
    print(
        f"No Spam: "
        f"{probabilidades_clases['probabilidad_no_spam']}"
    )
    print()
    print("=" * 60)
    print("          TABLA DE PROBABILIDADES")
    print("=" * 60)
    print(
        f"{'TOKEN':<20}"
        f"{'P(T|Spam)':<15}"
        f"{'P(T|NoSpam)':<15}"
    )
    print("-" * 50)
    for token, datos_token in probabilidades.items():
        print(
            f"{token:<20}"
            f"{datos_token['probabilidad_token_dado_spam']:<15}"
            f"{datos_token['probabilidad_token_dado_no_spam']:<15}"
        )

def main():
    print()
    print("=" * 60)
    print("             CLASS_PROB")
    print("             DE TOKENIZADOR")
    print("=" * 60)
    print()
    conocimiento = cargar_conocimiento()
    if conocimiento is None:
        return
    datos = procesar_mensajes(conocimiento)
    (
        spam_tokens,
        no_spam_tokens,
        total_spam,
        total_no_spam
    ) = contar_tokens(datos)
    probabilidades = calcular_probabilidades(
        spam_tokens,
        no_spam_tokens,
        total_spam,
        total_no_spam
    )
    probabilidades_clases = calcular_probabilidad_clases(
        datos
    )
    mostrar_resultados(
        datos,
        probabilidades,
        probabilidades_clases
    )
    guardar_probabilidades(
        probabilidades,
        probabilidades_clases,
        datos
    )
    print()
    print("Proceso de DeTokenización terminado.")
    print()
if __name__ == "__main__":
    main()

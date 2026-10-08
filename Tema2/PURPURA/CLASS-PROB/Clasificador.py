
import json
import re


ARCHIVO_PROBABILIDADES = "tabla_probabilidades.json"
ARCHIVO_MENSAJES = "mensajes_nuevos.txt"
ARCHIVO_RESULTADOS = "resultados_clasificador.json"


PALABRAS_IGNORADAS = {
    # Artículos
    "el", "la", "los", "las",
    "un", "una", "unos", "unas",

    # Preposiciones
    "a", "ante", "bajo", "con", "contra",
    "de", "desde", "durante", "en", "entre",
    "hacia", "hasta", "mediante", "para",
    "por", "según", "sin", "sobre", "tras",

    # Conectores
    "y", "e", "o", "u", "ni",
    "que", "pero", "aunque",
    "porque", "como", "cuando",
    "donde", "si", "mientras",

    # Pronombres
    "yo", "tu", "tú", "él", "ella",
    "nosotros", "ellos", "ellas",
    "me", "te", "se", "nos", "les",
    "lo", "le"
}


def cargar_probabilidades():

    try:

        with open(
            ARCHIVO_PROBABILIDADES,
            "r",
            encoding="utf-8"
        ) as archivo:

            datos = json.load(archivo)

        return datos

    except FileNotFoundError:

        print()
        print("ERROR:")
        print(
            f"No se encontró '{ARCHIVO_PROBABILIDADES}'."
        )
        print(
            "Ejecuta primero DeTokenizador.py."
        )

        return None

    except json.JSONDecodeError:

        print()
        print("ERROR:")
        print("El JSON de probabilidades es inválido.")

        return None


def cargar_mensajes():

    try:

        with open(
            ARCHIVO_MENSAJES,
            "r",
            encoding="utf-8"
        ) as archivo:

            mensajes = [
                linea.strip()
                for linea in archivo
                if linea.strip()
            ]

        if len(mensajes) != 10:

            print()
            print("ERROR:")
            print(
                "El archivo de mensajes nuevos "
                "debe contener exactamente 10 mensajes."
            )
            print(
                f"Se encontraron {len(mensajes)}."
            )

            return None

        return mensajes

    except FileNotFoundError:

        print()
        print("ERROR:")
        print(
            f"No se encontró '{ARCHIVO_MENSAJES}'."
        )

        return None


def tokenizar(mensaje):

    mensaje = mensaje.lower()

    mensaje = re.sub(
        r"[^\w\sáéíóúüñ]",
        " ",
        mensaje
    )

    tokens = mensaje.split()

    tokens_filtrados = []

    for token in tokens:

        if token not in PALABRAS_IGNORADAS:
            tokens_filtrados.append(token)

    return tokens_filtrados


def clasificar_por_consenso(
    tokens,
    tabla_tokens
):

    votos_spam = 0
    votos_no_spam = 0

    detalles = []

    for token in tokens:

        if token in tabla_tokens:

            datos_token = tabla_tokens[token]

            prob_spam = datos_token[
                "probabilidad_token_dado_spam"
            ]

            prob_no_spam = datos_token[
                "probabilidad_token_dado_no_spam"
            ]

            if prob_spam > prob_no_spam:

                votos_spam += 1
                voto = "Spam"

            elif prob_no_spam > prob_spam:

                votos_no_spam += 1
                voto = "No Spam"

            else:

                voto = "Empate"

            detalles.append({
                "token": token,
                "probabilidad_spam": prob_spam,
                "probabilidad_no_spam": prob_no_spam,
                "voto": voto
            })

        else:

            detalles.append({
                "token": token,
                "probabilidad_spam": None,
                "probabilidad_no_spam": None,
                "voto": "Sin información"
            })
    if votos_spam > votos_no_spam:

        clasificacion = "Spam"

    elif votos_no_spam > votos_spam:

        clasificacion = "No Spam"

    else:

        clasificacion = "Empate"

    return (
        clasificacion,
        votos_spam,
        votos_no_spam,
        detalles
    )


def clasificar_mensaje(
    numero,
    mensaje,
    tabla_tokens
):

    tokens = tokenizar(mensaje)

    (
        clasificacion,
        votos_spam,
        votos_no_spam,
        detalles
    ) = clasificar_por_consenso(
        tokens,
        tabla_tokens
    )

    return {
        "id": numero,
        "mensaje": mensaje,
        "tokens": tokens,
        "votos_spam": votos_spam,
        "votos_no_spam": votos_no_spam,
        "clasificacion": clasificacion,
        "detalle_tokens": detalles
    }


def clasificar_mensajes(
    mensajes,
    tabla_tokens
):

    resultados = []

    print()
    print("=" * 60)
    print("             CLASS_PROB")
    print("             CLASIFICADOR")
    print("=" * 60)
    print()
    print(
        f"Se cargaron {len(mensajes)} mensajes "
        f"desde '{ARCHIVO_MENSAJES}'."
    )
    print()

    for i, mensaje in enumerate(
        mensajes,
        start=1
    ):

        resultado = clasificar_mensaje(
            i,
            mensaje,
            tabla_tokens
        )

        resultados.append(resultado)

        print("-" * 60)
        print(f"MENSAJE {i} DE 10")
        print("-" * 60)

        print()
        print(f"Mensaje: {mensaje}")

        print()
        print(
            "Tokens:",
            ", ".join(resultado["tokens"])
        )

        print()
        print(
            f"Votos Spam: "
            f"{resultado['votos_spam']}"
        )

        print(
            f"Votos No Spam: "
            f"{resultado['votos_no_spam']}"
        )

        print()
        print(
            f"CLASIFICACIÓN: "
            f"{resultado['clasificacion']}"
        )

        print()

    return resultados


def guardar_resultados(resultados):

    contenido = {

        "descripcion":
            "Resultados generados por el Clasificador",

        "metodo_consenso":
            "Votación por mayoría de tokens",

        "archivo_entrada":
            ARCHIVO_MENSAJES,

        "total_mensajes":
            len(resultados),

        "resultados":
            resultados
    }

    try:

        with open(
            ARCHIVO_RESULTADOS,
            "w",
            encoding="utf-8"
        ) as archivo:

            json.dump(
                contenido,
                archivo,
                ensure_ascii=False,
                indent=4
            )

        print("=" * 60)
        print("       CLASIFICACIÓN TERMINADA")
        print("=" * 60)
        print()
        print(
            f"Archivo generado: "
            f"{ARCHIVO_RESULTADOS}"
        )

    except Exception as error:

        print(
            f"ERROR al guardar resultados: {error}"
        )


def main():

    datos = cargar_probabilidades()

    if datos is None:
        return

    mensajes = cargar_mensajes()

    if mensajes is None:
        return

    tabla_tokens = datos.get(
        "tabla_tokens",
        {}
    )

    if not tabla_tokens:

        print(
            "ERROR: la tabla de probabilidades está vacía."
        )

        return

    resultados = clasificar_mensajes(
        mensajes,
        tabla_tokens
    )

    guardar_resultados(
        resultados
    )


if __name__ == "__main__":
    main()

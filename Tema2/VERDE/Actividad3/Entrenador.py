from pathlib import Path
import yaml

CARPETA = Path(__file__).resolve().parent
ARCHIVO_ENTRADA = CARPETA / "msg.yaml"
ARCHIVO_SALIDA = CARPETA / "msg_etiquetados.yaml"

ETIQUETA_SPAM = "spam"
ETIQUETA_NO_SPAM = "no_spam"


def respuesta_a_etiqueta(respuesta):
    match respuesta.strip().upper():
        case "S":
            return ETIQUETA_SPAM
        case "N":
            return ETIQUETA_NO_SPAM
        case _:
            return None 

def etiquetar(mensajes, etiquetas):
    return [{"mensaje": m, "etiqueta": e} for m, e in zip(mensajes, etiquetas)]

def contar_etiqueta(etiquetados, etiqueta):
    return sum(1 for r in etiquetados if r["etiqueta"] == etiqueta)

def hay_ambas_clases(etiquetados):
    return (contar_etiqueta(etiquetados, ETIQUETA_SPAM) > 0
            and contar_etiqueta(etiquetados, ETIQUETA_NO_SPAM) > 0)


def cargar_mensajes(ruta):
    # Lee msg.yaml: una lista simple de textos
    with open(ruta, "r", encoding="utf-8") as archivo:
        return yaml.safe_load(archivo)


def preguntar_etiqueta(mensaje, numero, total):
    respuesta = input(f"\nMensaje {numero}/{total}:\n  \"{mensaje}\"\n¿Es spam? (S/N): ")
    etiqueta = respuesta_a_etiqueta(respuesta)
    if etiqueta is None:
        print("Respuesta inválida: escribe únicamente S o N.")
        return preguntar_etiqueta(mensaje, numero, total)
    return etiqueta

def etiquetar_mensajes(mensajes):
    total = len(mensajes)
    etiquetas = [preguntar_etiqueta(m, i, total) for i, m in enumerate(mensajes, start=1)]
    return etiquetar(mensajes, etiquetas)

def etiquetar_hasta_balancear(mensajes):
    etiquetados = etiquetar_mensajes(mensajes)
    if hay_ambas_clases(etiquetados):
        return etiquetados
    print("\nSe necesita al menos un mensaje spam y uno no spam. Vuelve a etiquetar.")
    return etiquetar_hasta_balancear(mensajes)

def guardar_etiquetados(ruta, etiquetados):
    with open(ruta, "w", encoding="utf-8") as archivo:
        yaml.safe_dump(etiquetados, archivo, allow_unicode=True, sort_keys=False)

def main():
    mensajes = cargar_mensajes(ARCHIVO_ENTRADA)
    print(f"Se cargaron {len(mensajes)} mensajes de {ARCHIVO_ENTRADA.name}.")
    etiquetados = etiquetar_hasta_balancear(mensajes)
    guardar_etiquetados(ARCHIVO_SALIDA, etiquetados)
    print(f"\nListo: {len(etiquetados)} mensajes etiquetados en {ARCHIVO_SALIDA.name}.")


if __name__ == "__main__":
    main()

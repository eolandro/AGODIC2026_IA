import sys
from datetime import datetime
import json
import os
import unicodedata



def quitar_acentos(texto):
    texto = texto.lower().replace("ñ", "\0")
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.replace("\0", "ñ")


def guardar(datos, ruta):
    if ruta.endswith((".yaml", ".yml")):
        import yaml  
        with open(ruta, "w", encoding="utf-8") as f:
            yaml.safe_dump(datos, f, allow_unicode=True, sort_keys=False)
    else:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"\n>> Archivo de conocimiento generado: {os.path.abspath(ruta)}")


def cargar(ruta):
    if not os.path.exists(ruta):
        raise SystemExit(f"No existe el archivo '{ruta}'. Ejecuta primero el programa anterior.")
    with open(ruta, encoding="utf-8") as f:
        if ruta.endswith((".yaml", ".yml")):
            import yaml
            return yaml.safe_load(f)
        return json.load(f)


def cargar_mensajes_texto(ruta):
    """Lee mensajes de un .txt (uno por línea) o de un .json/.yaml (lista de textos)."""
    if ruta.endswith((".json", ".yaml", ".yml")):
        datos = cargar(ruta)
        if isinstance(datos, dict):
            datos = datos.get("mensajes", [])
        return [m["texto"] if isinstance(m, dict) else str(m) for m in datos]
    with open(ruta, encoding="utf-8") as f:
        return [l.strip() for l in f if l.strip()]


def preguntar_si_no(pregunta):
    while True:
        r = quitar_acentos(input(pregunta).strip())
        if r in ("s", "si"):
            return True
        if r in ("n", "no"):
            return False
        print("   Responde 's' (sí) o 'n' (no).")


N_MENSAJES = 10
SALIDA = "mensajes_etiquetados.json"


def main():
    print("=" * 60)
    print(" ENTRENADOR - El Supervisor etiqueta 10 mensajes")
    print("=" * 60)

    if len(sys.argv) > 1:
        mensajes = cargar_mensajes_texto(sys.argv[1])[:N_MENSAJES]
        if len(mensajes) < N_MENSAJES:
            raise SystemExit(f"El archivo debe traer al menos {N_MENSAJES} mensajes.")
    else:
        mensajes = []
        for i in range(1, N_MENSAJES + 1):
            texto = ""
            while not texto:
                texto = input(f"\nMensaje {i}: ").strip()
            mensajes.append(texto)

    print("\nSupervisor: indica si cada mensaje es SPAM (s) o NO SPAM (n).")
    etiquetados = []
    for i, texto in enumerate(mensajes, 1):
        print(f"\n[{i}] {texto}")
        es_spam = preguntar_si_no("    ¿Es spam? (s/n): ")
        etiquetados.append({"id": i, "texto": texto, "spam": es_spam})

    n_spam = sum(m["spam"] for m in etiquetados)
    guardar({
        "descripcion": "Mensajes etiquetados por el Supervisor (R006 Entrenador)",
        "fecha": datetime.now().isoformat(timespec="seconds"),
        "total": len(etiquetados),
        "total_spam": n_spam,
        "total_no_spam": len(etiquetados) - n_spam,
        "mensajes": etiquetados,
    }, SALIDA)
    print(f"   Spam: {n_spam}   No spam: {len(etiquetados) - n_spam}")


if __name__ == "__main__":
    main()

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
        import yaml  # pip install pyyaml
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


def preguntar_si_no(pregunta):
    while True:
        r = quitar_acentos(input(pregunta).strip())
        if r in ("s", "si"):
            return True
        if r in ("n", "no"):
            return False
        print("   Responde 's' (sí) o 'n' (no).")


ENTRADA = "mensajes_clasificados.json"
SALIDA = "metricas.json"


def dividir(a, b):
    return a / b if b else 0.0


def main():
    datos = cargar(ENTRADA)
    mensajes = datos["mensajes"]

    print("=" * 60)
    print(" MÉTRICAS - El usuario etiqueta los mensajes nuevos")
    print("=" * 60)
    for m in mensajes:
        print(f"\n[{m['id']}] {m['texto']}")
        m["real"] = preguntar_si_no("    ¿Es spam? (s/n): ")

    vp = sum(1 for m in mensajes if m["spam"] and m["real"])
    fp = sum(1 for m in mensajes if m["spam"] and not m["real"])
    fn = sum(1 for m in mensajes if not m["spam"] and m["real"])
    vn = sum(1 for m in mensajes if not m["spam"] and not m["real"])
    total = vp + fp + fn + vn

    accuracy = dividir(vp + vn, total)
    precision = dividir(vp, vp + fp)
    recall = dividir(vp, vp + fn)
    prevalence = dividir(vp + fn, total)

    print("\n" + "=" * 60)
    print(" COMPARACIÓN  (sistema vs usuario)")
    print("=" * 60)
    for m in mensajes:
        s = "SPAM" if m["spam"] else "NO SPAM"
        r = "SPAM" if m["real"] else "NO SPAM"
        tipo = ("VP" if m["real"] else "FP") if m["spam"] else ("FN" if m["real"] else "VN")
        print(f" [{m['id']:>2}] sistema: {s:<8} usuario: {r:<8} -> {tipo}")

    print("\n MATRIZ DE CONFUSIÓN")
    print("                      Realidad (usuario)")
    print("                      Spam    No spam")
    print(f"   Sistema  Spam      {vp:>4}    {fp:>4}")
    print(f"            No spam   {fn:>4}    {vn:>4}")

    print("\n MÉTRICAS")
    print(f"   Accuracy   = ({vp}+{vn})/{total} = {accuracy:.2%}")
    print(f"   Precision  = {vp}/({vp}+{fp}) = {precision:.2%}")
    print(f"   Recall     = {vp}/({vp}+{fn}) = {recall:.2%}")
    print(f"   Prevalence = ({vp}+{fn})/{total} = {prevalence:.2%}")

    guardar({
        "descripcion": "Evaluación del clasificador (R009 Métricas)",
        "metodo_consenso": datos.get("metodo_consenso"),
        "umbral": datos.get("umbral"),
        "comparacion": [{"id": m["id"], "texto": m["texto"], "sistema": m["spam"], "usuario": m["real"]}
                        for m in mensajes],
        "matriz_confusion": {"VP": vp, "FP": fp, "FN": fn, "VN": vn},
        "metricas": {
            "accuracy": round(accuracy, 4),
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "prevalence": round(prevalence, 4),
        },
    }, SALIDA)


if __name__ == "__main__":
    main()

"""
Descripción: Carga y genera archivo de conocimiento  "DeTokenizador"
Restricciones: Se leen los mensajes etiquetados, se tokenizan dichos mensajes, se eliminan, articulos, preposiciones y conectores, se calcula la probabilidad condicional de los tokens restantes y se genera la tabla de probabilidades.
"""
import sys

from common import cargar, guardar, procesar


def calcular_tabla(datos):
    n_spam = sum(1 for d in datos if d["etiqueta"] == "spam")
    n_ham = len(datos) - n_spam
    if n_spam == 0 or n_ham == 0:
        print("AVISO: solo hay una clase en el entrenamiento; la tabla no será útil.")
    p_spam = n_spam / len(datos)
    p_ham = 1 - p_spam

    conteo = {}                                                
    for d in datos:
        for palabra in set(procesar(d["mensaje"])):                       
            conteo.setdefault(palabra, [0, 0])
            conteo[palabra][0 if d["etiqueta"] == "spam" else 1] += 1

    tokens = {}
    for palabra, (cs, ch) in sorted(conteo.items()):
        p_w_spam = (cs + 1) / (n_spam + 2)
        p_w_ham = (ch + 1) / (n_ham + 2)
        p_spam_w = (p_w_spam * p_spam) / (p_w_spam * p_spam + p_w_ham * p_ham)
        tokens[palabra] = {
            "spam": cs,
            "no_spam": ch,
            "tabla_2x2": {                         
                "palabra_spam": cs,
                "palabra_no_spam": ch,
                "sin_palabra_spam": n_spam - cs,
                "sin_palabra_no_spam": n_ham - ch,
                "total_palabra": cs + ch,
                "total": len(datos),
            },
            "p_spam_sin_laplace": round(cs / (cs + ch), 4),
            "p_spam_dado_palabra": round(p_spam_w, 4),                               
        }
    return {"p_spam": round(p_spam, 4), "tokens": tokens}


def main(entrada="conocimiento.json", salida="tabla_probabilidades.json"):
    tabla = calcular_tabla(cargar(entrada))
    guardar(salida, tabla)
    print(f"{len(tabla['tokens'])} palabras en la tabla. P(spam) = {tabla['p_spam']:.2f}")
    print(f"\n{'Palabra':<16}{'Spam':>5}{'No spam':>9}{'P(spam|w)':>11}")
    for w, d in sorted(tabla["tokens"].items(), key=lambda x: -x[1]["p_spam_dado_palabra"])[:15]:
        print(f"{w:<16}{d['spam']:>5}{d['no_spam']:>9}{d['p_spam_dado_palabra']:>11}")
    print("... (tabla completa en el archivo)")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "conocimiento.json",
         sys.argv[2] if len(sys.argv) > 2 else "tabla_probabilidades.json")

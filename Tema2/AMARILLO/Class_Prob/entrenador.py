"""
Descripción: Carga y genera archivo de conocimiento.  "Entrenador"
Restricciones: Se toman 10 mensajes en lenguaje natural y el Supervisor clasifica si son Spam o No, se genera un archivo con esos mensaje etiquetado.
"""
import sys

from common import guardar, preguntar_etiqueta, obtener_mensajes


def main(entrada=None, salida="conocimiento.json"):
    mensajes = obtener_mensajes(entrada)                                     
    etiquetados = [{"mensaje": m, "etiqueta": preguntar_etiqueta(m)} for m in mensajes]
    guardar(salida, etiquetados)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else None,
         sys.argv[2] if len(sys.argv) > 2 else "conocimiento.json")

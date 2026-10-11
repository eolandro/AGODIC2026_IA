import json
import re 

trash_basura = [
    "el", "la", "los", "las", "un", "una", "unos", "unas", "lo","am","pm",
    "a", "ante", "bajo", "cabe", "con", "contra", "de", "desde", "durante", 
    "en", "entre", "hacia", "hasta", "mediante", "para", "por", "según", 
    "sin", "so", "sobre", "tras", "versus", "vía", "del", "al",
    "y", "e", "ni", "que", "o", "u", "pero", "mas", "sino", "aunque", 
    "porque", "pues", "como", "si", "así","cuando", "donde",
    "mientras", "también", "tampoco", "además", "luego", "entonces", "este",
    "esta", "estos", "estas", "esto", "ese", "esa", "esos", "esas", 
    "eso", "aquel", "aquella", "aquellos", "aquellas", "aquello",
    "mi", "tu", "su", "mis", "tus", "sus", "nuestro", "nuestra", "nos", 
    "me", "te", "se", "les", "le", "yo", "tú", "él", "ella", "nosotros", 
    "vosotros", "ellos", "ellas"
]

def obtener_tokens(texto):
    texto_min = texto.lower()
    texto_limpio = re.sub(r'[^\w\s]', '', texto_min)
    palabras = texto_limpio.split()
    
    tokens = []
    for p in palabras:
        if p not in trash_basura:
            tokens.append(p)
    return tokens

def ejecutar_detokenizador():
    print("\n ********************* DETOKENIZADOR ***********************")
    
    archivo = open("msg0_etiquetados.json", "r", encoding="utf-8")
    mensajes = json.load(archivo)
    archivo.close()
    
    tot_msjs_si_spam = 0
    conteo_tokens = {}
    
    print("Procesando mensajes, eliminando basura y agrupando tokens...")
    
    for msg in mensajes:
        es_spam = msg["es_noes"]
        
        if es_spam == 1:
            tot_msjs_si_spam = tot_msjs_si_spam + 1
            
        texto = msg["msg0"]
        
        tokens_mensaje = obtener_tokens(texto)
        
        tokens_unicos = []
        for p in tokens_mensaje:
            if p not in tokens_unicos:
                tokens_unicos.append(p)
        
        for token in tokens_unicos:
            if token not in conteo_tokens:
                conteo_tokens[token] = {"spam": 0, "no_spam": 0}
            
            if es_spam == 1:
                conteo_tokens[token]["spam"] = conteo_tokens[token]["spam"] + 1
            else:
                conteo_tokens[token]["no_spam"] = conteo_tokens[token]["no_spam"] + 1

    tabla_probabilidades = {}

    for token in conteo_tokens:
        ocurrencias_spam = conteo_tokens[token]["spam"]
        
        if tot_msjs_si_spam > 0:
            probabilidad = ocurrencias_spam / tot_msjs_si_spam
        else:
            probabilidad = 0.0
        
        tabla_probabilidades[token] = round(probabilidad, 2)
        
    archivo_guardar = open("tabla_probabilidades.json", "w", encoding="utf-8")
    json.dump(tabla_probabilidades, archivo_guardar, ensure_ascii=False, indent=4)
    archivo_guardar.close()

    print("\n ¡Listo! Se generó 'tabla_probabilidades.json' con éxito")

if __name__ == "__main__":
    ejecutar_detokenizador()
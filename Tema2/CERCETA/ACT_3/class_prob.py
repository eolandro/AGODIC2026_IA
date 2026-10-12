import json
import re
from pathlib import Path

CARPETA = Path(__file__).resolve().parent
VACIAS = set('''el la los las un una unos unas a ante bajo con contra
de desde durante en entre hacia hasta mediante para por segun sin
sobre tras al del y e ni o u pero aunque porque que'''.split())


def guardar(nombre, datos):
    with (CARPETA / nombre).open('w', encoding='utf-8') as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def cargar(nombre):
    with (CARPETA / nombre).open(encoding='utf-8') as archivo:
        return json.load(archivo)


def preguntar():
    # Se muestra S/N al usuario; internamente se guarda 1/0 en los JSON.
    respuesta = input('¿Es spam? (S/N): ').strip().upper()
    while respuesta not in ('S', 'N'):
        respuesta = input('Escribe solamente S o N: ').strip().upper()
    return 1 if respuesta == 'S' else 0


def letra(valor):
    return 'S' if valor == 1 else 'N'


def leer_mensajes(nombre):
    mensajes = cargar(nombre)
    if not isinstance(mensajes, list) or len(mensajes) != 10:
        raise ValueError(f'{nombre} debe contener una lista de 10 mensajes.')
    if any(not isinstance(m, str) or not m.strip() for m in mensajes):
        raise ValueError('Todos los mensajes deben ser textos no vacíos.')
    claves = [' '.join(m.lower().split()) for m in mensajes]
    if len(set(claves)) != 10:
        raise ValueError('Los diez mensajes deben ser distintos.')
    return mensajes


def palabras(texto):
    texto = texto.lower().translate(str.maketrans('áéíóúü', 'aeiouu'))
    tokens = re.findall(r'[a-zñ]+', texto)
    return set(tokens) - VACIAS  # Una aparición por mensaje.


def borrar_resultados(nombres):
    for nombre in nombres:
        ruta = CARPETA / nombre
        if ruta.exists():
            ruta.unlink()


# R006: entrenador.
def entrenar():
    mensajes = leer_mensajes('mensajes_entrenamiento.json')
    etiquetados = []
    print('\n--- ENSÉÑALE AL RADAR ---')
    for numero, texto in enumerate(mensajes, 1):
        print(f'\nMensaje {numero}/10: {texto}')
        etiquetados.append({'texto': texto, 'spam': preguntar()})
    guardar('entrenamiento.json', etiquetados)
    borrar_resultados(['probabilidades.json', 'clasificados.json', 'evaluacion.json'])
    print('\nEntrenamiento guardado. Continúa con la opción 2.')


# R007: el requisito lo llama DeTokenizador; aquí se tokeniza.
def generar_probabilidades():
    mensajes = cargar('entrenamiento.json')
    tabla = {}
    for mensaje in mensajes:
        for palabra in palabras(mensaje['texto']):
            if palabra not in tabla:
                tabla[palabra] = {'spam': 0, 'no_spam': 0}
            if mensaje['spam'] == 1:
                tabla[palabra]['spam'] += 1
            else:
                tabla[palabra]['no_spam'] += 1
    for datos in tabla.values():
        total = datos['spam'] + datos['no_spam']
        datos['probabilidad'] = datos['spam'] / total
    guardar('probabilidades.json', tabla)
    borrar_resultados(['clasificados.json', 'evaluacion.json'])
    print(f'\nRadar preparado: {len(tabla)} palabras registradas.')
    ver_tabla()


def ver_tabla():
    tabla = cargar('probabilidades.json')
    print('\nPALABRA       SPAM  NO SPAM  P(SPAM)')
    print('-' * 38)
    for palabra, datos in sorted(tabla.items()):
        print(f"{palabra:13} {datos['spam']:4} {datos['no_spam']:8} "
              f"{datos['probabilidad']:8.0%}")


# R008: consenso mediante la media de probabilidades conocidas.
def clasificar():
    tabla = cargar('probabilidades.json')
    nuevos = leer_mensajes('mensajes_nuevos.json')
    entrenamiento = cargar('entrenamiento.json')
    anteriores = {' '.join(m['texto'].lower().split()) for m in entrenamiento}
    for texto in nuevos:
        if ' '.join(texto.lower().split()) in anteriores:
            raise ValueError('Los mensajes nuevos no deben repetir los de entrenamiento.')
    resultados = []
    for texto in nuevos:
        valores = []
        for palabra in palabras(texto):
            if palabra in tabla:
                valores.append(tabla[palabra]['probabilidad'])
        promedio = None
        prediccion = 0
        if valores:
            promedio = sum(valores) / len(valores)
            if promedio > 0.5:
                prediccion = 1
        resultados.append({'texto': texto, 'prediccion': prediccion,
                           'promedio': promedio, 'palabras_conocidas': len(valores)})
    guardar('clasificados.json', resultados)
    borrar_resultados(['evaluacion.json'])
    print(f'\nListo: {len(resultados)} mensajes clasificados.')
    print('Usa la opción 4 para evaluarlos.')


# R009: supervisor, matriz de confusión y métricas.
def evaluar():
    resultados = cargar('clasificados.json')
    print('\n--- PON A PRUEBA AL RADAR ---')
    print('Tu criterio será la referencia para evaluar al programa.')
    for numero, mensaje in enumerate(resultados, 1):
        print(f"\nMensaje {numero}/10: {mensaje['texto']}")
        mensaje['real'] = preguntar()
    vp = vn = fp = fn = 0
    for mensaje in resultados:
        real = mensaje['real']
        prediccion = mensaje['prediccion']
        if real == 1 and prediccion == 1:
            vp += 1
        elif real == 0 and prediccion == 0:
            vn += 1
        elif real == 0 and prediccion == 1:
            fp += 1
        else:
            fn += 1
    total = len(resultados)
    metricas = {
        'Accuracy': (vp + vn) / total,
        'Precision': vp / (vp + fp) if vp + fp else None,
        'Recall': vp / (vp + fn) if vp + fn else None,
        'Prevalence': (vp + fn) / total
    }
    print('\n--- REPORTE ---')
    print('S = spam | N = no spam\n')
    print('Tú  Radar')
    for mensaje in resultados:
        marca = '' if mensaje['real'] == mensaje['prediccion'] else '  <- error'
        print(f" {letra(mensaje['real'])}    {letra(mensaje['prediccion'])}    "
              f"{mensaje['texto']}{marca}")
    print('\nMATRIZ DE CONFUSIÓN')
    print('               Radar: S   Radar: N')
    print(f'Tú: S          {vp:8}   {fn:8}')
    print(f'Tú: N          {fp:8}   {vn:8}')
    print(f'\nAciertos: {vp + vn}/{total}\n')
    for nombre, valor in metricas.items():
        if valor is None:
            print(f'{nombre}: no definida')
        else:
            print(f'{nombre}: {valor:.0%}')
    guardar('evaluacion.json', {'mensajes': resultados,
            'matriz': {'VP': vp, 'VN': vn, 'FP': fp, 'FN': fn}, 'metricas': metricas})
    print('\nReporte guardado en evaluacion.json.')


def preparar_archivos():
    ejemplos = {
        'mensajes_entrenamiento.json': [
            'Reclama dinero gratis hoy', 'Oferta de descuento especial',
            'Ganaste dinero reclama tu regalo', 'Compra hoy con descuento',
            'Regalo gratis por tu compra', 'La reunion del equipo es hoy',
            'Envia el informe del equipo', 'La tarea se entrega el lunes',
            'Revisa el informe antes de la reunion', 'La clase del lunes tiene tarea'],
        'mensajes_nuevos.json': [
            'Reclama tu regalo gratis', 'La reunion es el lunes',
            'Compra con descuento especial', 'Envia la tarea del lunes',
            'Ganaste dinero gratis', 'Revisa el informe del equipo',
            'Oferta especial reclama hoy', 'La clase tiene tarea',
            'El informe habla del dinero gratis', 'Nos vemos durante el desayuno']
    }
    for nombre, mensajes in ejemplos.items():
        if not (CARPETA / nombre).exists():
            guardar(nombre, mensajes)


def menu():
    preparar_archivos()
    while True:
        print('''
==============================
   SPAMRADAR | Class_Prob
==============================
  1. Entrenar
  2. Calcular probabilidades
  3. Clasificar mensajes nuevos
  4. Evaluar
  5. Ver probabilidades
  6. Ayuda
  0. Salir
==============================''')
        opcion = input('Selecciona una opción: ').strip()
        try:
            if opcion == '1':
                entrenar()
            elif opcion == '2':
                generar_probabilidades()
            elif opcion == '3':
                clasificar()
            elif opcion == '4':
                evaluar()
            elif opcion == '5':
                ver_tabla()
            elif opcion == '6':
                print('''
1. Etiqueta 10 mensajes con S (spam) o N (no spam).
2. Calcula P(spam | palabra) para cada palabra.
3. Clasifica 10 mensajes nuevos con la media.
4. Etiquétalos tú y compara con el radar.

P(spam | palabra) = mensajes spam con la palabra /
                    todos los mensajes con la palabra.
Media mayor a 0.5 = spam; si no, no spam.

Puedes editar mensajes_entrenamiento.json y
mensajes_nuevos.json (10 mensajes distintos cada uno).''')
            elif opcion == '0':
                print('\nRadar apagado. ¡Hasta la próxima!')
                break
            else:
                print('\nElige una opción del 0 al 6.')
        except FileNotFoundError:
            print('\nFalta un archivo. Sigue el orden: 1 → 2 → 3 → 4.')
        except json.JSONDecodeError:
            print('\nUn archivo JSON está mal escrito. Revisa su formato.')
        except ValueError as error:
            print('\n', error)
        input('\nPresiona Enter para regresar al menú...')


if __name__ == '__main__':
    menu()

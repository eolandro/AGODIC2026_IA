import argparse
import heapq
import json
import os
import sys

CONFIG_DEFECTO = {
    "costo_recto": 1,
}

MOVIMIENTOS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

ROBOT, BOMBA, OBST, LIBRE_MAPA = "R", "B", "X", "0"
LIBRE = "."  

avisos = []

def avisar(texto):
    avisos.append(texto)

def salir(texto):
    print(f"\n[ERROR] {texto}")
    sys.exit(1)

def ubicar_archivo(ruta):
    carpetas = [os.getcwd(), os.path.dirname(os.path.abspath(__file__))]
    if ruta:
        if os.path.isfile(ruta):
            return ruta
        for carpeta in carpetas:
            candidato = os.path.join(carpeta, ruta)
            if os.path.isfile(candidato):
                return candidato
        salir(f"No se encontró el archivo '{ruta}'.")
    for carpeta in carpetas:
        for nombre in ("mapa.json", "mapa.yaml", "mapa.yml"):
            candidato = os.path.join(carpeta, nombre)
            if os.path.isfile(candidato):
                return candidato
    script = os.path.basename(__file__)
    salir(f"No se encontró mapa.json ni mapa.yaml. Indica el archivo: python {script} mapa.json")

def cargar_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8-sig") as f:
            texto = f.read()
    except UnicodeDecodeError:
        with open(ruta, "r", encoding="latin-1") as f:
            texto = f.read()

    if not texto.strip():
        salir(f"El archivo '{ruta}' está vacío.")

    extension = os.path.splitext(ruta)[1].lower()
    if extension in (".yaml", ".yml"):
        try:
            import yaml
        except ImportError:
            try:
                return json.loads(texto)
            except json.JSONDecodeError:
                salir("Para leer YAML instala PyYAML:  pip install pyyaml   (o usa el mapa en JSON)")
        try:
            return yaml.safe_load(texto)
        except yaml.YAMLError as e:
            salir(f"El YAML tiene un error de formato:\n        {e}")

    try:
        return json.loads(texto)
    except json.JSONDecodeError as e:
        lineas = texto.splitlines()
        linea = lineas[e.lineno - 1] if 0 < e.lineno <= len(lineas) else ""
        pista = ""
        if "trailing comma" in e.msg or "Expecting property name" in e.msg:
            pista = "\n        Pista: sobra una coma antes de ] o }, o hay comillas simples (usa dobles \")."
        elif "Expecting ',' delimiter" in e.msg:
            pista = "\n        Pista: falta una coma entre dos filas o valores."
        elif "Expecting value" in e.msg:
            pista = ("\n        Pista: las letras deben ir entre comillas dobles (\"R\", \"B\", \"X\"),"
                     " o sobra una coma al final de la lista.")
        salir(f"El JSON tiene un error en la línea {e.lineno}, columna {e.colno}: {e.msg}\n"
              f"        >> {linea.strip()}{pista}")

def buscar_clave(datos, nombres):
    if not isinstance(datos, dict):
        return None
    normal = {str(k).strip().lower(): v for k, v in datos.items()}
    for n in nombres:
        if n in normal:
            return normal[n]
    return None

def leer_config(datos):
    config = dict(CONFIG_DEFECTO)
    personal = buscar_clave(datos, ["configuracion", "configuración", "config", "opciones"])
    fuente = personal if isinstance(personal, dict) else datos
    if not isinstance(fuente, dict):
        return config

    ignoradas = [c for c in ("diagonales", "costo_diagonal", "esquinas", "heuristica", "heurística")
                 if buscar_clave(fuente, [c]) is not None]
    if ignoradas:
        avisar(f"Se ignoraron las opciones {', '.join(ignoradas)}: "
               f"Boome solo se mueve en 4 direcciones y usa Manhattan.")

    valor = buscar_clave(fuente, ["costo_recto"])
    if valor is not None:
        try:
            numero = float(valor)
            if numero <= 0:
                raise ValueError
            config["costo_recto"] = numero
        except (TypeError, ValueError):
            avisar(f"Valor inválido para 'costo_recto' ({valor}); se usa {CONFIG_DEFECTO['costo_recto']}.")
    return config

def separar_fila(fila):
    if isinstance(fila, list):
        celdas = []
        for c in fila:
            c = "" if c is None else str(c).strip()
            celdas.append(c if c else " ")
        return celdas
    texto = str(fila).rstrip("\n\r")
    for sep in (",", ";", "|", "\t"):
        texto = texto.replace(sep, " ")
    if " " in texto.strip():
        return texto.split()
    return list(texto.strip())

def construir_desde_coordenadas(datos):
    filas = buscar_clave(datos, ["filas", "alto"])
    cols = buscar_clave(datos, ["columnas", "ancho"])
    robot = buscar_clave(datos, ["robot", "inicio", "boome"])
    bomba = buscar_clave(datos, ["bomba", "bombas", "meta"])
    if filas is None or cols is None or robot is None or bomba is None:
        return None
    try:
        filas, cols = int(filas), int(cols)
        tablero = [[LIBRE] * cols for _ in range(filas)]
        for f, c in buscar_clave(datos, ["obstaculos", "obstáculos", "paredes"]) or []:
            tablero[int(f)][int(c)] = OBST
        tablero[int(robot[0])][int(robot[1])] = ROBOT
        lista_bombas = bomba if isinstance(bomba[0], list) else [bomba]
        for f, c in lista_bombas:
            tablero[int(f)][int(c)] = BOMBA
        return tablero
    except (TypeError, ValueError, IndexError):
        salir("Las coordenadas del mapa están fuera del tablero o mal escritas.")

def leer_mapa(ruta):
    datos = cargar_archivo(ruta)
    config = leer_config(datos)

    if isinstance(datos, list):
        filas_crudas = datos
    else:
        filas_crudas = buscar_clave(datos, ["tablero", "mapa", "grid", "matriz", "escenario", "board"])
        if isinstance(filas_crudas, str):
            filas_crudas = [l for l in filas_crudas.splitlines() if l.strip()]
        if filas_crudas is None:
            tablero = construir_desde_coordenadas(datos)
            if tablero is None:
                salir("El archivo no tiene la clave \"tablero\" (lista de filas).")
            return tablero, config

    if not isinstance(filas_crudas, list) or not filas_crudas:
        salir("El tablero está vacío o no es una lista de filas.")

    tablero = []
    for i, fila in enumerate(filas_crudas, start=1):
        celdas = separar_fila(fila)
        if not celdas or all(c == " " for c in celdas):
            avisar(f"La fila {i} está vacía y se ignoró.")
            continue
        convertida = []
        for c in celdas:
            s = c.upper()
            if s in (ROBOT, BOMBA, OBST):
                convertida.append(s)
            elif s == LIBRE_MAPA:
                convertida.append(LIBRE)
            else:
                avisar(f"Símbolo desconocido '{c}' en la fila {i}; se tomó como obstáculo "
                       f"(solo se usan R, B, X y 0).")
                convertida.append(OBST)
        tablero.append(convertida)

    if not tablero:
        salir("El tablero no tiene filas válidas.")

    ancho = max(len(f) for f in tablero)
    for i, fila in enumerate(tablero, start=1):
        if len(fila) < ancho:
            avisar(f"La fila {i} tiene {len(fila)} columnas (se esperaban {ancho}); "
                   f"se completó con casillas libres.")
            fila.extend([LIBRE] * (ancho - len(fila)))
    return tablero, config

def validar(tablero):
    robots = [(f, c) for f, fila in enumerate(tablero) for c, s in enumerate(fila) if s == ROBOT]
    bombas = [(f, c) for f, fila in enumerate(tablero) for c, s in enumerate(fila) if s == BOMBA]
    if not robots:
        salir("No hay robot en el mapa. Coloca una 'R' en el tablero.")
    if not bombas:
        salir("No hay bomba en el mapa. Coloca una 'B' en el tablero.")
    if len(robots) > 1:
        avisar(f"Hay {len(robots)} robots; se usa el primero {coord(robots[0])} "
               f"y los demás se tratan como casillas libres.")
        for r in robots[1:]:
            tablero[r[0]][r[1]] = LIBRE
    if len(bombas) > 1:
        avisar(f"Hay {len(bombas)} bombas; Boome irá a la que le cueste menos llegar.")
    return robots[0], bombas

def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def vecinos(tablero, celda, config):
    filas, cols = len(tablero), len(tablero[0])
    for df, dc in MOVIMIENTOS:
        nf, nc = celda[0] + df, celda[1] + dc
        if 0 <= nf < filas and 0 <= nc < cols and tablero[nf][nc] != OBST:
            yield (nf, nc), config["costo_recto"]

def a_estrella(tablero, inicio, bombas, config, mostrar_pasos=False):
    costo = config["costo_recto"]
    metas = set(bombas)

    def h(n):
        return min(manhattan(n, b) for b in bombas) * costo

    g = {inicio: 0}
    hv = {inicio: h(inicio)}
    padre = {inicio: None}
    contador = 0
    abiertos = [(hv[inicio], hv[inicio], contador, inicio)]
    cerrados, cerrados_set = [], set()

    while abiertos:
        f_act, _, _, actual = heapq.heappop(abiertos)
        if actual in cerrados_set:
            continue
        cerrados.append(actual)
        cerrados_set.add(actual)

        if mostrar_pasos:
            pendientes = sorted({(g[n] + hv[n], n) for *_, n in abiertos if n not in cerrados_set})
            texto = ", ".join(f"{coord(n)}={num(fv)}" for fv, n in pendientes[:8])
            if len(pendientes) > 8:
                texto += f", ... (+{len(pendientes) - 8})"
            print(f"  It {len(cerrados):>3}: expando {coord(actual):<7} g={num(g[actual]):<3} "
                  f"h={num(hv[actual]):<3} f={num(f_act):<3}| abiertos: {texto or '-'}")

        if actual in metas:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1], g, hv, cerrados

        for vecino, paso in vecinos(tablero, actual, config):
            if vecino in cerrados_set:
                continue
            g_nuevo = g[actual] + paso
            if vecino not in g or g_nuevo < g[vecino]:
                g[vecino] = g_nuevo
                hv[vecino] = h(vecino)
                padre[vecino] = actual
                contador += 1
                heapq.heappush(abiertos, (g_nuevo + hv[vecino], hv[vecino], contador, vecino))

    return None, g, hv, cerrados

def coord(celda):
    return f"({celda[0] + 1},{celda[1] + 1})"

def num(x):
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}"

def encabezado_columnas(cols, ancho):
    return "    " + "".join(str(c + 1).rjust(ancho) for c in range(cols))

def imprimir_tablero(tablero, titulo, camino=None):
    marcas = set(camino[1:-1]) if camino else set()
    print(f"\n{titulo}")
    print(encabezado_columnas(len(tablero[0]), 3))
    for f, fila in enumerate(tablero):
        celdas = ["*" if (f, c) in marcas else s for c, s in enumerate(fila)]
        print(f"{f + 1:>3} " + "".join(s.rjust(3) for s in celdas))

def imprimir_valores(tablero, valores, titulo, camino):
    en_camino = set(camino) if camino else set()
    textos = {}
    for f, fila in enumerate(tablero):
        for c, s in enumerate(fila):
            if s == OBST:
                textos[(f, c)] = "X"
            elif (f, c) in valores:
                textos[(f, c)] = num(valores[(f, c)]) + ("*" if (f, c) in en_camino else "")
            else:
                textos[(f, c)] = "."
    ancho = max(4, max(len(t) for t in textos.values()) + 1)
    print(f"\n{titulo}")
    print(encabezado_columnas(len(tablero[0]), ancho))
    for f in range(len(tablero)):
        print(f"{f + 1:>3} " + "".join(textos[(f, c)].rjust(ancho) for c in range(len(tablero[0]))))

def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Boome busca la bomba con A* (Manhattan, 4 direcciones).")
    parser.add_argument("archivo", nargs="?", help="mapa en JSON o YAML (por defecto mapa.json)")
    parser.add_argument("--pasos", action="store_true", help="muestra cada iteración de A*")
    args = parser.parse_args()

    ruta = ubicar_archivo(args.archivo)
    tablero, config = leer_mapa(ruta)
    inicio, bombas = validar(tablero)

    print("\n")
    print("=" * 60)
    print("   BOOME - Búsqueda de la bomba con A*")
    print("=" * 60)
    print(f"\nMapa        : {os.path.basename(ruta)}")
    print(f"Tamaño      : {len(tablero)} filas x {len(tablero[0])} columnas")
    print(f"Boome (R)   : {coord(inicio)}")
    print(f"Bomba(s) (B): {', '.join(coord(b) for b in bombas)}")
    print(f"Movimientos : 4 direcciones, sin diagonales (costo={num(config['costo_recto'])})")
    print("Heurística  : manhattan")
    print("Coordenadas : (fila, columna), empezando en 1\n")
    print("=" * 60)

    imprimir_tablero(tablero, "Tablero leído  (R=Boome, B=bomba, X=obstáculo, .=libre):\n")

    if args.pasos:
        print("\nRecorrido de A* (siempre se expande el nodo con menor f):")
    camino, g, h, cerrados = a_estrella(tablero, inicio, bombas, config, args.pasos)

    if avisos:
        print("\nAvisos al leer el mapa:")
        for a in dict.fromkeys(avisos):
            print(f"  - {a}")

    imprimir_valores(tablero, g, "g(n) - costo desde Boome  (* = camino):\n", camino)
    imprimir_valores(tablero, h, "h(n) - distancia Manhattan hasta la bomba:\n", camino)
    f_vals = {n: g[n] + h[n] for n in g}
    imprimir_valores(tablero, f_vals, "f(n) = g(n) + h(n):\n", camino)

    print()
    if camino is None:
        print("[!] Boome NO puede llegar a la bomba: está bloqueada por obstáculos.")
        print(f"    Casillas exploradas: {len(cerrados)}")
        return

    imprimir_tablero(tablero, "\nCamino encontrado (*):\n", camino)
    print("\nRuta de Boome: " + " -> ".join(coord(c) for c in camino))
    print(f"\nMovimientos      : {len(camino) - 1}")
    print(f"Costo total      : {num(g[camino[-1]])}")
    print(f"Nodos expandidos : {len(cerrados)}")
    if len(camino) == 1:
        print("\nBoome ya estaba sobre la bomba.")
    else:
        print(f"\n¡Boome llegó a la bomba en {coord(camino[-1])} y la desactivó!")

if __name__ == "__main__":
    main()
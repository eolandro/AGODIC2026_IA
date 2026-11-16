import heapq
import json
import os


class BommeVirtualMachine:
	"""
	Maquina virtual de Boome con pathfinding A*.

	Simbolos del tablero (archivo JSON o YAML):
		0 -> celda libre
		X -> bloqueo (tambien se acepta 1)
		R -> posicion inicial de Boome
		B -> bomba (solo una; opcional, el maestro puede elegirla al ejecutar)

	Boome solo se mueve en 4 direcciones (arriba, abajo, izq, der) con costo 1,
	NO se permiten movimientos en diagonal, por eso la heuristica es la
	distancia Manhattan: nunca sobreestima el costo real (heuristica admisible)
	y A* garantiza el camino mas corto.

		f(n) = g(n) + h(n)
		g(n): pasos reales desde R hasta n
		h(n): |fila_n - fila_B| + |col_n - col_B|
	"""

	DIRECCIONES = {
		"arriba": (-1, 0),
		"abajo": (1, 0),
		"izq": (0, -1),
		"der": (0, 1),
	}

	def __init__(self, archivo_tablero="tablero.json"):
		self.RBPos = None        # posicion actual de Boome
		self.Inicio = None       # posicion inicial (R)
		self.Bomba = None        # posicion de la bomba (B)
		self.Mapa = self.LoadTablero(archivo_tablero)
		################ Resultado de A*
		self.Camino = []         # celdas desde R hasta B
		self.Instrucciones = []  # movimientos (arriba, abajo, izq, der)
		self.RIP = None
		self.Expandidos = 0
		self.Estado = "wait"

	# ------------------------------------------------------------------
	# Lectura del tablero desde archivo (JSON o YAML)
	# ------------------------------------------------------------------
	@staticmethod
	def LeerArchivo(archivo):
		ext = os.path.splitext(archivo)[1].lower()
		with open(archivo, "r", encoding="utf-8") as f:
			if ext == ".json":
				return json.load(f)
			if ext in (".yaml", ".yml"):
				try:
					import yaml
				except ImportError:
					raise SystemExit("Para leer YAML instala PyYAML:  pip install pyyaml")
				return yaml.safe_load(f)
		raise ValueError(f"Formato no soportado: '{ext}' (usa .json, .yaml o .yml)")

	def LoadTablero(self, archivo):
		"""Convierte el tablero ya validado por anlexsyn en la matriz 0/1."""
		datos = self.LeerArchivo(archivo)
		self.Datos = datos
		Mapa = []
		for x, F in enumerate(datos["tablero"]):
			valores = F.split() if isinstance(F, str) else [str(v) for v in F]
			fila = []
			for y, valor in enumerate(valores):
				match valor.upper():
					case "X" | "1":
						fila.append(1)
					case "R":
						self.Inicio = (x, y)
						fila.append(0)
					case "B":
						self.Bomba = (x, y)
						fila.append(0)
					case _:
						fila.append(0)
			Mapa.append(fila)
		self.RBPos = self.Inicio
		return Mapa

	# ------------------------------------------------------------------
	# El maestro elige donde colocar la bomba
	# ------------------------------------------------------------------
	def NumCasilla(self, x, y):
		"""Numero lineal de la casilla (fila * columnas + columna), empezando en 0."""
		return x * len(self.Mapa[0]) + y

	def InterpretarPosicion(self, texto):
		"""Acepta el numero de casilla (ej. 57) o fila,columna (ej. 5,7)."""
		filas, columnas = len(self.Mapa), len(self.Mapa[0])
		texto = str(texto).strip().replace(" ", "")
		try:
			if "," in texto:
				x, y = (int(v) for v in texto.split(","))
			else:
				n = int(texto)
				if not 0 <= n < filas * columnas:
					raise ValueError(f"La casilla {n} no existe (0 a {filas * columnas - 1})")
				x, y = divmod(n, columnas)
		except ValueError as e:
			if "no existe" in str(e):
				raise
			raise ValueError(f"'{texto}' no es una posicion valida")
		if not (0 <= x < filas and 0 <= y < columnas):
			raise ValueError(f"({x},{y}) esta fuera del tablero {filas}x{columnas}")
		return (x, y)

	def ColocarBomba(self, texto):
		x, y = self.InterpretarPosicion(texto)
		if self.Mapa[x][y] == 1:
			raise ValueError(f"No se puede poner la bomba en ({x}, {y}): hay un bloqueo X")
		if (x, y) == self.Inicio:
			raise ValueError("No se puede poner la bomba sobre Boome (R)")
		self.Bomba = (x, y)

	# ------------------------------------------------------------------
	# A*
	# ------------------------------------------------------------------
	@staticmethod
	def Heuristica(a, b):
		"""Distancia Manhattan."""
		return abs(a[0] - b[0]) + abs(a[1] - b[1])

	def AEstrella(self):
		"""
		Busca el camino mas corto de R a B.
		Lista abierta: heap ordenado por f (en empate, menor h).
		Lista cerrada: celdas ya revisadas.
		Regresa True si encontro camino.
		"""
		if self.Bomba is None:
			raise ValueError("No hay bomba en el tablero")
		inicio, meta = self.Inicio, self.Bomba
		filas, columnas = len(self.Mapa), len(self.Mapa[0])
		contador = 0
		h0 = self.Heuristica(inicio, meta)
		abiertos = [(h0, h0, contador, inicio)]   # (f, h, orden, celda)
		g = {inicio: 0}
		padre = {inicio: None}                   # celda -> (anterior, direccion)
		cerrados = set()

		while abiertos:
			_, _, _, actual = heapq.heappop(abiertos)
			if actual in cerrados:
				continue
			if actual == meta:
				self.Expandidos = len(cerrados)
				self.Reconstruir(padre, meta)
				return True
			cerrados.add(actual)

			# Solo 4 vecinos: arriba, abajo, izq, der (sin diagonales)
			for direccion, (dx, dy) in self.DIRECCIONES.items():
				vecino = (actual[0] + dx, actual[1] + dy)
				if not (0 <= vecino[0] < filas and 0 <= vecino[1] < columnas):
					continue
				if self.Mapa[vecino[0]][vecino[1]] == 1 or vecino in cerrados:
					continue
				nuevo_g = g[actual] + 1
				if nuevo_g < g.get(vecino, float("inf")):
					g[vecino] = nuevo_g
					padre[vecino] = (actual, direccion)
					hv = self.Heuristica(vecino, meta)
					contador += 1
					heapq.heappush(abiertos, (nuevo_g + hv, hv, contador, vecino))

		self.Expandidos = len(cerrados)
		self.Estado = "sin camino"
		return False

	def Reconstruir(self, padre, meta):
		camino, movimientos = [meta], []
		actual = meta
		while padre[actual] is not None:
			anterior, direccion = padre[actual]
			camino.append(anterior)
			movimientos.append(direccion)
			actual = anterior
		self.Camino = camino[::-1]
		self.LoadText(movimientos[::-1])

	# ------------------------------------------------------------------
	# Ejecucion: Boome recorre el camino que encontro A*
	# ------------------------------------------------------------------
	def LoadText(self, L):
		if not L:
			return
		self.Instrucciones = [a for a in L]
		self.RIP = 0
		self.Estado = "ready"

	def Mover(self, direccion):
		dx, dy = self.DIRECCIONES[direccion]
		x, y = self.RBPos
		nx, ny = x + dx, y + dy
		if nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[0]):
			self.Estado = "dead"
			return
		if self.Mapa[nx][ny] == 1:
			self.Estado = "dead"
			return
		self.RBPos = (nx, ny)
		if self.RBPos == self.Bomba:
			self.Estado = "done"     # Boome llego a la bomba

	def step(self):
		if self.Estado != "ready":
			return
		self.Mover(self.Instrucciones[self.RIP])
		self.RIP += 1
		if self.Estado == "ready" and self.RIP >= len(self.Instrucciones):
			self.Estado = "done"

	# ------------------------------------------------------------------
	# Impresion
	# ------------------------------------------------------------------
	def AgruparMovimientos(self):
		"""['der','der','abajo'] -> 'der x2, abajo x1'"""
		grupos = []
		for m in self.Instrucciones:
			if grupos and grupos[-1][0] == m:
				grupos[-1][1] += 1
			else:
				grupos.append([m, 1])
		return ", ".join(f"{m} x{n}" for m, n in grupos)

	def CaminoResultante(self):
		S = "===== Camino resultante (A*) =====\n"
		S += str(self) + "\n"
		S += "Casillas: " + " -> ".join(str(self.NumCasilla(x, y)) for x, y in self.Camino) + "\n"
		S += "Movimientos: " + self.AgruparMovimientos() + "\n"
		S += f"Longitud del camino: {len(self.Instrucciones)} pasos  |  nodos expandidos: {self.Expandidos}"
		return S

	def __str__(self):
		en_camino = set(self.Camino)
		S = ""
		for x, fila in enumerate(self.Mapa):
			celdas = []
			for y, v in enumerate(fila):
				if (x, y) == self.Inicio:
					celdas.append("R")
				elif (x, y) == self.Bomba:
					celdas.append("B")
				elif v == 1:
					celdas.append("X")
				elif (x, y) in en_camino:
					celdas.append("*")
				else:
					celdas.append(".")
			S += " ".join(celdas) + "\n"
		return S

import random


class BommeVirtualMachine:
	"""
	Maquina virtual de Boome con detector bayesiano de bombas.

	Simbolos del mapa (archivo de texto, separados por espacios):
		0 -> celda libre
		1 -> obstaculo
		B -> bomba (oculta para Boome, celda libre en apariencia)
		R -> posicion inicial de Boome (celda libre)
	"""

	DIRECCIONES = {
		"arriba": (-1, 0),
		"abajo": (1, 0),
		"izq": (0, -1),
		"der": (0, 1),
	}

	def __init__(self, archivo_mapa="mapa.txt", sensibilidad=0.9,
				 falso_positivo=0.1, umbral=0.5, umbral_seguro=0.0001,
				 min_lecturas=3, max_lecturas=15, semilla=None):
		################R0,R1,R2,R3
		self.Registros = [0, 0, 0, 0]
		self.Instrucciones = []
		self.RIP = None
		self.Saltos = {}
		################
		self.RBPos = [0, 0]      # posicion de Boome (se puede cambiar con R en el mapa)
		self.Bombas = []         # posiciones de bombas leidas del mapa
		self.Mapa = self.LoadMapa(archivo_mapa)
		################ Parametros del detector (modelo bayesiano)
		self.Sens = sensibilidad        # P(+ | bomba)
		self.FP = falso_positivo        # P(+ | no bomba)
		self.Umbral = umbral            # P(B|evidencia) >= umbral -> peligro
		self.UmbralSeguro = umbral_seguro
		self.MinLecturas = min_lecturas # evita confiar en un solo falso negativo
		self.MaxLecturas = max_lecturas
		self.Rng = random.Random(semilla)
		self.Prior = self.CalcularPrior()
		self.Creencias = {}             # (x,y) -> ultima P(bomba) calculada
		self.Positivos = []             # historial de detecciones positivas
		self.Estado = "wait"

	# ------------------------------------------------------------------
	# R010: Leer tablero de Boome desde archivo
	# ------------------------------------------------------------------
	def LoadMapa(self, archivo):
		Mapa = []
		inicio = None
		with open(archivo, "r", encoding="utf-8") as f:
			for linea in f:
				linea = linea.strip()
				if not linea:  # ignorar lineas vacias
					continue
				fila = []
				for valor in linea.split():
					x, y = len(Mapa), len(fila)
					match valor.upper():
						case "0":
							fila.append(0)
						case "1":
							fila.append(1)
						case "B":
							self.Bombas.append([x, y])
							fila.append(0)
						case "R":
							if inicio is not None:
								raise ValueError("El mapa tiene mas de una R (posicion de Boome)")
							inicio = [x, y]
							fila.append(0)
						case _:
							raise ValueError(f"Simbolo no valido en el mapa: '{valor}' (fila {x+1}, col {y+1})")
				Mapa.append(fila)

		if not Mapa:
			raise ValueError("El mapa esta vacio")
		columnas = len(Mapa[0])
		if any(len(fila) != columnas for fila in Mapa):
			raise ValueError("Todas las filas deben tener el mismo numero de columnas")
		if inicio is not None:
			self.RBPos = inicio
		if self.RBPos in self.Bombas:
			raise ValueError("Boome no puede iniciar sobre una bomba")
		if Mapa[self.RBPos[0]][self.RBPos[1]] == 1:
			raise ValueError("Boome no puede iniciar sobre un obstaculo")
		return Mapa

	def CalcularPrior(self):
		"""P(B): bombas / celdas libres donde podria haber bomba (sin contar el inicio)."""
		libres = sum(fila.count(0) for fila in self.Mapa) - 1
		if libres <= 0:
			return 0.0
		return len(self.Bombas) / libres

	def LoadText(self, L):
		if not L:
			return
		self.Instrucciones = [a for a in L]
		self.Saltos = self._construir_saltos(self.Instrucciones)
		self.Estado = "ready"
		self.RIP = 0

	# ------------------------------------------------------------------
	# Teorema de Bayes
	# ------------------------------------------------------------------
	def Bayes(self, prior, positivo):
		"""
		Positivo: P(B|+) = P(+|B)P(B) / [P(+|B)P(B) + P(+|~B)P(~B)]
		Negativo: P(B|-) = P(-|B)P(B) / [P(-|B)P(B) + P(-|~B)P(~B)]
		"""
		if positivo:
			num = self.Sens * prior
			den = num + self.FP * (1 - prior)
		else:
			num = (1 - self.Sens) * prior
			den = num + (1 - self.FP) * (1 - prior)
		return (num / den if den else 0.0), num, den

	def LeerDetector(self, celda):
		"""Simula una lectura ruidosa del detector sobre la celda."""
		hay_bomba = list(celda) in self.Bombas
		p_positivo = self.Sens if hay_bomba else self.FP
		return self.Rng.random() < p_positivo

	# ------------------------------------------------------------------
	# R011: Imprimir la probabilidad de Bayes por detector positivo
	# ------------------------------------------------------------------
	def NumCasilla(self, x, y):
		"""Numero lineal de la casilla (fila * columnas + columna), empezando en 0."""
		return x * len(self.Mapa[0]) + y

	def Detector(self, direccion):
		"""
		Revisa la casilla vecina y decide con Bayes si tiene bomba.
		Fase 1 (verificacion): hasta MinLecturas lecturas; si todas son negativas
		y la probabilidad queda muy baja -> "No hay lectura registrada".
		Asi un solo falso negativo ya no basta para que Boome pise una bomba.
		Fase 2 (intentos): ante un positivo se hacen los intentos, cada uno
		actualiza P(B) con Bayes (el posterior de un intento es el prior del siguiente).
		Regresa 1 si la casilla es peligrosa (P >= umbral) o 0 si es segura.
		"""
		dx, dy = self.DIRECCIONES[direccion]
		x, y = self.RBPos
		nx, ny = x + dx, y + dy

		if nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[0]):
			print(f"\nBoom está revisando hacia {direccion}: fuera del mapa, no hay casilla.")
			return 0
		n = self.NumCasilla(nx, ny)
		print(f"\nBoom está revisando la casilla: {n}")
		if self.Mapa[nx][ny] == 1:
			print("La casilla es un obstáculo (no puede tener bomba).")
			return 0

		celda = (nx, ny)
		p = self.Creencias.get(celda, self.Prior)

		# ---- Fase 1: lecturas de verificacion (cubre falsos negativos)
		positivo_en = None
		anterior = p
		for k in range(1, self.MinLecturas + 1):
			lectura = self.LeerDetector(celda)
			anterior = p
			p, _, _ = self.Bayes(p, lectura)
			if lectura:
				positivo_en = k
				break

		if positivo_en is None and p <= self.UmbralSeguro:
			self.Creencias[celda] = p
			print("No hay lectura registrada.")
			return 0

		# ---- Fase 2: intentos bayesianos
		if positivo_en == 1:
			print("Lectura inicial: positivo")
		elif positivo_en:
			print("Lectura inicial: negativo")
			print(f"Lectura de verificación {positivo_en}: positivo (posible falso negativo detectado)")
		else:
			print("Lecturas negativas, pero la evidencia previa aún indica riesgo")
		if positivo_en:
			self.Positivos.append((celda, 1, anterior, p))
		print(f"Intento 1: {p * 100:.2f}%")

		intento = 1
		while True:
			intento += 1
			if intento > self.MinLecturas:
				if intento == self.MinLecturas + 1:
					print(f"Boom terminó los {self.NumeroEnLetra(self.MinLecturas)} intentos.")
				# Si el resultado no es concluyente, sigue revisando
				if p >= self.Umbral or p <= self.UmbralSeguro or intento > self.MaxLecturas:
					break
				if intento == self.MinLecturas + 1:
					print(f"(Para declararla segura se requiere P < {self.UmbralSeguro * 100:.2f}%, "
						  f"para declarar bomba P >= {self.Umbral * 100:.0f}%)")
				print(f"Resultado no concluyente, realizando intento {intento} ...")
			else:
				print(f"Realizando intento {intento} ...")
			lectura = self.LeerDetector(celda)
			anterior = p
			p, _, _ = self.Bayes(p, lectura)
			if lectura:
				self.Positivos.append((celda, intento, anterior, p))
			tipo = "positiva" if lectura else "negativa"
			print(f"Intento {intento}: probabilidad de bomba = {p * 100:.2f}%  (lectura {tipo})")

		self.Creencias[celda] = p
		if p >= self.Umbral:
			print(f"Decisión: {p * 100:.2f}% >= {self.Umbral * 100:.0f}% -> hay bomba, Boom NO avanza.")
			return 1
		print(f"Decisión: {p * 100:.2f}% < {self.Umbral * 100:.0f}% -> casilla segura, Boom puede avanzar.")
		return 0

	@staticmethod
	def NumeroEnLetra(n):
		letras = {1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco",
				  6: "seis", 7: "siete", 8: "ocho", 9: "nueve", 10: "diez"}
		return letras.get(n, str(n))

	# ------------------------------------------------------------------
	# Ejecucion
	# ------------------------------------------------------------------
	def RegIndex(self, R):
		return int(R[1])

	def ParseHex(self, cadena):
		if len(cadena) != 5 or not cadena.startswith("#"):
			raise ValueError(f"Hex invalido: {cadena}")
		return int(cadena[1:], 16)

	def Valor(self, token):
		if token.startswith("R"):
			return self.Registros[self.RegIndex(token)]
		return self.ParseHex(token)

	def Sensor(self, direccion):
		dx, dy = self.DIRECCIONES[direccion]
		x, y = self.RBPos
		nx, ny = x + dx, y + dy
		if nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[0]):
			return 1  # fuera del mapa cuenta como obstaculo
		return self.Mapa[nx][ny]

	def Mover(self, direccion):
		dx, dy = self.DIRECCIONES[direccion]
		x, y = self.RBPos
		nx, ny = x + dx, y + dy
		if nx < 0 or nx >= len(self.Mapa) or ny < 0 or ny >= len(self.Mapa[0]):
			print(f"\nBoom se salió del mapa al moverse {direccion}.")
			self.Estado = "dead"
			return
		if self.Mapa[nx][ny] == 1:
			print(f"\nBoom chocó con un obstáculo en la casilla {self.NumCasilla(nx, ny)}.")
			self.Estado = "dead"
			return
		self.RBPos = [nx, ny]
		if self.RBPos in self.Bombas:
			print(f"\n¡BOOM! Había una bomba en la casilla {self.NumCasilla(nx, ny)}.")
			self.Estado = "boom"
			return
		print(f"\n>> Boom avanza ({direccion}) a la casilla: {self.NumCasilla(nx, ny)}")
		self.Creencias[(nx, ny)] = 0.0  # la visito y no exploto: retroalimentacion

	def EjecutarAsign(self, palabras):
		match palabras:
			case [R, "=", Nh] if Nh.startswith("#"):
				self.Registros[self.RegIndex(R)] = self.ParseHex(Nh)
			case [R, "=", "sensor", M]:
				self.Registros[self.RegIndex(R)] = self.Sensor(M)
			case [R, "=", "detector", M]:
				self.Registros[self.RegIndex(R)] = self.Detector(M)
			case [R, "=", A, "+", B]:
				self.Registros[self.RegIndex(R)] = self.Valor(A) + self.Valor(B)
			case [R, "=", A, "-", B]:
				self.Registros[self.RegIndex(R)] = self.Valor(A) - self.Valor(B)

	def step(self):
		if self.Estado != "ready":
			return
		fetch = self.Instrucciones[self.RIP].split()
		match fetch:
			case ["izq" | "der" | "arriba" | "abajo"] as mov:
				self.Mover(mov[0])
				if self.Estado != "ready":
					return
			case ["Si", Re]:
				if self.Registros[self.RegIndex(Re)] != 1:
					self.RIP = self.Saltos[self.RIP]
			case ["FinSi"]:
				pass
			case ["ciclo", Re]:
				if self.Registros[self.RegIndex(Re)] != 1:
					self.RIP = self.Saltos[self.RIP]
			case ["Finciclo"]:
				self.RIP = self.Saltos[self.RIP] - 1
			case _:
				self.EjecutarAsign(fetch)

		self.RIP += 1
		if self.RIP >= len(self.Instrucciones):
			self.Estado = "done"

	def _construir_saltos(self, instrucciones):
		saltos = {}
		pila = []
		for i, ins in enumerate(instrucciones):
			palabras = ins.split()
			if not palabras:
				continue
			primera = palabras[0]
			if primera in ("Si", "ciclo"):
				pila.append((i, primera))
			elif primera in ("FinSi", "Finciclo"):
				if not pila:
					raise ValueError(f"{primera} sin apertura en linea {i}")
				j, tipo = pila.pop()
				esperado = "FinSi" if tipo == "Si" else "Finciclo"
				if primera != esperado:
					raise ValueError(f"Se esperaba {esperado} en linea {i}, hay {primera}")
				saltos[j] = i
				saltos[i] = j
		if pila:
			j, tipo = pila[-1]
			raise ValueError(f"{tipo} en linea {j} sin cerrar")
		return saltos

	# ------------------------------------------------------------------
	# Impresion
	# ------------------------------------------------------------------
	def ResumenPositivos(self):
		S = "\n===== Probabilidad de Bayes por detector positivo =====\n"
		if not self.Positivos:
			return S + "No hubo detecciones positivas\n"
		S += f"P(B|+) = P(+|B)·P(B) / [P(+|B)·P(B) + P(+|~B)·P(~B)]   con P(+|B)={self.Sens}, P(+|~B)={self.FP}\n"
		for (cx, cy), intento, antes, despues in self.Positivos:
			real = "BOMBA" if [cx, cy] in self.Bombas else "falso positivo"
			S += (f"Casilla {self.NumCasilla(cx, cy)} intento {intento}: "
				  f"P(B) {antes * 100:.2f}% -> P(B|+) {despues * 100:.2f}%  ({real})\n")
		return S

	def MapaCreencias(self):
		S = "\n===== Mapa de probabilidades P(B) (. = no evaluada, # = obstaculo) =====\n"
		for x, fila in enumerate(self.Mapa):
			celdas = []
			for y, v in enumerate(fila):
				if v == 1:
					celdas.append("  #  ")
				elif (x, y) in self.Creencias:
					celdas.append(f"{self.Creencias[(x, y)]:.3f}")
				else:
					celdas.append("  .  ")
			S += " ".join(celdas) + "\n"
		return S

	def __str__(self):
		S = " | ".join(f"R{i}:{v}" for i, v in enumerate(self.Registros)) + "\n"
		if self.Estado == "ready":
			S += f"Por ejecutar: {self.Instrucciones[self.RIP]}\n"
		CM = [[str(e) for e in fila] for fila in self.Mapa]
		for bx, by in self.Bombas:
			CM[bx][by] = "B"
		x, y = self.RBPos
		CM[x][y] = "*" if self.Estado == "boom" else "R"
		for fila in CM:
			S += " ".join(fila) + "\n"
		S += f"Estado {self.Estado}"
		return S

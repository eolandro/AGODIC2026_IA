# Cómo se mueve cada dirección en términos de (fila, columna) del mapa.
DIRECCIONES = {
	"arriba": (-1, 0),
	"abajo": (1, 0),
	"izq": (0, -1),
	"der": (0, 1),
}


class BoomeVirtualMachine:
	def __init__(self):
		self.Registros = [0, 0, 0, 0]
		self.Instrucciones = []   # aquí queda la lista anidada que llega de Boome.py
		self.RIP = None           # contador de instrucciones ejecutadas (solo informativo)
		# Mapa del terreno: 0 = celda libre, 1 = pared/obstáculo fijo.
		self.mapa = [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
			[0, 1, 0, 0, 0, 0, 0, 0, 1, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
		]
		self.RBPos = [0, 0]     # posición actual de Boome [fila, columna]
		self.BBPos = [3, 5]     # posición de la bomba (obstáculo especial)
		self.Estado = "wait"    # wait -> ready -> (done | dead)
		self.Flujo = None       # generador que va entregando instrucciones simples
		self.Actual = None      # instrucción que toca ejecutar en este momento

	# ---------- construcción del flujo de ejecución ----------

	def flujo(self, lineas):
		"""Generador recursivo: recorre la lista anidada y va entregando
		(yield), una por una, SOLO las instrucciones simples que hay que
		ejecutar de verdad (movimientos y asignaciones). Los bloques
		'Si'/'ciclo' se resuelven aquí mismo y nunca llegan a step():

		- 'Si': evalúa el registro UNA vez; si es distinto de 0, entrega
		  las líneas de adentro; si es 0, se las salta por completo.
		- 'ciclo': evalúa el registro antes de CADA vuelta; mientras sea
		  distinto de 0, vuelve a entregar las líneas de adentro.."""
		for elemento in lineas:
			if isinstance(elemento, list):
				match elemento:
					case ["Si", registro, sub, "FinSi"]:            # decode
						if self._valor_registro(registro) != 0:      # execute
							yield from self.flujo(sub)
					case ["ciclo", registro, sub, "finciclo"]:      # decode
						while self._valor_registro(registro) != 0:   # execute
							yield from self.flujo(sub)
			else:
				yield elemento

	def loadText(self, L):
		"""Recibe la lista anidada ya validada y prepara la máquina para
		empezar a ejecutar: crea el generador y adelanta la primera
		instrucción a self.Actual."""
		if not L:
			return
		if not self.Estado == 'wait':
			return
		self.Instrucciones = [
			a for a in L
		]
		self.Flujo = self.flujo(self.Instrucciones)
		self.Actual = next(self.Flujo, None)
		self.RIP = 0
		self.Estado = "ready" if self.Actual is not None else "done"

	def __str__(self):
		"""Representación en consola: registros, siguiente instrucción,
		mapa con la posición de Boome ('R') y de la bomba ('B'), y estado."""
		S = f'R0:{self.Registros[0]} |'
		S += f'R1:{self.Registros[1]} |'
		S += f'R2:{self.Registros[2]} |'
		S += f'R3:{self.Registros[3]} |'
		S += "\n"
		if self.Estado == "ready":
			S += f"Por ejecutar {self.Actual}"
		S += "\n"
		CM = [fila[::] for fila in self.mapa]
		if self.Estado in ["ready", "wait", "done", "dead"]:
			x, y = self.RBPos
			CM[x][y] = 'R'
		x, y = self.BBPos
		CM[x][y] = 'B'
		CM = [
			[str(e) for e in fila]
			for fila in CM
		]

		for fila in CM:
			S += ' '.join(fila)
			S += "\n"

		S += f"Estado {self.Estado}"
		return S

	# ---------- utilidades internas ----------

	def _indice_registro(self, R):
		"""'R0' -> 0, 'R1' -> 1, etc. Toma el segundo caracter del nombre."""
		return int(R[1])

	def _valor_registro(self, R):
		return self.Registros[self._indice_registro(R)]

	def _valor_numhex(self, texto):
		"""'#0001' -> 1 (convierte de texto hexadecimal a entero)."""
		return int(texto[1:], 16)

	def _resolver_operando(self, operando):
		"""Un operando de una operación puede ser un registro o un
		número hexadecimal; aquí se obtiene su valor numérico real."""
		if operando.startswith("#"):
			return self._valor_numhex(operando)
		return self._valor_registro(operando)

	def _dentro_del_mapa(self, x, y):
		return 0 <= x < len(self.mapa) and 0 <= y < len(self.mapa[0])

	def _hay_obstaculo(self, x, y):
		"""Regresa True si la celda (x, y) NO se puede pisar: porque
		está fuera del mapa, porque ahí está la bomba, o porque es
		una pared (valor 1 en self.mapa). La usan tanto los movimientos
		(para saber si Boome muere) como el sensor (para saber qué
		reportar)."""
		if not self._dentro_del_mapa(x, y):
			return True
		if [x, y] == self.BBPos:
			return True
		return self.mapa[x][y] == 1

	# ---------- ejecución de instrucciones simples ----------

	def _mover(self, dx, dy):
		"""Intenta mover a Boome. Si el destino es un obstáculo, muere
		(Estado = 'dead') y NO se actualiza su posición."""
		x, y = self.RBPos
		nx, ny = x + dx, y + dy
		if self._hay_obstaculo(nx, ny):
			self.Estado = "dead"
			return
		self.RBPos = [nx, ny]

	def _asignar_sensor(self, R, mov):
		"""'R = sensor mov': revisa la celda vecina en esa dirección y
		guarda 1 si hay obstáculo, 0 si está libre."""
		dx, dy = DIRECCIONES[mov]
		x, y = self.RBPos
		valor = 1 if self._hay_obstaculo(x + dx, y + dy) else 0
		self.Registros[self._indice_registro(R)] = valor

	def _asignar_valor(self, R, valor):
		"""'R = #hex': guarda un número hexadecimal directo en el registro."""
		self.Registros[self._indice_registro(R)] = valor

	def _asignar_operacion(self, R, A, operador, B):
		"""'R = A op B': resuelve A y B (registro o hex) y guarda el
		resultado de sumarlos o restarlos en el registro R."""
		a = self._resolver_operando(A)
		b = self._resolver_operando(B)
		resultado = a + b if operador == "+" else a - b
		self.Registros[self._indice_registro(R)] = resultado

	def step(self):
		"""Ejecuta UNA instrucción (self.Actual) y avanza al siguiente
		elemento del generador. Los bloques Si/ciclo NUNCA llegan aquí"""
		if self.Estado != "ready":
			return

		fetch = [ins for ins in self.Actual.split(" ") if ins]

		match fetch:
			case ['izq']:
				self._mover(*DIRECCIONES["izq"])
			case ['der']:
				self._mover(*DIRECCIONES["der"])
			case ['arriba']:
				self._mover(*DIRECCIONES["arriba"])
			case ['abajo']:
				self._mover(*DIRECCIONES["abajo"])

			case [R, '=', 'sensor', mov]:
				self._asignar_sensor(R, mov)

			case [R, '=', A, operador, B]:
				self._asignar_operacion(R, A, operador, B)

			case [R, '=', valor]:
				self._asignar_valor(R, self._valor_numhex(valor))
		if self.Estado != "ready":
			return

		self.RIP += 1
		self.Actual = next(self.Flujo, None)
		if self.Actual is None:
			self.Estado = "done"
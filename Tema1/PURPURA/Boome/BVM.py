class BommeVirtualMachine:
	def __init__(self):
		################R0,R1,R2,R3
		self.Registros =[0,0,0,0]
		self.Instrucciones=[]
		self.RIP=None
		################
		self.Mapa=[
			[0,0,0,0,0,0,0,0,0,0],
			[0,1,0,0,0,0,0,0,1,0],
			[0,0,1,0,0,0,0,1,0,0],
			[0,0,1,0,0,0,0,1,0,0],
			[0,1,0,0,0,0,0,0,1,0],
			[0,0,0,0,0,0,0,0,0,0]
		]		
		self.RBPos= [0,0] #posicion de boome en el mapa
		self.BBPos= [3,5] #posicion bomba
		self.Estado="wait"
		self.Saltos = {}  
	def LoadText(self,L):
		if not L:
			return 
		self.Instrucciones =[
			a for a in L
		]
		self.Saltos = self._construir_saltos(self.Instrucciones)
		self.Estado="ready"
		self.RIP=0
		
	def __str__(self):
		S=f'R0:{self.Registros[0]} |'
		S+=f'R1:{self.Registros[1]} |'
		S+=f'R2:{self.Registros[2]} |'
		S+=f'R3:{self.Registros[3]} |'
		S+="\n"
		if self.Estado=="ready":
			S+=f"Por ejecutar {self.Instrucciones[self.RIP]}"	
		S+="\n"
		CM =[fila[::] for fila in self.Mapa]
		if self.Estado in ["ready","wait","done"]:	
			x,y=self.RBPos
			CM[x][y]='R'
		x,y=self.BBPos
		CM[x][y]='B'
		CM=[
			[str(e) for e in fila]
			for fila in CM
		]
		for fila in CM:
			S += ' '.join(fila)
			S += "\n"
		S += f"Estado {self.Estado}"
		return S 
	def step(self):
		if self.Estado != "ready":
			return
		fetch=self.Instrucciones[self.RIP]
		fecth=fetch.split(" ")
		fecth=[ins for ins in fetch if ins]
		match fetch:
			case ['izq']: #decode
				self.RBPos[1]-= 1 #execute
				if self.RBPos[1]<0:
					self.Estado="dead"
					return
			case ['der']:  #decode
				self.RBPos[1]+=1#execute
				X,_=self.RBPos
				if self.RBPos[1]>=len(self.Mapa[x]):
					self.Estado="dead"
		self.RIP += 1
		if self.RIP >= len(self.Instrucciones):
			self.Estado="done"
	def ParseHex(self, cadena):
		if len(cadena) != 5 or not cadena.startswith("#"):
			raise ValueError(f"Hex inválido: {cadena}")
		return int(cadena[1:], 16)
		
	def RegIndex(self,R):
		return int(R[1])
 
 
	def Valor(self,token):
		if token.startswith("R"):
			return self.Registros[self.RegIndex(token)]
		return self.ParseHex(token)
 
	DIRECCIONES={
		"arriba":(-1,0),
		"abajo":(1,0),
		"izq":(0,-1),
		"der":(0,1),
	}
 
	def Sensor(self,direccion):
		dx,dy=self.DIRECCIONES[direccion]
		x,y=self.RBPos
		nx,ny=x+dx,y+dy
		if nx<0 or nx>=len(self.Mapa) or ny<0 or ny>=len(self.Mapa[0]):
			return 1  #### fuera del mapa cuenta como obstaculo
		return self.Mapa[nx][ny]
 
	def Mover(self,direccion):
		dx,dy=self.DIRECCIONES[direccion]
		x,y=self.RBPos
		nx,ny=x+dx,y+dy
		if nx<0 or nx>=len(self.Mapa) or ny<0 or ny>=len(self.Mapa[0]):
			self.Estado="dead"
			return
		if self.Mapa[nx][ny]==1:
			self.Estado="dead"
			return
		self.RBPos=[nx,ny]
		if self.RBPos==self.BBPos:
			self.Estado="boom"
 
	def EjecutarAsign(self,palabras):
		match palabras:
			case [R,"=",Nh] if Nh.startswith("#"):
				self.Registros[self.RegIndex(R)]=self.ParseHex(Nh)
			case [R,"=","sensor",M]:
				self.Registros[self.RegIndex(R)]=self.Sensor(M)
			case [R,"=",A,"+",B]:
				self.Registros[self.RegIndex(R)]=self.Valor(A)+self.Valor(B)
			case [R,"=",A,"-",B]:
				self.Registros[self.RegIndex(R)]=self.Valor(A)-self.Valor(B)
 
	def step(self):
		if self.Estado != "ready":
			return
		fetch=self.Instrucciones[self.RIP]
		fecth=fetch.split(" ")
		fecth=[ins for ins in fecth if ins]
		match fecth:
			case ["izq"|"der"|"arriba"|"abajo"] as mov:
				self.Mover(mov[0])
				if self.Estado != "ready":
					return
 
			case ["Si",Re]:
				if self.Registros[self.RegIndex(Re)] != 1:
					self.RIP=self.Saltos[self.RIP] 
 
			case ["FinSi"]:
				pass 
 
			case ["ciclo",Re]:
				if self.Registros[self.RegIndex(Re)] != 1:
					self.RIP=self.Saltos[self.RIP] 
 
			case ["Finciclo"]:
				self.RIP=self.Saltos[self.RIP]-1 
 
			case _:
				self.EjecutarAsign(fecth)
 
		self.RIP += 1
		if self.RIP >= len(self.Instrucciones):
			self.Estado="done"
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
					raise ValueError(f"{primera} sin apertura en línea {i}")
				j, tipo = pila.pop()
				esperado = "FinSi" if tipo == "Si" else "Finciclo"
				if primera != esperado:
					raise ValueError(f"Se esperaba {esperado} en línea {i}, hay {primera}")
				saltos[j] = i
				saltos[i] = j
		if pila:
			j, tipo = pila[-1]
			raise ValueError(f"{tipo} en línea {j} sin cerrar")
		return saltos 				
					
		
		
		

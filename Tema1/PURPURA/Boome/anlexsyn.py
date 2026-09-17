def uhex(cadena_hex):
	if len(cadena_hex) != 1:
		return (False,"Longitud Incorrecta")
	if cadena_hex.isdigit():
		return (True,)		
	if cadena_hex in ["A","B","C","D","E","F"]:
		return (True,)
	return (False,"No Valido")
def numhex(valor):
	match valor:
		case str():
			return numhex(list(valor))
		case ["#",A,B,C,D]:
			R = [uhex(A),uhex(B),uhex(C),uhex(D)]
			#[(True,),(True,),(True,),(True,)]
			"""
			Valido=False
			for e in R:
				if e[0]==False:
					Valido=False
			
"""
			R=[e for e in R if not e[0]]
			if not R:
				return (True,)
			return (False,R)
		case _:
			return (False,f"Error desconocido en numhex: {valor}")
def regs(valor):
	if valor in ["R0","R1","R2","R3"]:
		return (True,)
	return (False,f"{valor} No es un registro valido")
	
def opmat(valor):
	if valor in ["+","-"]:
		return (True,)
	return (False,f"{valor} No es un operador valido")

def movs(valor):
	if valor in ["arriba","abajo","izq","der"]:
		return (True,)
	return (False,f"{valor} No es un movimiento valido")
def opera(lista):
	match lista:
		case[A,B,C]:
			Oper=opmat(B)
			if len(Oper)!=1:
				return (False,[f"{lista} usa {Oper} y no es valido",Oper])
			###opera(A,B,C) :- regs(A),opmat(B),regs(C).
			R=[regs(A),regs(C)]
			N=[len(e) for e in R]
			match N:
				case[1,1]:
					return (True,)
			###opera(A,B,C) :- regs(A),opmat(B),numhex(C).
			R=[regs(A),numhex(C)]
			N=[len(e) for e in R]
			match N:
				case[1,1]:
					return (True,)
			###opera(A,B,C) :- numhex(A),opmat(B),regs(C).
			R=[numhex(A),regs(C)]
			N=[len(e) for e in R]
			match N:
				case[1,1]:
					return (True,)
			###opera(A,B,C) :- numhex(A),opmat(B),numhex(C).
			R=[numhex(A),numhex(C)]
			N=[len(e) for e in R]
			match N:
				case[1,1]:
					return (True,)
			return (False,[f"{lista}no es una operacion valida"])
def asign(valor):
	match valor:
		case str():
			return asign([e for e in valor.split(' ') if e])
		case [R,"=",Nh] if Nh.startswith("#"):
			RG=regs(R); N=numhex(Nh)
			if len(RG)!=1: return (False,[f"{valor} tiene un registro no valido",RG])
			if len(N)!=1: return (False,[f"{valor} tiene un hex no valido",N])
			return (True,)
		case [R,"=","sensor",M]:
			RG=regs(R); Mv=movs(M)
			if len(RG)!=1: return (False,[f"{valor} tiene un registro no valido",RG])
			if len(Mv)!=1: return (False,[f"{valor} tiene un movimiento no valido",Mv])
			return (True,)
		case [R,"=",A,o,B]:
			RG=regs(R)
			if len(RG) != 1:
				return (False,[f"{valor} tiene un registro no valido",RG])
			Res=opera([A,o,B])
			if len(Res)==1:
				return (True,)
			return (False,Res)
		case _:
			return (False,f"Error desconocido en asign: {valor}")
			
def linea(valor):
	match valor:
		case str():
			palabras=[e for e in valor.split(' ') if e]
			if len(palabras)==1:
				if palabras[0] in ["FinSi","Finciclo"]:
					return (True,)
				M=movs(palabras[0])
				if len(M)==1:
					return (True,)
				return (False,[f"{valor} no es una linea valida",M])
			if len(palabras)==2 and palabras[0] in ["Si","ciclo"]:
				RG=regs(palabras[1])
				if len(RG)==1:
					return (True,)
				return (False,[f"{valor} no es una linea valida",RG])
			A=asign(palabras)
			if len(A)==1:
				return (True,)
			return (False,[f"{valor} no es una linea valida",A])
		case _:
			return (False,f"Error desconocido en linea: {valor}")
 
### lineas([L]) :- linea(L).
### lineas([P|R]) :- linea(P), lineas(R).
def lineas(lista):
	match lista:
		case [L]:
			Res=linea(L)
			if len(Res)==1:
				return (True,)
			return (False,[f"{lista} no es valido",Res])
		case [P,*R]:
			Rp=linea(P)
			if len(Rp)!=1:
				return (False,[f"{P} no es una linea valida",Rp])
			return lineas(R)
		case _:
			return (False,f"{lista} no es una lista de lineas valida")
 
 
### condicional("Si",Re,[F|R],"FinSi") :- regs(Re), lineas([F|R]).
def condicional(lista):
	match lista:
		case ["Si",Re,cuerpo,"FinSi"]:
			RG=regs(Re)
			if len(RG)!=1:
				return (False,[f"{Re} no es un registro valido",RG])
			L=lineas(cuerpo)
			if len(L)!=1:
				return (False,[f"{cuerpo} no es un cuerpo valido",L])
			return (True,)
		case _:
			return (False,f"{lista} no es un condicional valido")
 
 
### ciclos("ciclo",Re,[F|R],"Finciclo") :- regs(Re), lineas([F|R]).
def ciclos(lista):
	match lista:
		case ["ciclo",Re,cuerpo,"Finciclo"]:
			RG=regs(Re)
			if len(RG)!=1:
				return (False,[f"{Re} no es un registro valido",RG])
			L=lineas(cuerpo)
			if len(L)!=1:
				return (False,[f"{cuerpo} no es un cuerpo valido",L])
			return (True,)
		case _:
			return (False,f"{lista} no es un ciclo valido")
 

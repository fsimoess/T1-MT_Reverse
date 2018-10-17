import os
import sys

def entrada_valida(enter, alfabeto):
	for word in enter:
		exists = False
		for contain in alfabeto:
			if contain == word:
				exists = True
		if not exists:
			print('Entrada inválida, encerrando aplicação.')
			exit()

def structure_list(var, list):
	organized_list = ''
	cont=0
	for i in var:
		if cont%2==1:
			if (i != "=") and (cont!=1) and (cont!=11):
				organized_list = organized_list + var[cont] + " "
		cont=cont+1
	entrada_valida(organized_list, list)

def verifica_transicao(alfabeto, transicao):
	alfabeto = alfabeto + " D" + " E" + " /"
	for x in transicao:
		structure_list(x, alfabeto)

class Fita(object):
	def __init__(self, entrada):
		self.fita = entrada + "B"
		self.head = 0

	def read_fita(self):
		return self.fita[self.head]

	def write_fita(self, aux):
		self.fita = self.fita[:self.head] + aux + self.fita[self.head + 1:]

	def move_left(self):
		if self.head == 0:
			return
		if self.head == len(self.fita)-1 or self.fita[self.head] == "B":
			self.fita = self.fita[:self.head-1] + "B"
		self.head = self.head - 1

	def move_right(self):
		self.head = self.head + 1
		if self.head == len(self.fita):
			self.fita = self.fita + "B"

	def write_history(self, aux, dir):
		if dir == "x" or dir == "D":
			self.fita = self.fita[:self.head] + aux + self.fita[self.head + 1:]
		if dir == "D" or dir == "x":
			self.move_right()
		if dir == "E" or dir == "0":
			self.move_left()

class Maquina_Turing(object):
	def __init__(self, entrada):
		self.fita1 = Fita(entrada)
		self.fita2 = Fita("")
		self.fita3 = Fita("")

def MT_revert(newState, _f1, _f2, _f3, oldState, f1, f2, f3):

	if f1 == "/" and _f1 == "D":
		_f1 = f1
		f1 = "E"
	if f1 == "/" and _f1 == "E":
		_f1 = f1
		f1 = "D"
	if f2 == "/" and _f2 == "D":
		_f2 = f2
		f2 = "E"
	if f2 == "/" and _f2 == "E":
		_f2 = f2
		f2 = "D"
	if f3 == "/" and _f3 == "D":
		_f3 = f3
		f3 = "E"
	if f3 == "/" and _f3 == "E":
		_f1 = f1
		f1 = "D"

	transitions = "(" + newState + "," + _f1 + "," + _f2 + "," + _f3 + ")=(" + oldState + "," + f1 + "," + f2 + "," + f3 + ")"
	return transitions

def control(str1, oldState, fita, mode, str2, maquina):
	if mode == "Move":
		#print('Movimento na fita', fita)
		if str2 == "D" and fita==1:
			maquina.fita1.move_right()
			maquina.fita2.write_history(oldState, str2)
		if str2 == "E" and fita==1:
			maquina.fita1.move_left()
			maquina.fita2.write_history(oldState, str2)
		if str2 == "D" and fita==2:
			maquina.fita2.write_history(oldState, str2)
		if str2 == "E" and fita==2:
			maquina.fita2.write_history(oldState, str2)
			print('oi',maquina.fita2.head)
		if str2 == "D" and fita==3:
			maquina.fita3.move_right()
			maquina.fita2.write_history(oldState, str2)
		if str2 == "E" and fita==3:
			maquina.fita3.move_left()
			maquina.fita2.write_history(oldState, str2)
	if mode == "RW":
		#print('Leitura e Escrita na fita', fita)
		maquina.fita1.write_fita(str2)
		maquina.fita2.write_history(oldState, str2)

def transitions_MT(var, maquina, transitions_revert, palavra, passo):
	oldState = var[1]
	f1 = var[3]
	f2 = var[5]
	f3 = var[7]
	newState = var[11]
	_f1 = var[13]
	_f2 = var[15]
	_f3 = var[17]
	aux = False
	cont = 0

	if f1 == "/":
		control(f1, oldState, 1, "Move", _f1, maquina)
		passo-=1

	if f1 != "/":
		for x in palavra:
			if cont == passo:
				break
			if x == f1:
				aux = True
			elif x != "B":
				print("Automato em looping! Não existe parte da palavra na transição", var)
				print("Saindo do programa!")
				exit()

		control(f1, oldState, 1, "RW", _f1, maquina)

	transitions_revert.append(MT_revert(newState,_f1,_f2,_f3,oldState,f1,f2,f3))

def main(args):

	print('\nImplementação de uma MT Reversível com multifita (3 fitas)\n\n')

	entrada = list()
	states = list()
	alfabeto_fita = list()
	transitions = list()
	transitions_revert = list()
	enter_fita = list()
	exit_fita = list()

	for x in open(args[1], "r"):
		entrada.append(x[:-1])

	end = len(entrada)
	states = entrada[1]
	symbols = entrada[2]
	alfabeto_fita = entrada[3]
	transitions = entrada[4:-1]
	enter_fita = entrada[end-1]

	entrada_valida(enter_fita, symbols) #Verifica se a entrada é válida pro alfabeto de entrada
	entrada_valida(symbols, alfabeto_fita) #Verifica se o alfabeto de entrada é válido pro alfabeto da fita
	verifica_transicao(alfabeto_fita, transitions) #Verifica se o alfabeto da fita está contido nas transições

	print('______________________________________')
	print('Todos os dados são válidos!')
	print('Palavra de Entrada: ', enter_fita)
	print('Alfabeto de entrada:', symbols)
	print('Alfabeto da fita: ', alfabeto_fita)

	print('______________________________________')
	print('Dados das Fitas: ')
	maquina = Maquina_Turing(enter_fita)
	print('Estado inicial da Fita 1: ',maquina.fita1.fita)
	print('Estado inicial da Fita 2: ',maquina.fita2.fita)
	print('Estado inicial da Fita 3: ',maquina.fita3.fita)
	print('______________________________________')

	cont=0
	for x in transitions:
		cont+=1
		transitions_MT(x, maquina, transitions_revert, enter_fita, cont)

	transitions_revert.reverse()
	transitions = list()

	print('Primeiro passo da MT Reversível:')
	print('Estado atual da Fita 1: ',maquina.fita1.fita)
	print('Estado atual da Fita 2: ',maquina.fita2.fita)
	print('Estado atual da Fita 3: ',maquina.fita3.fita)
	print('______________________________________')
	
	exit_fita = maquina.fita1.fita
	maquina.fita3.fita = exit_fita

	print('Cópia da saída, segundo passo da MT Reversível:')
	print('Estado atual da Fita 1: ',maquina.fita1.fita)
	print('Estado atual da Fita 2: ',maquina.fita2.fita)
	print('Estado atual da Fita 3: ',maquina.fita3.fita)
	print('______________________________________')

	cont=0
	for x in transitions_revert:
		cont+=1
		transitions_MT(x, maquina, transitions, exit_fita, cont)

	print('Reversão da saída, terceiro passo da MT Reversível:')
	print('Estado atual da Fita 1: ',maquina.fita1.fita)
	print('Estado atual da Fita 2: ',maquina.fita2.fita)
	print('Estado atual da Fita 3: ',maquina.fita3.fita)
	print('______________________________________')

	#Salvar a nova entrada na fita 3

if __name__ == "__main__": sys.exit(main(sys.argv))
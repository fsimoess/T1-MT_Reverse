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

	def write_fite(self, aux):
		self.fita = self.fita[:self.head] + aux + self.fita[self.head + 1:]

	def move_left(self):
		if self.head == 0:
			return
		if self.fita[self.head] == 'B' and self.fita[self.head + 1] == 'B' and self.head + 2 == len(self.fita):
			self.fita = self.fita[:self.head+1]
		self.head = self.head - 1

	def move_right(self):
		self.head = self.head + 1
		if self.head == len(self.fita):
			self.fita = self.fita + "B"

class Maquina_Turing(object):
	def __init__(self, entrada):
		self.fita1 = Fita(entrada)
		self.fita2 = Fita("")
		self.fita3 = Fita("")

	def print_fita(self):
		print(self.fita1)

def control(str1, fita, mode, str2, maquina):
	if mode == "Move":
		print('Movimento na fita', fita)
		if str2 == "D" and fita==1:
			maquina.fita1.move_right()
		if str2 == "E" and fita==1:
			maquina.fita1.move_left()
		if str2 == "D" and fita==2:
			maquina.fita2.move_right()
		if str2 == "E" and fita==2:
			maquina.fita2.move_left()
		if str2 == "D" and fita==3:
			maquina.fita3.move_right()
		if str2 == "E" and fita==3:
			maquina.fita3.move_left()
	if mode == "RW":
		print('Leitura e Escrita na fita', fita)
		if str1 != "B":
			maquina.fita2.write_fite(maquina.fita1.read_fita())
			maquina.fita1.write_fite("x")

def transitions_MT(var, maquina):
	oldState = var[1]
	f1 = var[3]
	f2 = var[5]
	f3 = var[7]
	newState = var[11]
	_f1 = var[13]
	_f2 = var[15]
	_f3 = var[17]

	if f1 == "/":
		control(f1, 1, "Move", _f1, maquina)
	if f1 != "/":
		control(f1, 1, "RW", _f1, maquina)
	if f2 == "/":
		control(f2, 2, "Move", _f2, maquina)
	if f2 != "/":
		control(f2, 2, "RW", _f2, maquina)
	if f3 == "/":
		control(f3, 3, "Move", _f3, maquina)
	if f3 != "/":
		control(f3, 3, "RW", _f3, maquina)

def main(args):

	print('\nImplementação de uma MT Reversível com multifita (3 fitas)\n\n')

	entrada = list()
	states = list()
	alfabeto_fita = list()
	transitions = list()
	enter_fita = list()

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
	print(maquina.fita1.fita)
	print(maquina.fita2.fita)
	print(maquina.fita3.fita)

	print('______________________________________')
	print('Transições: ')
	for x in transitions:
		print(x)
		transitions_MT(x, maquina)
		print('Estado atual da Fita 1: ',maquina.fita1.fita)
		print('Estado atual da Fita 2: ',maquina.fita2.fita)
		print('Estado atual da Fita 1: ',maquina.fita3.fita)
		print('______________________________________')

if __name__ == "__main__": sys.exit(main(sys.argv))
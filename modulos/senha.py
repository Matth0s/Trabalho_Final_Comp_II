from .excecoes import *

import string
import random

class Senha():
	"""
	Classe que representa uma senha dentro do programa.
	"""
	tipos_codigos = [
		0b0001, # Minusculos
		0b0010, # Maiusculos
		0b0100, # Numericos
		0b1000  # Especiais
	]

	def __init__(self, nome, username="", URL="", tipo=0b0001, tamanho=1):
		self.setNome(nome)
		self.setUsername(username)
		self.setURL(URL)
		self.setTipo(tipo)
		self.setTamanho(tamanho)
		self.__senha = ""
		self.setSenha()

	def getNome(self):
		return self.__nome

	def setNome(self, nome):
		nome = str(nome)
		if nome == "":
			raise NomeNuloError("A senha precisa ter um identificador")
		self.__nome = nome

	def getUsername(self):
		return self.__username

	def setUsername(self, username):
		username = str(username)
		self.__username = username

	def getURL(self):
		return self.__URL

	def setURL(self, URL):
		URL = str(URL)
		self.__URL = URL

	def getTipo(self):
		return self.__tipo

	def setTipo(self, tipo):
		tipo = int(tipo)
		if tipo >= 0b10000 or tipo < 0b0000:
			raise ValueError("O tipo de senha precisa ser um codigo de identificação valido!")
		if tipo == 0b0000:
			raise SemTipoDeCaractereError("A senha precisa ter pelo menos um tipo de caractere!")
		self.__tipo = tipo

	def getTamanho(self):
		return self.__tamanho

	def setTamanho(self, tamanho):
		tamanhoMin = sum((self.__tipo & t_cod) != 0 for t_cod in self.tipos_codigos)
		if tamanho == "" or int(tamanho) < tamanhoMin:
			raise TamanhoInvalidoError(f"Tamanho precisa comportar os tipos selecionados (> {tamanhoMin})!")
		tamanho = int(tamanho)
		self.__tamanho = tamanho

	def getSenha(self):
		return self.__senha

	def setSenha(self):
		"""
		Gera senhas fortes de acordo com o tipo de senha definido.
		"""
		senha = ""
		caracteres_possiveis = ""

		tipos_caracteres = [
			string.ascii_lowercase, # Minusculos -> string do tipo "abcdef..."
			string.ascii_uppercase, # Maiusculos -> string do tipo "ABCDEF..."
			string.digits, # Numericos -> string do tipo "012345..."
			string.punctuation # Especiais -> string do tipo "!#$%&'..."
		]

		# Varre todos os codigos de tipo e todas as strings do tipo para escolher
		# os caracteres que serão utilizados para criar a senha corretametne
		for t_cod, t_char in zip(self.tipos_codigos, tipos_caracteres):
			if (self.__tipo & t_cod) != 0:
				# Poe todos os caracteres daquele tipo como possiveis opções para
				# serem escolhidas para a senha
				caracteres_possiveis += t_char

				# Garante que pelo menos 1 caracter daquele tipo vai estar na senha
				senha += random.choice(t_char)

		# Completa o restante de caracteres que faltam para que a senha tenha o
		# numero de caracteres igual a self.__tamanho
		for _ in range(self.__tamanho - len(senha)):
			senha += random.choice(caracteres_possiveis)

		# pega a senha gerada e tranforma em uma lista de caracteres embaralhada
		# Ex: abcd123 --> ['d', '2', 'b', 'a', 3, 1, 'c']
		embaralhar_senha = random.sample(senha, len(senha))

		# junta a lista embaralhada em str de novo
		# Ex: ['d', '2', 'b', 'a', 3, 1, 'c'] --> d2ba31c
		self.__senha =  "".join(embaralhar_senha)


__all__ = ["Senha"]

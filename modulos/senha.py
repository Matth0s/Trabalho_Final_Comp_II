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
			string.ascii_lowercase, # Minusculos
			string.ascii_uppercase, # Maiusculos
			string.digits, # Numericos
			string.punctuation # Especiais
		]

		for t_cod, t_char in zip(self.tipos_codigos, tipos_caracteres):
			if (self.__tipo & t_cod) != 0:
				caracteres_possiveis += t_char
				senha += random.choice(t_char)

		for _ in range(self.__tamanho - len(senha)):
			senha += random.choice(caracteres_possiveis)

		embaralhar_senha = random.sample(senha, len(senha))
		self.__senha =  "".join(embaralhar_senha)

	def __str__(self):
		string = '/' + '¨' * 20 + '\n'
		string += '| ' + str(self.__nome) + '\n'
		string += '| ' + str(self.__username) + '\n'
		string += '| ' + str(self.__URL) + '\n'
		string += '| ' + str(self.__tamanho) + '\n'
		string += '| ' + str(self.__tipo) + '\n'
		string += '| ' + str(self.__senha) + '\n'
		string += ' ' + '_' * 20
		return string


__all__ = ["Senha"]

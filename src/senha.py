import string
import random

class Senha():
	"""
	Classe que representa uma senha dentro do programa.
	"""

	def __init__(self, nome, URL, username, tipo, tamanho):
		self.__nome = nome
		self.__username = username
		self.__URL = URL
		self.__tipo = tipo
		self.__tamanho = tamanho
		self.__senha = ""

	def gerar_senha(self):
		"""
		Gera senhas fortes de acordo com o tipo de senha definido.
		"""

		caracteres_possiveis = ""

		if (self.__tipo & 0b0001) != 0: # Maiusculos
			caracteres_possiveis += string.ascii_uppercase

		if (self.__tipo & 0b0010) != 0: # Minusculos
			caracteres_possiveis += string.ascii_lowercase

		if (self.__tipo & 0b0100) != 0: # Numericos
			caracteres_possiveis += string.digits

		if (self.__tipo & 0b1000) != 0: # Especiais
			caracteres_possiveis += string.punctuation

		self.__senha =  ""
		for _ in range(self.__tamanho):
			self.__senha += random.choice(caracteres_possiveis)

	# def getNome(self):
	# 	return

	# def setNome(self, nome):
	# 	return

	# def getSenha(self):
	# 	return

	# def setSenha(self, senha):
	# 	return

	# def getTipo(self):
	# 	return

	# def getTamanho(self):
	# 	return

	# def __str__(self):
	# 	exibir = f""
	# 	exibir += f" _____________________________\n"
	# 	exibir += f"| Identificação : {self.__nome}\n"
	# 	exibir += f"| Senha         : {self.__senha}\n"
	# 	exibir += f" ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n"
	# 	return exibir

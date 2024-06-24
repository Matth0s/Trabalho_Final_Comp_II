import numpy as np

class Perfil():
	"""
	Classe responsavel por armazenar e manipular as senhas e dados do usuario.
	"""

	def __init__(self, nome, chave):
		self.__nome = nome
		self.__chave = chave
		# self.__senhas = np.array([])

	def getNome(self):
		return self.__nome

	def setNome(self, nome):
		self.__nome = nome

	def getChave(self):
		return self.__chave

	def setChave(self, chave):
		self.__chave = chave

	# def addSenha(self, senha):
	# 	return

	# def rmSenha(self, senha):
	# 	return

	# def getSenhaByNome(self, nome):
	# 	return

	# def mostrarSenhas(self):
	# 	return

	# def __str__(self):
	# 	exibir = ""
	# 	exibir += f"+-----------------------------\n"
	# 	exibir += f"| Nome   : {self.__nome}\n"
	# 	exibir += f"| Senhas : {len(self.__senhas)}\n"
	# 	exibir += f"+-----------------------------\n"
	# 	return exibir

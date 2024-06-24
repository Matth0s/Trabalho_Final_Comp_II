import numpy as np

class Perfil():
	"""
	Classe responsavel por armazenar e manipular as senhas e dados do usuario.
	"""

	def __init__(self, nome, chave):
		self.__nome = nome
		self.chave = chave
		self.__senhas = np.array([])

	def getNome(self):
		return self.__nome

	def setNome(self, nome):
		return

	def addSenha(self, senha):
		return

	def rmSenha(self, senha):
		return

	def getSenhaByNome(self, nome):
		return

	def mostrarSenhas(self):
		return

	def __str__(self):
		exibir = ""
		exibir += f"+-----------------------------\n"
		exibir += f"| Nome   : {self.__nome}\n"
		exibir += f"| Senhas : {len(self.__senhas)}\n"
		exibir += f"+-----------------------------\n"
		return exibir

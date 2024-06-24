class Senha():
	"""
	Classe que representa uma senha dentro do programa.
	"""

	def __init__(self, nome, URL, username, senha, tipo, tamanho):
		self.__nome = nome
		self.__URL = URL
		self.__username = username
		self.__senha = senha
		self.__tipo = tipo
		self.__tamanho = tamanho

	def getNome(self):
		return

	def setNome(self, nome):
		return

	def getSenha(self):
		return

	def setSenha(self, senha):
		return

	def getTipo(self):
		return

	def getTamanho(self):
		return

	def __str__(self):
		exibir = f""
		exibir += f" _____________________________\n"
		exibir += f"| Identificação : {self.__nome}\n"
		exibir += f"| Senha         : {self.__senha}\n"
		exibir += f" ¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n"
		return exibir

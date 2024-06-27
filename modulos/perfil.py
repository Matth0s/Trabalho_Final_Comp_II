from .excecoes import *
from .senha import Senha
from cryptography.fernet import Fernet

import numpy as np
import pickle

class Perfil():
	"""
	Classe responsavel por armazenar e manipular as senhas e dados do usuario.
	"""

	def __init__(self, nome, chave):
		self.__nome = nome
		self.__chave = chave
		self.__senhas = np.array([])

	def getNome(self):
		return self.__nome

	def setNome(self, nome):
		self.__nome = nome

	def getChave(self):
		return self.__chave

	def setChave(self, chave):
		self.__chave = chave

	def getSenhas(self):
		getNomes = np.vectorize(lambda e: e.getNome(), otypes=[str])
		return getNomes(self.__senhas)

	def addSenha(self, senha):
		self.__senhas = np.append(self.__senhas, senha)

	def salvar(self):
		"""
		Salva todas as informações do Perfil logado no programa.
		"""

		try:
			with open(f"./perfis/{self.__nome}.pkl", "wb") as arquivo:
				obj_serializado = pickle.dumps(self)
				obj_criptografado = Fernet(self.__chave).encrypt(obj_serializado)
				arquivo.write(obj_criptografado)
		except Exception as e:
			print(f"Erro ao tentar salvar o Perfil {self.__nome}: {e}")

	# def rmSenhaByName(self, senha):
	# 	pass
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

# p = Perfil("Teste", "Chave")

# for i in range(10):
# 	p.addSenha(Senha(f"senha {i}"))

# print(p.getSenhas())
# new_arr = np.insert(arr, index, element)

__all__ = ["PErfil"]

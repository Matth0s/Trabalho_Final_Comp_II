from .excecoes import *
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

	def addSenha(self, senha):
		idx = np.searchsorted(np.char.lower(self.getNomesSenhas()), senha.getNome().lower())
		self.__senhas = np.insert(self.__senhas, idx, senha)

	def getSenhaByIdx(self, idx):
		return self.__senhas[idx]

	def removeSenhaByIdx(self, idx):
		self.__senhas = np.delete(self.__senhas, idx)

	def getNomesSenhas(self):
		getNomes = np.vectorize(lambda e: e.getNome(), otypes=[str])
		return getNomes(self.__senhas)

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


__all__ = ["Perfil"]

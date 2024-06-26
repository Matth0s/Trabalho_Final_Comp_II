from src.perfil import Perfil
from src.excecoes import PerfilJaExisteError
from src.excecoes import ChavesDiferentes

import os
import base64
import pickle

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

def gerar_chave_mestra(nome_perfil, palavra_chave):
	"""
	Gera uma chave ,a partir de uma combinação do nome do perfil e da palavra chave,
	que será utilizada para a criptografia e descriptografia das senhas atravez
	da criptografia com Fernet

	Parametros:
		nome_perfil: str  -> nome do perfil logado no programa
		palavra_chave: str  -> senha que será utilizada para gerar a chave

	Retorno:
		Fernet.key() -> uma chave gerada usando o PBKDF2HMAC
	"""
	nucleo = nome_perfil + palavra_chave
	n = len(nucleo).to_bytes(8, 'big')
	kdf = PBKDF2HMAC(hashes.SHA256(), 32, n, 100000, default_backend())
	chave = base64.urlsafe_b64encode(kdf.derive(nucleo.encode()))

	return chave

def salvar_perfil(perfil):
	"""
	Salva todas as informações do Perfil logado no programa.

	Parametros:
		perfil: Perfil  -> objeto Perfil logado no programa.
	"""

	try:

		f = Fernet(perfil.getChave())

		with open(f"./perfis/{perfil.getNome()}.pkl", "wb") as arquivo:
			obj_serializado = pickle.dumps(perfil)
			obj_criptografado = f.encrypt(obj_serializado)
			arquivo.write(obj_criptografado)

	except Exception as e:
		print(f"Erro ao tentar salvar o Perfil {perfil.getNome()}: {e}")

def criar_perfil(nome, chave_mestra, chave_repetida):
	"""
	Cria um perfil novo utilizando os parametros passados e realizando as
	verificações necessarias

	Parametros:
		nome: str -> nome do perfil que se deseja carregar.
		chave_mestra: str -> chave_mestra utilizada para a validação do usuario.
		chave_repetida: str -> garantia de que o usuario digitou realmente a
		chave_mestra que desejava.

	Retorno:
		Perfil | None -> retorna o Perfil criado em caso de sucesso e None
		em caso de fracasso.

	Raise:
		PerfilJaExisteError -> será lançado caso o nome de perfil já esteja
		sendo utilizado por outro usuario.

		ChavesDiferentes -> será lançado caso o usuario tenha passado as
		chave_mestra e chave de confirmação diferentes.
	"""
	if os.path.exists(f"./perfis/{nome}.pkl"):
		raise PerfilJaExisteError(f"O nome de perfil '{nome}' já esta sendo utilizado!")

	if chave_mestra != chave_repetida:
		raise ChavesDiferentes("As chaves mestras não são iguais!")

	if not os.path.exists("./perfis"):
		os.mkdir("./perfis")

	perfil = Perfil(nome, gerar_chave_mestra(nome, chave_mestra))

	f = Fernet(perfil.getChave())

	with open(f"./perfis/{perfil.getNome()}.pkl", "wb") as arquivo:
		obj_serializado = pickle.dumps(perfil)
		obj_criptografado = f.encrypt(obj_serializado)
		arquivo.write(obj_criptografado)

	return perfil

def carregar_perfil(nome, chave_mestra):
	"""
	Carrega todas as informações de um Perfil criado em uma sessão anterior.

	Parametros:
		nome: str -> nome do perfil que se deseja carregar.
		chave_mestra: str -> chave para comprovar que o usuario é o dono do
		perfil.

	Retorno:
		Perfil | None -> retorna o Perfil carregado em caso de sucesso e None
		em caso de fracasso.

	Raise:
		FileNotFoundError -> será lançado caso o perfil identificado por 'nome'
		não exista.

		InvalidToken -> será lançado caso a 'chave_mestra' sejá invalida para
		o perfil selecionado

	"""

	f = Fernet(gerar_chave_mestra(nome, chave_mestra))

	perfil = None

	with open(f"./perfis/{nome}.pkl", "rb") as arquivo:
		obj_criptografado = arquivo.read()
		obj_serializado = f.decrypt(obj_criptografado)
		perfil = pickle.loads(obj_serializado)

	return perfil

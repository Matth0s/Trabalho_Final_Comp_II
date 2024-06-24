import os
import base64
import pickle
import string
import random as rd

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

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

def gerar_senha(tamanho = 8, maiusculo = True, minusculo = True, numero = True,
			   especial = True):
	"""
	Gera senhas fortes com a escolha de caracteres permitidos.

	Parametros:
		tamanho  : int  -> numero de caracteres na senha.
		maiusculo: bool -> permissão para a senha conter caracteres maiúsculos.
		minusculo: bool -> permissão para a senha conter caracteres minúsculos.
		numero   : bool -> permissão para a senha conter caracteres numéricos.
		especial : bool -> permissão para a senha conter caracteres especiais.

	Retorno:
		(str, int) -> uma tupla contendo a senha criada e um codigo binario
		identificando quais restrições de criação foram utilizadas.

	Raises:
		ValueError: se todos os parametros passados são iguais a False
	"""

	caracteres_possiveis = ""
	tipo_de_senha = 0b0000

	if maiusculo:
		tipo_de_senha |= 0b0001
		caracteres_possiveis += string.ascii_uppercase
	if minusculo:
		tipo_de_senha |= 0b0010
		caracteres_possiveis += string.ascii_lowercase
	if numero:
		tipo_de_senha |= 0b0100
		caracteres_possiveis += string.digits
	if especial:
		tipo_de_senha |= 0b1000
		caracteres_possiveis += string.punctuation

	if not caracteres_possiveis:
		raise ValueError("A senha precisa ter pelo menos um tipo de caractere")

	senha =  ""
	for i in range(tamanho):
		senha += rd.choice(caracteres_possiveis)

	return senha, tipo_de_senha


def salvar_perfil(perfil):
	"""
	Salva todas as informações do Perfil logado no programa.

	Parametros:
		perfil: Perfil  -> objeto Perfil logado no programa.
	"""

	try:
		if not os.path.exists("./perfis"):
			os.mkdir("./perfis")

		obj_serializado = pickle.dumps(perfil)

		with open(f"./perfis/{perfil.getNome()}.pkl", "wb") as arquivo:
			arquivo.write(obj_serializado)

	except Exception as e:
		print(f"Erro ao tentar salvar o Perfil: {e}")


def carregar_perfil(nome):
	"""
	Carrega todas as informações de um Perfil criado em uma sessão anterior.

	Parametros:
		nome: str -> nome do perfil que se deseja carregar.

	Retorno:
		Perfil | None -> retorna o Perfil carregado em caso de sucesso e None
		em caso de fracasso.
	"""

	try:
		with open(f"./perfis/{nome}.pkl", "rb") as arquivo:
			obj = pickle.load(arquivo)
			return obj

	except FileNotFoundError:
		print("O Perfil '{nome}' não existe!")
		return None

	except Exception as e:
		print(f"Erro ao tentar carregar o Perfil: {e}")
		return None

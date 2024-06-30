
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

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
	nucleo = nome_perfil.lower() + palavra_chave
	n = len(nucleo).to_bytes(8, 'big')
	kdf = PBKDF2HMAC(hashes.SHA256(), 32, n, 100000, default_backend())
	chave = base64.urlsafe_b64encode(kdf.derive(nucleo.encode()))

	return chave


__all__ = ["gerar_chave_mestra"]

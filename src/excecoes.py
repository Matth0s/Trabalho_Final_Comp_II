class PerfilJaExisteError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class ChavesDiferentes(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class NomeNulo(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class SemTipoDeCaractere(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class TamanhoInvalido(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

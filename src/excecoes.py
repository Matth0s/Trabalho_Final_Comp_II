class PerfilJaExisteError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class ChavesDiferentes(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

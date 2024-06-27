"""
	Modulo de Exceções personalizadas
"""

class NomeNuloError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class PerfilJaExisteError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class ChavesDiferentesError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class SemTipoDeCaractereError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class TamanhoInvalidoError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

class AcessoInvalidoError(Exception):
	def __init__(self, mensagem):
		super().__init__(mensagem)

__all__ = [
	"NomeNuloError",
	"PerfilJaExisteError",
	"ChavesDiferentesError",
	"SemTipoDeCaractereError",
	"TamanhoInvalidoError",
	"AcessoInvalidoError"
	]

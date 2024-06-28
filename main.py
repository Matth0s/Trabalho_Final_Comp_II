from modulos import *

import tkinter as tk

class Janela(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title("GGS")
		self["background"] = "white"
		self.geometry("400x400+100+100")

		self.__perfil = None

		self.__frame_atual = None
		self.trocar_frame("bem_vindo")

	@property
	def perfil(self):
		return self.__perfil

	@perfil.setter
	def perfil(self, perfil):
		self.__perfil = perfil

	def trocar_frame(self, frame, **kwargs):
		"""
		Faz a troca de frames destruindo o antigo e criando o novo
		"""

		if self.__frame_atual != None:
			self.__frame_atual.destroy()
			self.unbind_all("<Return>")

		if frame == "bem_vindo":
			self.__frame_atual = FrameBemVindo(self, self)
		elif frame == "criar_perfil":
			self.__frame_atual = FrameCriarPerfil(self, self)
		elif frame == "carregar_perfil":
			self.__frame_atual = FrameCarregarPerfil(self, self)
		elif frame == "usuario_opcoes":
			self.__frame_atual = FrameUsuarioOpcoes(self, self)
		elif frame == "criar_senha":
			self.__frame_atual = FrameCriarSenha(self, self)
		elif frame == "ver_senha":
			self.__frame_atual = FrameVerSenha(self, self, kwargs["index"])
		elif frame == "mudar_nome":
			self.__frame_atual = FrameMudarNome(self, self)
		elif frame == "mudar_chave":
			self.__frame_atual = FrameMudarChaveMestra(self, self)

		self.__frame_atual.pack(expand=True, fill=tk.BOTH)


if __name__ == "__main__":
	janela = Janela()
	janela.mainloop()

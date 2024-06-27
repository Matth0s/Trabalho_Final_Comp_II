from modulos import *
from .excecoes import *
from cryptography.fernet import InvalidToken
from .uteis import criar_perfil
from .uteis import carregar_perfil

import tkinter as tk

class FrameBemVindo(tk.Frame):
	def __init__(self, parent, janela):
		super().__init__(parent)
		self.__janela = janela

		tk.Label(self, text="Bem Vindo", font=("Arial", 40)
			).pack(side=tk.TOP, padx=10, pady=50, fill=tk.BOTH)

		botoes = [
			["Criar Perfil", lambda : self.__janela.trocar_frame("criar_perfil")],
			["Carregar Perfil", lambda : self.__janela.trocar_frame("carregar_perfil")]
		]
		self.criar_botoes(botoes)

	def criar_botoes(self, botoes):
		"""
		Configura as ações dos botoes do Frame de acordo com o parametro passado

		botoes : [
			[nome no botão 1, ação do botão 1],
			[nome no botão 2, ação do botão 2],
			...
		]
		"""
		for botao in botoes:
			tk.Button(self, text=botao[0], bg="lightgrey", width=30, height=3,
							command=botao[1]
				).pack(side=tk.TOP, padx=50, pady=20, fill=tk.BOTH)

class FrameFormularioSimples(tk.Frame):
	def __init__(self, parent, janela):
		super().__init__(parent)
		self.__janela = janela

		self.__botao_voltar = tk.Button(self, text="Voltar", bg="lightgrey", command=self.voltar)
		self.__corpo = tk.Frame(self)
		self.__botao_acao = tk.Button(self, text="Acão", bg="lightgrey", command=self.acao)

		self.__botao_voltar.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
		self.__corpo.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
		self.__botao_acao.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)

		self.__entrys = {}
		self.__erro_labels = {}

	@property
	def janela(self):
		return self.__janela

	@property
	def entrys(self):
		return self.__entrys

	@property
	def erro_labels(self):
		return self.__erro_labels

	def voltar(self):
		"""
		Função que será sobrescrita nas subclasses de FrameFormularioSimples para ser
		ativada ao apertar o botão "Voltar"
		"""
		pass

	def acao(self):
		"""
		Função que será sobrescrita nas subclasses de FrameFormularioSimples para ser
		ativada ao apertar o botão 'Ação'
		"""
		pass

	def setNomeAcao(self, nome_acao):
		"""
		Função para as subclasses conseguirem personalizar o texto do botão de
		'Ação'
		"""
		self.__botao_acao.config(text=nome_acao)

	def criar_Forms(self, campos_infos):
		"""
		Popula o corpo do formulario com a lista de informações dos campos passada

		campos : [
			[nome da label 1, id da entry 1, char de exibição da entry 1],
			[nome da label 2, id da entry 2, char de exibição da entry 2],
			...
		]
		"""
		for campo_info in campos_infos:
			frame_temp = tk.Frame(self.__corpo)
			frame_temp.pack(pady=10, expand=True, fill=tk.BOTH)

			tk.Label(frame_temp, text=campo_info[0], font=("Arial", 15)
			).pack(side=tk.TOP, padx=10, pady=5)

			self.__entrys[campo_info[1]] = tk.Entry(frame_temp, bg="lightgrey",
												 width=30, show=campo_info[2])
			self.__entrys[campo_info[1]].pack(side=tk.TOP)

			self.__erro_labels[campo_info[1]] = tk.Label(frame_temp, text="",
												 font=("Arial", 10), fg="red")
			self.__erro_labels[campo_info[1]].pack(side=tk.TOP, padx=10)

class FrameCriarPerfil(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		campos_infos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*'],
			["Repita a Chave Mestra", "repetir", '*']
		]
		super().criar_Forms(campos_infos)

		super().setNomeAcao("Criar")

	def voltar(self):
		super().janela.trocar_frame("bem_vindo")

	def acao(self):
		try:
			for erro_label in super().erro_labels.values():
				erro_label.config(text="")

			super().janela.perfil = criar_perfil(
					super().entrys["nome"].get(),
					super().entrys["chave"].get(),
					super().entrys["repetir"].get()
				)

			super().janela.trocar_frame("usuario_opcoes")

		except (NomeNuloError, PerfilJaExisteError) as e:
			super().erro_labels["nome"].config(text=e)
		except ChavesDiferentesError as e:
			super().entrys["repetir"].delete(0, tk.END)
			super().erro_labels["repetir"].config(text=e)
		except Exception as e:
			print(f"Erro ao tentar criar o Perfil: {e}")
			self.voltar()

class FrameCarregarPerfil(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		campos_infos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*'],
		]
		super().criar_Forms(campos_infos)

		super().setNomeAcao("Carregar")

	def voltar(self):
		super().janela.trocar_frame("bem_vindo")

	def acao(self):
		try:
			for erro_label in super().erro_labels.values():
				erro_label.config(text="")

			super().janela.perfil = carregar_perfil(
					super().entrys["nome"].get(),
					super().entrys["chave"].get()
				)

			super().janela.trocar_frame("usuario_opcoes")

		except NomeNuloError as e:
			super().erro_labels["nome"].config(text=e)
		except FileNotFoundError:
			super().erro_labels["nome"].config(
				text=f"O Perfil '{super().entrys["nome"].get()}' não existe!")
		except InvalidToken:
			super().entrys["chave"].delete(0, tk.END)
			super().erro_labels["chave"].config(text=f"Chave Mestra utilizada invalida!")
		except Exception as e:
			print(f"Erro ao tentar carregar o Perfil: {e}")
			self.voltar()

class FrameScrollY(tk.Frame):
	def __init__(self, parent, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		self.__canvas = tk.Canvas(self, bg="lightgrey")
		self.__scroll = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.__canvas.yview)
		self.__nucleo = tk.Frame(self.__canvas)
		self.__id = self.__canvas.create_window((0, 0), window=self.__nucleo, anchor="nw")

		self.__scroll.pack(side=tk.RIGHT, fill=tk.Y)
		self.__canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
		self.__canvas.configure(yscrollcommand=self.__scroll.set)

		self.__canvas.bind("<Configure>", lambda _ : self.__canvas_bind_configure())
		self.bind("<Enter>", lambda _ : self.__self_bind_scroll())
		self.bind("<Leave>", lambda _ : self.__self_unbind_scroll())

	@property
	def nucleo(self):
		return self.__nucleo

	def __canvas_bind_configure(self):
		self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))
		self.__canvas.itemconfig(self.__id, width=self.__canvas.winfo_width())

	def __self_bind_scroll(self):
		self.bind_all("<MouseWheel>", lambda e : self.__canvas.yview_scroll(int(-1 * (e.delta/100)), "units")) # Windows e macOS Scroll
		self.bind_all("<Button-4>", lambda _ : self.__canvas.yview_scroll(-1, "units")) # Linux Scroll Up
		self.bind_all("<Button-5>", lambda _ : self.__canvas.yview_scroll(1, "units")) # Linux Scroll Down

	def __self_unbind_scroll(self):
		self.unbind_all("<MouseWheel>") # Windows e macOS Scroll
		self.unbind_all("<Button-4>") # Linux Scroll Up
		self.unbind_all("<Button-5>") # Linux Scroll Down

class FrameUsuarioOpcoes(tk.Frame):
	def __init__(self, parent, janela):
		super().__init__(parent)
		self.__janela = janela
		if self.__janela.perfil == None:
			raise AcessoInvalidoError("Nenhum perfil logado!")

		self.__corpo = tk.Frame(self)
		self.__frame_botoes = tk.Frame(self.__corpo, width=150)
		self.__frame_senhas = FrameScrollY(self.__corpo)
		self.__frame_senhas.nucleo.config(bg="lightgrey")
		self.__botao_sair = tk.Button(self, text="Sair", bg="lightgrey", command=self.sair)

		tk.Label(self, text=f"Olá {self.__janela.perfil.getNome()}", font=("Arial", 30)
		   ).pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH)

		self.__corpo.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

		self.__frame_botoes.pack(side=tk.LEFT, fill=tk.BOTH)
		self.__frame_botoes.pack_propagate(False)
		self.criar_botoes_opcoes()

		self.__frame_senhas.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
		self.criar_botoes_senhas()

		self.__botao_sair.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)

	def sair(self):
		self.__janela.perfil = None
		self.__janela.trocar_frame("bem_vindo")

	def criar_botoes_opcoes(self):
		botoes = [
			["Criar Senha", lambda : self.__janela.trocar_frame("criar_senha")],
			["Deletar Senha", None],
			["Mudar Nome", None],
			["Mudar Chave Mestra", None],
			["Gerar Estatisticas", None]
		]
		for botao in botoes:
			tk.Button(self.__frame_botoes, text=botao[0], bg="lightgrey", height=2,
				command=botao[1]
			).pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH)

	def criar_botoes_senhas(self):
		for senha in self.__janela.perfil.getSenhas():
			tk.Button(self.__frame_senhas.nucleo, text=senha, bg="white",
				command=None
			).pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH)

class FrameFormularioComplexo(tk.Frame):
	def __init__(self, parent, janela):
		super().__init__(parent)
		self.__janela = janela

		self.__botao_voltar = tk.Button(self, text="Voltar", bg="lightgrey", command=self.voltar)
		self.__corpo = tk.Frame(self)
		self.__botao_acao1 = tk.Button(self, text="Acão 1", bg="lightgrey", command=self.acao1)
		self.__botao_acao2 = tk.Button(self, text="Acão 2", bg="lightgrey", command=self.acao2)

		self.__botao_voltar.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
		self.__corpo.pack(side=tk.TOP, expand=True)
		self.__botao_acao1.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)
		self.__botao_acao_ativo = 1

		self.__entrys = {}
		self.__boxes = {}
		self.__erro_labels = {}
		self.__intvars = {}

	@property
	def janela(self):
		return self.__janela

	@property
	def entrys(self):
		return self.__entrys

	@property
	def erro_labels(self):
		return self.__erro_labels

	@property
	def intvars(self):
		return self.__intvars

	def voltar(self):
		self.__janela.trocar_frame("usuario_opcoes")

	def acao1(self):
		pass

	def acao2(self):
		pass

	def alternar_acao(self):
		if self.__botao_acao_ativo == 1:
			self.__botao_acao1.pack_forget()
			self.__botao_acao2.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)
			self.__botao_acao_ativo = 2
		else:
			self.__botao_acao2.pack_forget()
			self.__botao_acao1.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)
			self.__botao_acao_ativo = 1

	def setNomeAcao1(self, nome_acao):
		"""
		Função para as subclasses conseguirem personalizar o texto do botão de
		'Ação 1'
		"""
		self.__botao_acao1.config(text=nome_acao)

	def setNomeAcao2(self, nome_acao):
		"""
		Função para as subclasses conseguirem personalizar o texto do botão de
		'Ação 2'
		"""
		self.__botao_acao2.config(text=nome_acao)

	def desativar(self):
		for entry in self.__entrys.values():
			entry.config(state=tk.DISABLED)
		for box in self.__boxes.values():
			box.config(state=tk.DISABLED)

	def ativar(self):
		for entry in self.__entrys.values():
			entry.config(state=tk.NORMAL)
		for box in self.__boxes.values():
			box.config(state=tk.NORMAL)

	def popup_senha(self, texto):

		def copiar():
			popup.clipboard_clear()
			popup.clipboard_append(texto)
			popup.destroy()

		popup = tk.Toplevel(self.janela)
		popup.title("Senha")
		popup.geometry("400x100+300+300")
		popup.transient(self.janela)
		popup.grab_set()

		frame = tk.Frame(popup)
		frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
		frame.grid_columnconfigure(0, weight=1)
		frame.grid_rowconfigure(0, weight=1)

		tk.Label(frame, text=texto, font=("Arial", 20), bg="lightgrey"
			).grid(row=0, column=0, pady=1, ipadx=5, ipady=5)

		tk.Button(frame, text="Copiar", bg="lightgrey", command=copiar
			).grid(row=0, column=1, pady=1)

	def criar_Forms(self, campos_infos):
		"""
		Popula o corpo do formulario com a lista de informações dos campos passada

		campos : [
			[nome da label 1, id da entry 1, width da entry 1, posição no grid 1],
			[nome da label 2, id da entry 2, width da entry 2, posição no grid 2],
			...
		]
		"""
		for campo_info in campos_infos:
			tk.Label(self.__corpo, text=campo_info[0], font=("Arial", 15)
				).grid(row=campo_info[3] * 2, column=0, sticky=tk.W)
			tk.Label(self.__corpo, text=":", font=("Arial", 15)
				).grid(row=campo_info[3] * 2, column=0, sticky=tk.E)

			self.__entrys[campo_info[1]] = tk.Entry(self.__corpo, bg="lightgrey",
											width=campo_info[2])
			self.__entrys[campo_info[1]].grid(row=campo_info[3] * 2, column=1,
									 		sticky=tk.W)

			self.__erro_labels[campo_info[1]] = tk.Label(self.__corpo, text="",
											font=("Arial", 10), fg="red")
			self.__erro_labels[campo_info[1]].grid(row=campo_info[3] * 2 + 1,
											column=0, columnspan=2)

	def criar_checkboxs(self,campo_info, boxes_infos):
		"""
		Popula o corpo do formulario com a lista de informações dos campos passada

		campos : [
			nome da label, posição no grid, nº de boxes por linha
		]
		boxes : [
			[nome da box 1, valor da box ativada 1, valor da box desativada 1],
			[nome da box 2, valor da box ativada 2, valor da box desativada 2],
			...
		]
		"""
		tk.Label(self.__corpo, text=campo_info[0], font=("Arial", 15)
		   ).grid(row=campo_info[1] * 2, column=0)

		frame_boxes = tk.Frame(self.__corpo)
		frame_boxes.grid(row=campo_info[1] * 2, column=1, sticky=tk.W)
		frame_boxes.grid_columnconfigure(0, weight=1)

		for i, boxes in enumerate(boxes_infos):
			self.__intvars[boxes[0]] = tk.IntVar()
			self.__boxes[boxes[0]] = tk.Checkbutton(frame_boxes, text=boxes[0],
											variable=self.__intvars[boxes[0]],
											 onvalue=boxes[1], offvalue=boxes[2])
			self.__boxes[boxes[0]].grid(row=i%campo_info[2], column=i//campo_info[2])

		self.__erro_labels["tipo"] = tk.Label(self.__corpo, text="", font=("Arial", 10), fg="red")
		self.__erro_labels["tipo"].grid(row=campo_info[1] * 2 + 1, column=0, columnspan=2)

class FrameCriarSenha(FrameFormularioComplexo):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)
		self.__senha = None

		campos_infos = [
			["Identificação", "nome", 26, 0],
			["Username", "username", 26, 1],
			["URL do Login", "URL", 26, 2],
			["Tamanho Senha", "tamanho", 4, 4]
		]
		super().criar_Forms(campos_infos)

		campo_info = ["Tipos de Caracteres :", 3, 2]
		boxes_infos = [
			["maiusculos", 0b0001, 0],
			["minusculos", 0b0010, 0],
			["numeros", 0b0100, 0],
			["especiais", 0b1000, 0]
		]
		super().criar_checkboxs(campo_info, boxes_infos)

		super().setNomeAcao1("Gerar")
		super().setNomeAcao2("Salvar")

	def acao1(self):
		try:
			for erro_label in super().erro_labels.values():
				erro_label.config(text="")

			self.__senha = Senha(
							super().entrys["nome"].get(),
							super().entrys["username"].get(),
							super().entrys["URL"].get(),
							sum(valor.get() for valor in super().intvars.values()),
							super().entrys["tamanho"].get())

			self.popup_senha(self.__senha.getSenha())
			self.desativar()
			self.alternar_acao()
		except NomeNuloError as e:
			super().erro_labels["nome"].config(text=e)
		except SemTipoDeCaractereError as e:
			super().erro_labels["tipo"].config(text=e)
		except TamanhoInvalidoError as e:
			super().erro_labels["tamanho"].config(text=e)
		except Exception as e:
			print(f"Erro ao tentar gerar a Senha: {e}")
			self.voltar()

	def acao2(self):
		super().janela.perfil.addSenha(self.__senha)
		super().janela.perfil.salvar()
		self.voltar()

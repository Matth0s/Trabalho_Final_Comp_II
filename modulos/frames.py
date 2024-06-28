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

		self.criar_botoes("Criar Perfil", "criar_perfil")
		self.criar_botoes("Carregar Perfil", "carregar_perfil")

	def criar_botoes(self, texto, frame_destino):
		"""
		Configura as ações dos botoes do Frame de acordo com o parametro passado
		"""
		tk.Button(self, text=texto, bg="lightgrey", width=30, height=3,
				command=(lambda f = frame_destino : self.__janela.trocar_frame(f))
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
		Função que será sobrescrita nas subclasses de FrameFormularioSimples
		para ser ativada ao apertar o botão "Voltar"
		"""
		pass

	def acao(self):
		"""
		Função que será sobrescrita nas subclasses de FrameFormularioSimples
		para ser ativada ao apertar o botão 'Ação'
		"""
		pass

	def setNomeAcao(self, nome_acao):
		"""
		Função para as subclasses conseguirem personalizar o texto do botão de
		'Ação'
		"""
		self.__botao_acao.config(text=nome_acao)

	def criar_campo(self):
		pass

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

		self.__n_widges = 0
		self.__entrys = {}
		self.__checks = {}
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
		"""
		Função que será sobrescrita nas subclasses de FrameFormularioComplexo para
		ser ativada ao apertar o botão 'Ação 1'
		"""
		pass

	def setNomeAcao1(self, nome_acao):
		"""
		Função para as subclasses conseguirem personalizar o texto do botão de
		'Ação 1'
		"""
		self.__botao_acao1.config(text=nome_acao)

	def acao2(self):
		"""
		Função que será sobrescrita nas subclasses de FrameFormularioComplexo para
		ser ativada ao apertar o botão 'Ação 2'
		"""
		pass

	def setNomeAcao2(self, nome_acao):
		"""
		Função para as subclasses conseguirem personalizar o texto do botão de
		'Ação 2'
		"""
		self.__botao_acao2.config(text=nome_acao)

	def alternar_acao(self):
		if self.__botao_acao_ativo == 1:
			self.__botao_acao1.pack_forget()
			self.__botao_acao2.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)
			self.__botao_acao_ativo = 2
		else:
			self.__botao_acao2.pack_forget()
			self.__botao_acao1.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)
			self.__botao_acao_ativo = 1

	def desativar(self):
		for entry in self.__entrys.values():
			entry.config(state=tk.DISABLED)
		for check in self.__checks.values():
			check.config(state=tk.DISABLED)

	def ativar(self):
		for entry in self.__entrys.values():
			entry.config(state=tk.NORMAL)
		for check in self.__checks.values():
			check.config(state=tk.NORMAL)

	def criar_entry(self, id, text, width=26):
		"""
		Cria um bloco de widges formado por Label, Entry e Label Error
		Parametros:
			id: str -> chave que sera utilizada para guardar as entrys e labels erros criadas
			text: str -> texto que será inserido na label principal
			widht: int -> width da entry que será criada
		"""

		tk.Label(self.__corpo, text=text, font=("Arial", 15)
		   ).grid(row=self.__n_widges * 2, column=0, sticky=tk.W)

		tk.Label(self.__corpo, text=":", font=("Arial", 15)
		   ).grid(row=self.__n_widges * 2, column=1, sticky=tk.E)

		self.__entrys[id] = tk.Entry(self.__corpo, bg="lightgrey", width=width)
		self.__entrys[id].grid(row=self.__n_widges * 2, column=2, sticky=tk.W)

		self.__erro_labels[id] = tk.Label(self.__corpo, text="", font=("Arial", 10), fg="red")
		self.__erro_labels[id].grid(row=self.__n_widges * 2 + 1, column=0, columnspan=3)

		self.__n_widges += 1

	def criar_checkbutton(self, id, text, n_col, **checks):
		"""
		Cria um bloco de widges formado por Label, Checkbutton 1, Checkbutton 2, ...
		e Label Error
		Parametros:
			id: str -> chave que sera utilizada para guardar a label erros criada
			text: str -> texto que será inserido na label principal
			n_col: int -> numero que indica quantas Checkbuttons serão inseridas por linha
		"""

		tk.Label(self.__corpo, text=text, font=("Arial", 15)
		   ).grid(row=self.__n_widges * 2, column=0, sticky=tk.W)

		tk.Label(self.__corpo, text=":", font=("Arial", 15)
		   ).grid(row=self.__n_widges * 2, column=1, sticky=tk.E)

		frame_checks = tk.Frame(self.__corpo)
		frame_checks.grid(row=self.__n_widges * 2, column=2, sticky=tk.W)
		frame_checks.grid_columnconfigure(0, weight=1)

		for idx, (id_check, (on_check, off_check)) in enumerate(checks.items()):
			self.__intvars[id_check] = tk.IntVar()
			self.__checks[id_check] = tk.Checkbutton(frame_checks, text=id_check,
										variable=self.__intvars[id_check],
										onvalue=on_check, offvalue=off_check)
			self.__checks[id_check].grid(row=idx%n_col, column=idx//n_col)

		self.__erro_labels[id] = tk.Label(self.__corpo, text="", font=("Arial", 10), fg="red")
		self.__erro_labels[id].grid(row=self.__n_widges * 2 + 1, column=0, columnspan=3)

		self.__n_widges += 1

	def criar_entry_button(self, id, text_label, text_button, action):
		"""
		Cria um bloco de widges formado por Label, Entry e Button
		Parametros:
			id: str -> chave que sera utilizada para guardar as entrys e labels erros criadas
			text_label: str -> texto que será inserido na label principal
			text_button: str -> texto que será inserido nno botão
			action: func -> função que será executada na interação do botão
		"""

		tk.Label(self.__corpo, text=text_label, font=("Arial", 15)
			).grid(row=self.__n_widges * 2, column=0, sticky=tk.W)

		tk.Label(self.__corpo, text=":", font=("Arial", 15)
			).grid(row=self.__n_widges * 2, column=1, sticky=tk.E)

		frame_conteiner = tk.Frame(self.__corpo)
		frame_conteiner.grid(row=self.__n_widges * 2, column=2, sticky=tk.W)
		frame_conteiner.grid_columnconfigure(0, weight=1)

		self.__entrys[id] = tk.Entry(frame_conteiner, bg="lightgrey", width=20)
		self.__entrys[id].grid(row=0, column=0, sticky=tk.W)

		tk.Button(frame_conteiner, text=text_button, bg="lightgrey", command=action
			).grid(row=0, column=1, sticky=tk.W, padx=5)

		self.__n_widges += 1

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

		popup.grid_columnconfigure(0, weight=1)
		popup.grid_rowconfigure(0, weight=1)

		tk.Label(popup, text=texto, font=("Arial", 20), bg="lightgrey"
			).grid(row=0, column=0, ipadx=5, ipady=5)
		tk.Button(popup, text="Copiar", bg="lightgrey", command=copiar
			).grid(row=0, column=1, padx=20)

	def popup_confirmar(self, senha_idx):

		def sim():
			self.__janela.perfil.removeSenhaByIdx(senha_idx)
			self.__janela.perfil.salvar()
			popup.destroy()
			self.voltar()

		popup = tk.Toplevel(self.janela)
		popup.title("Confirmar")
		popup.geometry("300x100+300+300")
		popup.transient(self.janela)
		popup.grab_set()

		popup.grid_columnconfigure(0, weight=1)
		popup.grid_rowconfigure(0, weight=1)
		popup.grid_rowconfigure(1, weight=1)

		tk.Label(popup, text="Deseja Mesmo Deletar?", font=("Arial", 15)
		   ).grid(row=0, column=0)

		frame_botoes = tk.Frame(popup)
		frame_botoes.grid(row=1, column=0)

		tk.Button(frame_botoes, text="Sim", bg="lightgrey", command=sim
			).grid(row=0, column=0, padx=20, ipadx=4, ipady=2)
		tk.Button(frame_botoes, text="Não", bg="lightgrey", command=popup.destroy
			).grid(row=0, column=1, padx=20, ipadx=4, ipady=2)


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

		tk.Label(self, text=f"Olá {self.__janela.perfil.getNome()}", font=("Arial", 30)
			).pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH)

		tk.Button(self, text="Sair", bg="lightgrey", command=self.sair
			).pack(side=tk.BOTTOM, anchor=tk.S, padx=20, pady=10, expand=True)

		self.__corpo = tk.Frame(self)
		self.__frame_esquerda = tk.Frame(self.__corpo, width=150)
		self.__frame_direita = tk.Frame(self.__corpo)
		self.__botoes_senhas = []

		self.criar_frame_buscar()
		self.__corpo.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
		self.__frame_esquerda.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
		self.__frame_esquerda.pack_propagate(False)
		self.criar_frame_botoes()
		self.__frame_direita.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
		self.criar_frame_senhas()

	def sair(self):
		self.__janela.perfil = None
		self.__janela.trocar_frame("bem_vindo")

	def bucar_senhas(self, text):
		for botao in self.__botoes_senhas:
			if text.lower() in botao.cget("text").lower():
				botao.pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH)
			else:
				botao.pack_forget()

	def criar_frame_buscar(self):
		frame_buscar = tk.Frame(self)
		frame_buscar.pack(side=tk.TOP, fill=tk.X, padx=18, pady=10)

		entry = tk.Entry(frame_buscar, width=28)

		tk.Button(frame_buscar, text="Buscar", bg="lightgrey",
			command=lambda : self.bucar_senhas(entry.get())
			).pack(side=tk.RIGHT)

		entry.pack(side=tk.RIGHT, padx=10)

	def criar_frame_botoes(self):
		frame_botoes = tk.Frame(self.__frame_esquerda)
		frame_botoes.pack(side=tk.LEFT, anchor=tk.W, fill=tk.X, expand=True)

		botoes = [
			["Criar Senha", lambda : self.__janela.trocar_frame("criar_senha")],
			["Mudar Nome", None],
			["Mudar Chave Mestra", None],
			["Gerar Estatisticas", None]
		]
		for botao in botoes:
			tk.Button(frame_botoes, text=botao[0], bg="lightgrey", height=2,
				command=botao[1]
			).pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH)

	def criar_frame_senhas(self):
		frame_senhas = FrameScrollY(self.__frame_direita)
		frame_senhas.nucleo.config(bg="lightgrey")
		frame_senhas.pack(side=tk.TOP, anchor=tk.W, fill=tk.BOTH, expand=True)

		for idx, senha in enumerate(self.__janela.perfil.getNomesSenhas()):
			botao = tk.Button(frame_senhas.nucleo, text=senha, bg="white",
				command=(lambda i = idx : self.__janela.trocar_frame("ver_senha", index=i)))
			botao.pack(side=tk.TOP, padx=20, pady=5, fill=tk.BOTH)
			self.__botoes_senhas.append(botao)


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


class FrameCriarSenha(FrameFormularioComplexo):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)
		self.__senha = None

		super().criar_entry("nome", "Identificação")
		super().criar_entry("username", "Username")
		super().criar_entry("URL", "URL do Login")
		super().criar_checkbutton("tipo", "Tipos de Caracteres", 2,
										maiusculos=[0b0001, 0],
										minusculos=[0b0010, 0],
										numeros=[0b0100, 0],
										especiais=[0b1000, 0])
		super().criar_entry("tamanho", "Tamanho Senha", 4)

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

class FrameVerSenha(FrameFormularioComplexo):
	def __init__(self, parent, janela, senha_idx):
		super().__init__(parent, janela)
		self.__senha_idx = senha_idx
		self.__senha = super().janela.perfil.getSenhaByIdx(self.__senha_idx)

		super().criar_entry("nome", "Identificação")
		super().criar_entry("username", "Username")
		super().criar_entry("URL", "URL do Login")
		super().criar_checkbutton("tipo", "Tipos de Caracteres", 2,
										maiusculos=[0b0001, 0],
										minusculos=[0b0010, 0],
										numeros=[0b0100, 0],
										especiais=[0b1000, 0])
		super().criar_entry("tamanho", "Tamanho Senha", 4)
		super().criar_entry_button("senha", "Senha", "Mostrar",
					lambda s = self.__senha.getSenha() : self.popup_senha(s))

		super().setNomeAcao1("Deletar")

		self.settar_campos()
		self.desativar()

	def settar_campos(self):
		super().entrys["nome"].insert(0, self.__senha.getNome())
		super().entrys["username"].insert(0, self.__senha.getUsername())
		super().entrys["URL"].insert(0, self.__senha.getURL())
		super().entrys["tamanho"].insert(0, self.__senha.getTamanho())
		super().entrys["senha"].insert(0, "*" *  self.__senha.getTamanho())

		tipo = self.__senha.getTipo()
		boxes_infos = [
			["maiusculos", 0b0001],
			["minusculos", 0b0010],
			["numeros", 0b0100],
			["especiais", 0b1000]
		]

		for t_identificador,  t_cod in boxes_infos:
			if (tipo & t_cod) != 0:
				super().intvars[t_identificador].set(t_cod)

	def acao1(self):
		self.popup_confirmar(self.__senha_idx)
from modulos import *
from .excecoes import *
from cryptography.fernet import InvalidToken
from .uteis import criar_perfil
from .uteis import carregar_perfil
from .uteis import gerar_chave_mestra

import matplotlib.pyplot as plt
import tkinter as tk
import numpy as np
import os

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
			["Mudar Nome", lambda : self.__janela.trocar_frame("mudar_nome")],
			["Mudar Chave Mestra", lambda : self.__janela.trocar_frame("mudar_chave")],
			["Gerar Estatisticas", lambda : self.__janela.trocar_frame("estatisticas")]
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


class FrameFormularioSimples(tk.Frame):
	def __init__(self, parent, janela):
		super().__init__(parent)
		self.__janela = janela

		self.__botao_voltar = tk.Button(self, text="Voltar", bg="lightgrey", command=self.voltar)
		self.__corpo = tk.Frame(self)
		self.__botao_acao = tk.Button(self, text="Acão", bg="lightgrey", command=self.acao)
		self.__janela.bind_all("<Return>", lambda _ : self.__botao_acao.invoke())

		self.__botao_voltar.pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)
		self.__corpo.pack(side=tk.TOP, expand=True, fill=tk.BOTH)
		self.__botao_acao.pack(side=tk.BOTTOM, anchor=tk.S, padx=10, pady=10)

		self.__entrys = {}
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

	def criar_campo(self, id, texto, char=None):
		"""
		Cria um bloco de widges formado por Label, Entry e Label Error
		Parametros:
			id: str -> chave que sera utilizada para guardar as entrys e labels erros criadas
			texto: str -> texto que será inserido na label principal
			char: int -> caracter que será exibido na digitação da entry
		"""
		frame = tk.Frame(self.__corpo)
		frame.pack(pady=10, expand=True, fill=tk.BOTH)

		tk.Label(frame, text=texto, font=("Arial", 15)
			).pack(side=tk.TOP, padx=10, pady=5)

		self.__entrys[id] = tk.Entry(frame, bg="lightgrey", width=30, show=char)
		self.__entrys[id].pack(side=tk.TOP)

		self.__erro_labels[id] = tk.Label(frame, text="", font=("Arial", 10), fg="red")
		self.__erro_labels[id].pack(side=tk.TOP, padx=10)

	def criar_check(self, id, texto_label, texto_check):
		"""
		Cria um bloco de widges formado por Label e Checkbutton
		Parametros:
			id: str -> chave que sera utilizada para guardar as entrys e labels erros criadas
			texto_label: str -> texto que será inserido na label
			texto_check: int -> texto que será inserido no checkbutton
		"""
		frame = tk.Frame(self.__corpo)
		frame.pack(side=tk.TOP, pady=10, expand=True, fill=tk.BOTH)

		tk.Label(frame, text=texto_label, font=("Arial", 15)
			).pack(side=tk.TOP, ipadx=10, ipady=5)

		self.__intvars[id] = tk.IntVar()
		tk.Checkbutton(frame, text=texto_check, font=("Arial", 15), bg="lightgrey",
				variable=self.__intvars[id]
			).pack(side=tk.TOP, ipadx=10, ipady=5)

class FrameCriarPerfil(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		super().criar_campo("nome", "Nome do perfil")
		super().criar_campo("chave", "Chave Mestra", '*')
		super().criar_campo("repetir", "Repita a Chave Mestra", '*')

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
		except ChaveNulaError as e:
			super().entrys["repetir"].delete(0, tk.END)
			super().erro_labels["chave"].config(text=e)
		except ChavesDiferentesError as e:
			super().entrys["repetir"].delete(0, tk.END)
			super().erro_labels["repetir"].config(text=e)
		except Exception as e:
			print(f"Erro ao tentar criar o Perfil: {e}")
			self.voltar()

class FrameCarregarPerfil(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		super().criar_campo("nome", "Nome do perfil")
		super().criar_campo("chave", "Chave Mestra", '*')

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

class FrameMudarNome(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		super().criar_campo("nome", "Digite o Novo Nome")
		super().criar_campo("chave", "Digite a Chave Mestra", '*')

		super().setNomeAcao("Mudar")

	def voltar(self):
		super().janela.trocar_frame("usuario_opcoes")

	def acao(self):
		try:
			for erro_label in super().erro_labels.values():
				erro_label.config(text="")

			old_nome = super().janela.perfil.getNome()
			new_nome = super().entrys["nome"].get()
			chave = super().entrys["chave"].get()

			if new_nome == "":
				raise NomeNuloError("O novo nome não pode ser vazio!")

			if os.path.exists(f"./perfis/{new_nome}.pkl"):
				raise PerfilJaExisteError(f"O nome de perfil '{new_nome}' já esta sendo utilizado!")

			if super().janela.perfil.getChave() != gerar_chave_mestra(old_nome, chave):
				raise InvalidToken("Chave Mestra utilizada invalida!")

			super().janela.perfil.setNome(new_nome)
			super().janela.perfil.setChave(gerar_chave_mestra(new_nome, chave))
			super().janela.perfil.salvar()

			os.remove(f"./perfis/{old_nome}.pkl")

			super().janela.trocar_frame("usuario_opcoes")

		except (NomeNuloError, PerfilJaExisteError) as e:
			super().erro_labels["nome"].config(text=e)
		except InvalidToken as e:
			super().entrys["chave"].delete(0, tk.END)
			super().erro_labels["chave"].config(text=e)
		except Exception as e:
			print(f"Erro ao tentar mudar nome do Perfil: {e}")
			self.voltar()

class FrameMudarChaveMestra(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		super().criar_campo("old", "Digite a Chave Mestra Atual", '*')
		super().criar_campo("new", "Digite a Nova Chave Mestra", '*')
		super().criar_campo("repetir", "Repita a Nova Chave Mestra", '*')

		super().setNomeAcao("Mudar")

	def voltar(self):
		super().janela.trocar_frame("usuario_opcoes")

	def acao(self):
		try:
			for erro_label in super().erro_labels.values():
				erro_label.config(text="")

			old_chave = super().entrys["old"].get()
			new_chave = super().entrys["new"].get()
			repetir = super().entrys["repetir"].get()
			nome = super().janela.perfil.getNome()

			if super().janela.perfil.getChave() != gerar_chave_mestra(nome, old_chave):
				raise InvalidToken("Chave Mestra utilizada invalida!")

			if new_chave == "":
				raise ChaveNulaError("É obrigatorio declarar uma Chave Mestra!")

			if new_chave != repetir:
				raise ChavesDiferentesError("As novas chaves mestras não são iguais!")

			super().janela.perfil.setChave(gerar_chave_mestra(nome, new_chave))
			super().janela.perfil.salvar()

			super().janela.trocar_frame("usuario_opcoes")

		except InvalidToken as e:
			super().entrys["old"].delete(0, tk.END)
			super().erro_labels["old"].config(text=e)
		except ChaveNulaError as e:
			super().entrys["new"].delete(0, tk.END)
			super().erro_labels["new"].config(text=e)
		except ChavesDiferentesError as e:
			super().entrys["repetir"].delete(0, tk.END)
			super().erro_labels["repetir"].config(text=e)
		except Exception as e:
			print(f"Erro ao tentar mudar a chave mestra do Perfil: {e}")
			self.voltar()

class FrameGerarEstatisticas(FrameFormularioSimples):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)

		super().criar_check("setor", "Distribuição dos Tipos de Senha", "Grafico de Setor")
		super().criar_check("barra", "Distribuição dos Tamanhos de Senha", "Grafico de Barra")
		super().criar_check("dispersao", "Tipos de Senha vs. Tamanhos de Senha", "Grafico de Dispersão")

		super().setNomeAcao("Gerar")

	def voltar(self):
		super().janela.trocar_frame("usuario_opcoes")

	def acao(self):
		try:
			if not os.path.exists("./estatisticas"):
				os.mkdir("./estatisticas")

			if super().intvars["setor"].get() == 1:
				self.gerar_grafico_setor()

			if super().intvars["barra"].get() == 1:
				self.gerar_grafico_barrar()

			if super().intvars["dispersao"].get() == 1:
				self.gerar_grafico_dispersao()

			for intvar in super().intvars.values():
				intvar.set(0)

			self.popup_gerado()

		except Exception as e:
			print(f"Erro ao tentar gerar as estatisticas do Perfil: {e}")
			self.voltar()

	def gerar_grafico_setor(self):
		tipos, vezes = np.unique(super().janela.perfil.getTiposSenhas(), return_counts=True)
		codigos = [0b0001 , 0b0010 , 0b0100 , 0b1000]
		textos = ["Min, " , "Mai, " , "Num, " , "Esp, "]

		legendas = []
		for tipo in tipos:
			legenda = ""
			for codigo, texto in zip(codigos, textos):
				if (tipo & codigo) != 0:
					legenda += texto
			legendas.append(legenda[:-2])

		textos = [
			"Min: Caracteres Minusculos",
			"Mai: Caracteres Maiusculos",
			"Num: Caracteres Numericos",
			"Esp: Caracteres Especiais"
		]
		texto = "\n".join(textos)

		fig, ax = plt.subplots(figsize=(12, 8))

		ax.pie(vezes, autopct="%.2f%%", labels=legendas,
			wedgeprops={'edgecolor': 'black', 'linewidth': 2}, textprops={'fontsize': 14})
		ax.set_position([0.1, 0, 0.5, 1])
		ax.set_title(f"Grafico de Setor dos Tipos de Senha", fontsize=20, fontweight='bold')

		ax.text(1.8, -1.3, texto, fontsize=15, ha='left', va='center',
					bbox=dict(facecolor='lightgray', alpha=0.5))
		ax.legend(fontsize=15, bbox_to_anchor=(0.97, 0.95), bbox_transform=fig.transFigure)

		fig.savefig(f"./estatisticas/setor_{super().janela.perfil.getNome()}.jpg", format='jpg', dpi = 100)

	def gerar_grafico_barrar(self):
		tamanhos, vezes = np.unique(super().janela.perfil.getTamanhosSenhas(), return_counts=True)

		fig, ax = plt.subplots(figsize=(12, 8))

		ax.bar(tamanhos, vezes, tick_label=tamanhos, edgecolor='black', color="green")
		ax.set_title('Grafico de Barras dos Tamanhos das Senhas', fontsize=20, fontweight='bold')
		ax.set_xlabel('Valores dos Tamanhos')
		ax.set_ylabel('Frequências dos Tamanhos')
		ax.locator_params(axis='y', integer=True)

		fig.savefig(f"./estatisticas/barra_{super().janela.perfil.getNome()}.jpg", format='jpg', dpi = 100)

	def gerar_grafico_dispersao(self):
		tipos = super().janela.perfil.getTiposSenhas()
		tamanhos = super().janela.perfil.getTamanhosSenhas()

		codigos = [0b0001 , 0b0010 , 0b0100 , 0b1000]
		textos = ["Min, " , "Mai, " , "Num, " , "Esp, "]
		int_eixo_x = [i for i in range(1, 16)]
		str_eixo_x = []
		for idx in int_eixo_x:
			x = ""
			for codigo, texto in zip(codigos, textos):
				if (idx & codigo) != 0:
					x += texto
			str_eixo_x.append(x[:-2])

		textos = [
			"Min: Caracteres Minusculos",
			"Mai: Caracteres Maiusculos",
			"Num: Caracteres Numericos",
			"Esp: Caracteres Especiais"
		]
		texto = "\n".join(textos)

		fig, ax = plt.subplots(figsize=(16, 8))

		ax.scatter(tamanhos, tipos, s=100, c='cyan', alpha=0.6)
		plt.subplots_adjust(left=0.05, right=0.8, top=0.9, bottom=0.15)
		ax.text(15.5, 7, texto, fontsize=12, ha='left', va='center',
					bbox=dict(facecolor='lightgray', alpha=0.5))

		ax.set_title('Tipos de Senhas vs. Tamanhos de Senhas', fontsize=20, fontweight='bold')
		ax.set_xlabel('Tipos de Senhas')
		ax.set_ylabel('Tamanhos das Senhas')

		ax.set_xlim(1, 15)
		ax.set_xticks(int_eixo_x)
		ax.set_xticklabels(str_eixo_x, rotation=-30, ha='left')
		plt.grid(True)

		fig.savefig(f"./estatisticas/pontos_{super().janela.perfil.getNome()}.jpg", format='jpg', dpi = 100)

	def popup_gerado(self):
		"""
		PopUp responsavel avisar que os graficos foram gerados
		"""
		popup = tk.Toplevel(self.janela)
		popup.title("Sucesso")
		popup.geometry("400x100+300+300")
		popup.transient(self.janela)
		popup.grab_set()

		tk.Label(popup, text="Graficos Gerados Com Sucesso!", font=("Arial", 15)
			).pack(side=tk.TOP, expand=True, fill=tk.BOTH, pady=5)
		tk.Button(popup, text="Fechar", bg="lightgrey", command=popup.destroy
			).pack(side=tk.BOTTOM, pady=15)


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
			entry.config(state="readonly")
		for check in self.__checks.values():
			check.config(state="disabled")

	def ativar(self):
		for entry in self.__entrys.values():
			entry.config(state="normal")
		for check in self.__checks.values():
			check.config(state="normal")

	def criar_entry(self, id, texto, width=26):
		"""
		Cria um bloco de widges formado por Label, Entry e Label Error
		Parametros:
			id: str -> chave que sera utilizada para guardar as entrys e labels erros criadas
			texto: str -> texto que será inserido na label principal
			widht: int -> width da entry que será criada
		"""
		tk.Label(self.__corpo, text=texto, font=("Arial", 15)
		   ).grid(row=self.__n_widges * 2, column=0, sticky=tk.W)

		tk.Label(self.__corpo, text=":", font=("Arial", 15)
		   ).grid(row=self.__n_widges * 2, column=1, sticky=tk.E)

		self.__entrys[id] = tk.Entry(self.__corpo, bg="lightgrey", width=width)
		self.__entrys[id].grid(row=self.__n_widges * 2, column=2, sticky=tk.W)

		self.__erro_labels[id] = tk.Label(self.__corpo, text="", font=("Arial", 10), fg="red")
		self.__erro_labels[id].grid(row=self.__n_widges * 2 + 1, column=0, columnspan=3)

		self.__n_widges += 1

	def criar_checkbutton(self, id, texto, n_col, **checks):
		"""
		Cria um bloco de widges formado por Label, Checkbutton 1, Checkbutton 2, ...
		e Label Error
		Parametros:
			id: str -> chave que sera utilizada para guardar a label erros criada
			texto: str -> texto que será inserido na label principal
			n_col: int -> numero que indica quantas Checkbuttons serão inseridas por linha
		"""
		tk.Label(self.__corpo, text=texto, font=("Arial", 15)
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

	def criar_entry_button(self, id, texto_label, texto_button, action):
		"""
		Cria um bloco de widges formado por Label, Entry e Button
		Parametros:
			id: str -> chave que sera utilizada para guardar as entrys e labels erros criadas
			texto_label: str -> texto que será inserido na label principal
			texto_button: str -> texto que será inserido nno botão
			action: func -> função que será executada na interação do botão
		"""
		tk.Label(self.__corpo, text=texto_label, font=("Arial", 15)
			).grid(row=self.__n_widges * 2, column=0, sticky=tk.W)

		tk.Label(self.__corpo, text=":", font=("Arial", 15)
			).grid(row=self.__n_widges * 2, column=1, sticky=tk.E)

		frame_conteiner = tk.Frame(self.__corpo)
		frame_conteiner.grid(row=self.__n_widges * 2, column=2, sticky=tk.W)
		frame_conteiner.grid_columnconfigure(0, weight=1)

		self.__entrys[id] = tk.Entry(frame_conteiner, bg="lightgrey", width=20)
		self.__entrys[id].grid(row=0, column=0, sticky=tk.W)

		tk.Button(frame_conteiner, text=texto_button, bg="lightgrey", command=action
			).grid(row=0, column=1, sticky=tk.W, padx=5)

		self.__n_widges += 1

	def popup_senha(self, texto):
		"""
		PopUp responsavel por exibir a senha
		"""
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
		"""
		PopUp responsavel por confimar a exclusão de uma senha
		"""
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

class FrameCriarSenha(FrameFormularioComplexo):
	def __init__(self, parent, janela):
		super().__init__(parent, janela)
		self.__senha = None

		super().criar_entry("nome", "Identificação")
		super().criar_entry("username", "Username")
		super().criar_entry("URL", "URL do Login")
		super().criar_checkbutton("tipo", "Tipos de Senha", 2,
										minusculos=[0b0001, 0],
										maiusculos=[0b0010, 0],
										numeros=[0b0100, 0],
										especiais=[0b1000, 0])
		super().criar_entry("tamanho", "Tamanho da Senha", 4)

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
		super().criar_checkbutton("tipo", "Tipos de Senha", 2,
										minusculos=[0b0001, 0],
										maiusculos=[0b0010, 0],
										numeros=[0b0100, 0],
										especiais=[0b1000, 0])
		super().criar_entry("tamanho", "Tamanho da Senha", 4)
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

		codigos = [0b0001, 0b0010, 0b0100, 0b1000]
		legendas = ["minusculos", "maiusculos", "numeros", "especiais"]
		for codigo,  legenda in zip(codigos, legendas):
			if (tipo & codigo) != 0:
				super().intvars[legenda].set(codigo)

	def acao1(self):
		self.popup_confirmar(self.__senha_idx)

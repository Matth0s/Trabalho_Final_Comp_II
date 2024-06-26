from src import *
import tkinter as tk

def mock_perfil():
	p = Perfil("Teste", "Chave")

	for i in range(10):
		p.addSenha(Senha(f"senha {i}"))

	return p

class Janela:
	def __init__(self, raiz):
		self.__raiz = raiz
		self.__perfil = mock_perfil()
		self.__frames = {}

		self.__raiz.title("GGS")
		self.__raiz["background"] = "white"
		self.__raiz.geometry("400x400+100+100")

		self.frame_bem_vindo()
		self.frame_criar_perfil()
		self.frame_carregar_perfil()
		self.frame_perfil()
		self.frame_criar_senha()

		self.trocar_frame("criar_senha")

	def trocar_frame(self, frame, entrys=None, labels=None, checkboxs=None, intvars=None):
		"""
		Desliga todos os Frames da janela, limpa as alterações feitas e pôe na tela o
		frame passado por parametro.
		"""
		for f in self.__frames.values():
			f.pack_forget()

		self.__frames[frame].pack(expand=True, fill=tk.BOTH)
		self.__raiz.focus()
		if entrys != None:
			for entry in entrys.values():
				entry.config(state=tk.NORMAL)
				entry.delete(0, tk.END)
		if labels != None:
			for label in labels.values():
				label.config(text="")
		if checkboxs != None:
			for checkbox in checkboxs.values():
				checkbox.config(state=tk.NORMAL)
		if intvars != None:
			for intvar in intvars.values():
				intvar.set(0)

	def criar_blocos(self, frame, blocos):
		"""
		Auxilia na criação da triade label, entry, label_warning em um frame
		"""
		entrys = {}
		labels = {}

		blocos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*'],
			["Repita a Chave Mestra", "repetir", '*']
		]

		for bloco in blocos:
			frame_temp = tk.Frame(frame)

			frame_temp.pack(pady=10, expand=True, fill=tk.BOTH)
			tk.Label(frame_temp, text=bloco[0], font=("Arial", 15)
				).pack(side=tk.TOP, padx=10, pady=5)
			entrys[bloco[1]] = tk.Entry(frame_temp, bg="lightgrey", width=30, show=bloco[2])
			entrys[bloco[1]].pack(side=tk.TOP)
			labels[bloco[1]] = tk.Label(frame_temp, text="", font=("Arial", 10), fg="red")
			labels[bloco[1]].pack(side=tk.TOP, padx=10)

		return entrys, labels

	def frame_bem_vindo(self):
		"""
		Cria a janela responsavel por fazer o login do perfil do usuario
		"""
		frame = tk.Frame(self.__raiz)

		tk.Label(frame, text="Bem Vindo", font=("Arial", 40)
		   ).pack(side=tk.TOP, padx=10, pady=50, fill=tk.BOTH)

		# nome do botão, identificador do botão
		botoes = [
			["Criar Perfil", "criar_perfil"],
			["Carregar Perfil", "carregar_perfil"]
		]
		for botao in botoes:
			tk.Button(frame, text=botao[0], bg="lightgrey", width=30, height=3,
				command=(lambda frame_nome = botao[1] : self.trocar_frame(frame_nome)),
			).pack(side=tk.TOP, padx=50, pady=20, fill=tk.BOTH)

		self.__frames["bem_vindo"] = frame

	def frame_criar_perfil(self):
		"""
		Cria a janela responsavel por criar um novo perfil de usuario.
		"""
		frame = tk.Frame(self.__raiz)

		entrys = {}
		labels = {}

		tk.Button(frame, text="Voltar", bg="lightgrey",
			command=lambda : self.trocar_frame("bem_vindo", entrys, labels)
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		# texto da label, identificador da entry, caracter da entry
		blocos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*'],
			["Repita a Chave Mestra", "repetir", '*']
		]
		entrys, labels = self.criar_blocos(frame, blocos)

		def criar():
			try:
				for label in labels.values():
					label.config(text="")
				self.__perfil = criar_perfil(entrys["nome"].get(),
							   entrys["chave"].get(),
							   entrys["repetir"].get())
				self.trocar_frame("perfil", entrys, labels)
			except PerfilJaExisteError as e:
				labels["nome"].config(text=e)
			except ChavesDiferentes as e:
				entrys["repetir"].delete(0, tk.END)
				labels["repetir"].config(text=e)
			except Exception as e:
				print(f"Erro ao tentar criar o Perfil: {e}")
				self.trocar_frame("bem_vindo", entrys, labels)

		tk.Button(frame, text="Criar", bg="lightgrey", command=criar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["criar_perfil"] = frame

	def frame_carregar_perfil(self):
		"""
		Cria a janela responsavel por carregar um perfil já existente
		"""
		frame = tk.Frame(self.__raiz)
		entrys = {}
		labels = {}

		tk.Button(frame, text="Voltar", bg="lightgrey",
			command=lambda : self.trocar_frame("bem_vindo", entrys, labels)
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		# texto da label, identificador da entry, caracter da entry
		blocos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*']
		]
		entrys, labels = self.criar_blocos(frame, blocos)

		def carregar():
			try:
				for label in labels.values():
					label.config(text="")
				self.__perfil = carregar_perfil(entrys["nome"].get(),
								  entrys["chave"].get())
				self.trocar_frame("perfil", entrys, labels)
			except FileNotFoundError:
				labels["nome"].config(text=f"O Perfil '{entrys["nome"].get()}' não existe!")
			except InvalidToken:
				labels["chave"].config(text=f"Chave Mestra utilizada invalida!")
				entrys["chave"].delete(0, tk.END)
			except Exception as e:
				print(f"Erro ao tentar carregar o Perfil: {e}")
				self.trocar_frame("bem_vindo", entrys, labels)

		tk.Button(frame, text="Carregar", bg="lightgrey", command=carregar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["carregar_perfil"] = frame

	def frame_perfil(self):
		"""
		Cria a janela de opções para o usuario executar no programa
		"""
		frame = tk.Frame(self.__raiz)

		def teste():
			print(self.__perfil.getNome())

		tk.Label(frame, text=f"Olá", font=("Arial", 30)
		   ).pack(side=tk.TOP, padx=10, pady=5, fill=tk.BOTH)

		frame_pai = tk.Frame(frame, bg="lightgrey")
		frame_pai.pack(side=tk.TOP, expand=True, fill=tk.BOTH)

		frame_esquerda = self.frame_scroll(frame_pai, 200, tk.LEFT, False)
		frame_direita = self.frame_scroll(frame_pai, 200, tk.RIGHT, True)

		botoes = [
			["Criar Senha", teste],
			# ["Mudar Chave Mestra", teste]
		]
		for botao in botoes:
			tk.Button(frame_esquerda, text=botao[0], bg="lightgrey", #width=30, height=2,
				command=botao[1]
			).pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH)

		def sair():
			self.__perfil = None
			self.trocar_frame("bem_vindo")

		tk.Button(frame, text="Sair", bg="lightgrey", command=sair
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["perfil"] = frame

	def frame_scroll(self, frame, largura, lado, propagar):

		frame_conteiner = tk.Frame(frame, width=largura)
		frame_conteiner.pack(side=lado, fill=tk.BOTH, expand=propagar)
		frame_conteiner.pack_propagate(propagar)

		canvas = tk.Canvas(frame_conteiner)
		y_scroll = tk.Scrollbar(frame_conteiner, orient=tk.VERTICAL, command=canvas.yview)
		y_scroll.pack(side=tk.RIGHT, fill=tk.Y)
		canvas.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

		canvas.configure(yscrollcommand=y_scroll.set)

		frame_conteudo = tk.Frame(canvas)
		item_id = canvas.create_window((0, 0), window=frame_conteudo, anchor="nw")

		def bind_configure(event):
			canvas.configure(scrollregion=canvas.bbox("all"))
			canvas.itemconfig(item_id, width=event.width)

		canvas.bind("<Configure>", lambda e: bind_configure(e))

		def bind_scroll():
			frame_conteiner.bind_all("<MouseWheel>", lambda e : canvas.yview_scroll(int(-1 * (e.delta/100)), "units")) # Windows e macOS Scroll
			frame_conteiner.bind_all("<Button-4>", lambda _ : canvas.yview_scroll(-1, "units")) # Linux Scroll Up
			frame_conteiner.bind_all("<Button-5>", lambda _ : canvas.yview_scroll(1, "units")) # Linux Scroll Down
		def unbind_scroll():
			frame_conteiner.unbind_all("<MouseWheel>") # Windows e macOS Scroll
			frame_conteiner.unbind_all("<Button-4>") # Linux Scroll Up
			frame_conteiner.unbind_all("<Button-5>") # Linux Scroll Down

		frame_conteiner.bind("<Enter>", lambda _ : bind_scroll())
		frame_conteiner.bind("<Leave>", lambda _ : unbind_scroll())

		return frame_conteudo

	def frame_criar_senha(self):

		frame = tk.Frame(self.__raiz)

		entrys = {}
		labels = {}
		int_vars = {}

		tk.Button(frame,
			background="lightgrey", text="Voltar",
			command=lambda : self.trocar_frame("perfil", entrys, labels)
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		frame_central = tk.Frame(frame)
		frame_central.pack(side=tk.TOP, expand=True)

		blocos = [
			["Identificação", "nome", 0],
			["Username", "username", 2],
			["URL do Login", "URL", 4],
			["Tamanho Senha", "tamanho", 8]
		]
		for bloco in blocos:
			tk.Label(frame_central, text=bloco[0], font=("Arial", 15)
				).grid(row=bloco[2], column=0, sticky=tk.W)
			tk.Label(frame_central, text=":", font=("Arial", 15)
				).grid(row=bloco[2], column=0, sticky=tk.E)
			entrys[bloco[1]] = tk.Entry(frame_central, bg="lightgrey", width=(26 if bloco[2] != 8 else 4))
			entrys[bloco[1]].grid(row=bloco[2], column=1, sticky=tk.W)
			labels[bloco[1]] = tk.Label(frame_central, text="", font=("Arial", 10), fg="red")
			labels[bloco[1]].grid(row=bloco[2] + 1, column=0, columnspan=2)

		tk.Label(frame_central, text="Tipos de Caracteres :", font=("Arial", 15)
			).grid(row=6, column=0)
		frame_tipos = tk.Frame(frame_central)
		frame_tipos.grid(row=6, column=1, padx=0, sticky=tk.W)

		frame_tipos.grid_columnconfigure(0, weight=1)

		tipos = [
			["maiusculos", 0b0001],
			["minusculos", 0b0010],
			["numeros", 0b0100],
			["especiais", 0b1000]
		]
		for i, tipo in enumerate(tipos):
			int_vars[tipo[0]] = tk.IntVar()
			tk.Checkbutton(frame_tipos, text=tipo[0], variable=int_vars[tipo[0]],
				  onvalue=tipo[1], offvalue=0b0000).grid(row=i%2, column=i//2)
		labels["tipo"] = tk.Label(frame_central, text="", font=("Arial", 10), fg="red")
		labels["tipo"].grid(row=7, column=0, columnspan=2)

		def gerar():
			try:
				for label in labels.values():
					label.config(text="")
				senha = Senha(
							entrys["nome"].get(),
							entrys["username"].get(),
							entrys["URL"].get(),
							sum(valor.get() for valor in int_vars.values()),
							entrys["tamanho"].get())
				self.frame_popup_senha(senha.getSenha())
				for entry in entrys.values():
					entry.config(state=tk.DISABLED)
			except NomeNulo as e:
				labels["nome"].config(text=e)
			except SemTipoDeCaractere as e:
				labels["tipo"].config(text=e)
			except TamanhoInvalido as e:
				labels["tamanho"].config(text=e)
			except Exception as e:
				print(f"Erro ao tentar gerar a Senha: {e}")

		tk.Button(frame,
			background="lightgrey", text="Gerar",
			command=gerar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["criar_senha"] = frame

	def frame_popup_senha(self, senha):

		popup = tk.Toplevel(self.__raiz)
		popup.title("Senha Gerada")
		popup.geometry("400x100+300+300")
		popup.transient(self.__raiz)
		popup.grab_set()

		def copiar():
			popup.clipboard_clear()
			popup.clipboard_append(senha)
			popup.destroy()

		frame_conteudo = tk.Frame(popup)
		frame_conteudo.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)
		frame_conteudo.grid_columnconfigure(0, weight=1)
		frame_conteudo.grid_rowconfigure(0, weight=1)

		tk.Label(frame_conteudo, text=senha, font=("Arial", 20), bg="lightgrey"
			).grid(row=0, column=0, pady=1, ipadx=5, ipady=5)

		tk.Button(frame_conteudo, text="Copiar", bg="lightgrey", command=copiar
			).grid(row=0, column=1, pady=1)


if __name__ == "__main__":
	raiz = tk.Tk()
	Janela(raiz)
	raiz.mainloop()

"""
Parametros de Avaliação do Programa
	- Ter Conceito de POO
	- Atributos Privados e Metodos de Acesso
	- Persistência de Objetos
	- Leitura de Arquivos
	- Armazenamento de Graficos
	- Tratamento de Exceções
	- Numpy, Matplotlib, Pickle
	- Grafico de plataformas utilizadas
	- poder escrever as proprias senhas?
	administrador do aplicativo, gerar senhas, guardar todas
		herança
		senhas
Quando maior os conceitos trabalhados em aula, melhor
"""

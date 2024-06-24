import tkinter as tk

class Janela:
	def __init__(self, raiz):
		self.raiz = raiz

		self.raiz.title("GGS")
		self.raiz["background"] = "white"
		self.raiz.geometry("400x400+100+100")

		self.frames = {}
		self.frame_bem_vindo()
		self.frame_criar_perfil()
		self.frame_carregar_perfil()

		self.trocar_frame("bem_vindo")

	def trocar_frame(self, frame):
		"""
		Desliga todos os Frames da janela e ativa o frame passado por parametro.
		"""
		self.raiz.focus()
		for f in self.frames.values():
			f.pack_forget()
		self.frames[frame].pack(expand=True, fill='both')

	def frame_bem_vindo(self):
		"""
		Cria a janela responsavel por fazer o login do perfil do usuario
		"""
		frame = tk.Frame(self.raiz)

		tk.Label(frame, text="Bem Vindo", font=("Arial", 40)
		   ).pack(side=tk.TOP, padx=10, pady=50, fill='both')

		tk.Button(frame, text="Criar Perfil", background="lightgrey",
			width=30, height=3, command=lambda:self.trocar_frame("criar_perfil")
			).pack(side=tk.TOP, padx=50, pady=20, fill='both')

		tk.Button(frame, text="Carregar Perfil", background="lightgrey",
			width=30, height=3,	command=lambda:self.trocar_frame("carregar_perfil")
			).pack(side=tk.TOP, padx=50, pady=20, fill='both')

		self.frames["bem_vindo"] = frame

	def frame_criar_perfil(self):
		"""
		Cria a janela responsavel por criar um novo perfil de usuario
		"""
		frame = tk.Frame(self.raiz)
		entrys = {}

		def voltar():
			self.trocar_frame("bem_vindo")
			entrys["nome"].delete(0, tk.END)
			entrys["chave"].delete(0, tk.END)
			entrys["repetir"].delete(0, tk.END)
		tk.Button(frame,
			background="lightgrey", text="Voltar", command=voltar
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		frame_nome = tk.Frame(frame)
		frame_nome.pack(expand=True, fill='both', pady=10)
		tk.Label(frame_nome, text="Nome do perfil", font=("Arial", 15)
		   ).pack(side=tk.TOP, padx=10, pady=10)
		entrys["nome"] = tk.Entry(frame_nome, background="lightgrey", width=30)
		entrys["nome"].pack(side=tk.TOP)

		frame_chave = tk.Frame(frame)
		frame_chave.pack(expand=True, fill='both', pady=10)
		tk.Label(frame_chave, text="Chave Mestra", font=("Arial", 15)
		   ).pack(side=tk.TOP, padx=10, pady=10)
		entrys["chave"] = tk.Entry(frame_chave, background="lightgrey",
							 width=30, show='*')
		entrys["chave"].pack(side=tk.TOP)

		frame_repetir = tk.Frame(frame)
		frame_repetir.pack(expand=True, fill='both', pady=10)
		tk.Label(frame_repetir,
		   text="Repita a Chave Mestra", font=("Arial", 15)
		   ).pack(side=tk.TOP, padx=10, pady=10)
		entrys["repetir"] = tk.Entry(frame_repetir, background="lightgrey",
							   width=30, show='*')
		entrys["repetir"].pack(side=tk.TOP)

		def criar():
			print(entrys["nome"].get())
			print(entrys["chave"].get())
			print(entrys["repetir"].get())
		tk.Button(frame, background="lightgrey", text="Criar", command=criar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.frames["criar_perfil"] = frame

	def frame_carregar_perfil(self):
		"""
		Cria a janela responsavel por carregar um perfil já existente
		"""
		frame = tk.Frame(self.raiz)
		entrys = {}

		def voltar():
			self.trocar_frame("bem_vindo")
			entrys["nome"].delete(0, tk.END)
			entrys["chave"].delete(0, tk.END)
		tk.Button(frame,
			background="lightgrey", text="Voltar", command=voltar
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		frame_nome = tk.Frame(frame)
		frame_nome.pack(expand=True, fill='both', pady=10)
		tk.Label(frame_nome, text="Nome do perfil", font=("Arial", 15)
		   ).pack(side=tk.TOP, padx=10, pady=10)
		entrys["nome"] = tk.Entry(frame_nome, background="lightgrey", width=30)
		entrys["nome"].pack(side=tk.TOP)

		frame_chave = tk.Frame(frame)
		frame_chave.pack(expand=True, fill='both', pady=10)
		tk.Label(frame_chave, text="Chave Mestra", font=("Arial", 15)
		   ).pack(side=tk.TOP, padx=10, pady=10)
		entrys["chave"] = tk.Entry(frame_chave, background="lightgrey",
							 width=30, show='*')
		entrys["chave"].pack(side=tk.TOP)

		def carregar():
			print(entrys["nome"].get())
			print(entrys["chave"].get())
		tk.Button(frame, background="lightgrey", text="Carregar", command=carregar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.frames["carregar_perfil"] = frame


if __name__ == "__main__":
	raiz = tk.Tk()
	Janela(raiz)
	raiz.mainloop()


"""
O Programa Inicia
	if (Perfil Carregado)
		1 - Criar Senha
			- Identificador da senha
			- Parametros de Criação
		2 - Consultar Senha
			- Identificador
		3 - Vizualizar Senha
		4 - Salvar Informes de Senhas
		5 - Mudar Chave Mestra
			- Confirmar Chave Mestra Atual
			- Nova Chave Mestra
		6 - Salvar Perfil
		7 - Sair

	else
		1 - Criar Perfil
			- Escolher Nome
			- Escolher Chave Mestra
		2 - Carregar Perfil
			- Pedir Nome do Perfil
			- Pedir Chave Mestra Para Confirmar Permissão de Ver Perfil
"""

"""
Parametros de Avaliação do Programa
	- Ter Conceito de POO
	- Atributos Privados e Metodos de Acesso
	- Persistência de Objetos
	- Leitura de Arquivos
	- Armazenamento de Graficos
	- Tratamento de Exceções
	- Numpy, Matplotlib, Pickle
Quando maior os conceitos trabalhados em aula, melhor
"""

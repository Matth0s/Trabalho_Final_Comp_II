from src import *
import tkinter as tk

class Janela:
	def __init__(self, raiz):
		self.__raiz = raiz
		self.__perfil = None
		self.__frames = {}

		self.__raiz.title("GGS")
		self.__raiz["background"] = "white"
		self.__raiz.geometry("400x400+100+100")

		self.frame_bem_vindo()
		self.frame_criar_perfil()
		self.frame_carregar_perfil()
		self.frame_opcoes()

		self.trocar_frame("bem_vindo")

	def trocar_frame(self, frame, entrys=None, labels=None):
		"""
		Desliga todos os Frames da janela, limpa suas Entrys e póe na tela o
		frame passado por parametro.
		"""
		for f in self.__frames.values():
			f.pack_forget()

		self.__frames[frame].pack(expand=True, fill='both')
		self.__raiz.focus()
		if entrys != None:
			for entry in entrys.values():
				entry.delete(0, tk.END)
		if labels != None:
			for label in labels.values():
				label.config(text="")

	def frame_bem_vindo(self):
		"""
		Cria a janela responsavel por fazer o login do perfil do usuario
		"""
		frame = tk.Frame(self.__raiz)

		tk.Label(frame, text="Bem Vindo", font=("Arial", 40)
		   ).pack(side=tk.TOP, padx=10, pady=50, fill='both')

		botoes = [
			["Criar Perfil", "criar_perfil"],
			["Carregar Perfil", "carregar_perfil"]
		]
		for botao in botoes:
			tk.Button(frame, text=botao[0], bg="lightgrey", width=30, height=3,
				command=(lambda frame_nome = botao[1] : self.trocar_frame(frame_nome)),
			).pack(side=tk.TOP, padx=50, pady=20, fill='both')

		self.__frames["bem_vindo"] = frame

	def criar_blocos(self, frame, blocos):
		"""
		Auxilia na criação da triade label, entry, label_warning em um frame
		"""
		entrys = {}
		labels = {}

		for bloco in blocos:
			frame_temp = tk.Frame(frame)
			frame_temp.pack(expand=True, fill='both', pady=10)
			tk.Label(frame_temp, text=bloco[0], font=("Arial", 15)
				).pack(side=tk.TOP, padx=10, pady=5)
			entrys[bloco[1]] = tk.Entry(frame_temp, bg="lightgrey", width=30, show=bloco[2])
			entrys[bloco[1]].pack(side=tk.TOP)
			labels[bloco[1]] = tk.Label(frame_temp, text="", font=("Arial", 10), fg="red")
			labels[bloco[1]].pack(side=tk.TOP, padx=10)

		return entrys, labels

	def frame_criar_perfil(self):
		"""
		Cria a janela responsavel por criar um novo perfil de usuario.
		"""
		frame = tk.Frame(self.__raiz)
		entrys = {}
		labels = {}

		tk.Button(frame, bg="lightgrey", text="Voltar",
			command=lambda:self.trocar_frame("bem_vindo", entrys, labels)
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		blocos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*'],
			["Repita a Chave Mestra", "repetir", '*']
		]
		entrys, labels = self.criar_blocos(frame, blocos)

		def criar():
			try:
				self.__perfil = criar_perfil(entrys["nome"].get(),
							   entrys["chave"].get(),
							   entrys["repetir"].get())
				self.trocar_frame("opcoes", entrys, labels)
			except PerfilJaExisteError as e:
				print(e)
				#Botar uma mensagem de erro de perfil
			except ChavesDiferentes as e:
				print(e)
				#mostrar mensagem e limpar as entradas
			except Exception as e:
				print(e)

		tk.Button(frame, background="lightgrey", text="Criar", command=criar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["criar_perfil"] = frame

	def frame_carregar_perfil(self):
		"""
		Cria a janela responsavel por carregar um perfil já existente
		"""
		frame = tk.Frame(self.__raiz)
		entrys = {}
		labels = {}

		tk.Button(frame,
			background="lightgrey", text="Voltar",
			command=lambda:self.trocar_frame("bem_vindo", entrys, labels)
			).pack(side=tk.TOP, anchor=tk.W, padx=10, pady=10)

		blocos = [
			["Nome do perfil", "nome", None],
			["Chave Mestra", "chave", '*']
		]
		entrys, labels = self.criar_blocos(frame, blocos)

		def carregar():
			try:
				self.__perfil = carregar_perfil(entrys["nome"].get(),
								  entrys["chave"].get())
				self.trocar_frame("opcoes", entrys, labels)
			except FileNotFoundError:
				print(f"O Perfil '{entrys["nome"].get()}' não existe!")
			except InvalidToken:
				print("Chave Mestra utilizada invalida!")
			except Exception as e:
				print(f"Erro ao tentar carregar o Perfil: {e}")

		tk.Button(frame, background="lightgrey", text="Carregar", command=carregar
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["carregar_perfil"] = frame

	def frame_opcoes(self):
		"""
		Cria a janela de opções para o usuario executar no programa
		"""
		frame = tk.Frame(self.__raiz)

		def teste():
			print(self.__perfil.getNome())

		tk.Label(frame, text=f"Olá", font=("Arial", 30)
		   ).pack(side=tk.TOP, padx=10, pady=10, fill='both')

		botoes = [
			["Buscar Senha", teste],
			["Criar Senha", teste],
			["Mudar Chave Mestra", teste],
			["", teste],
			["", teste],
		]
		for botao in botoes:
			tk.Button(frame, text=botao[0], bg="lightgrey", width=30, height=2,
				command=botao[1]
			).pack(side=tk.TOP, padx=50, pady=5, fill='both')

		def sair():
			self.__perfil = None
			self.trocar_frame("bem_vindo")

		tk.Button(frame, background="lightgrey", text="Sair", command=sair
			).pack(side=tk.BOTTOM, padx=10, pady=10)

		self.__frames["opcoes"] = frame

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
Quando maior os conceitos trabalhados em aula, melhor
"""

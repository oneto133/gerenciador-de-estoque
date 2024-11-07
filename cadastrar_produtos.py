from tkinter import *
from PIL import ImageTk, Image
from connection_with_db import consulta
import asyncio
from threading import Thread
import tela_inicial
class Tela: 
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastrar")
        self.janela.configure(bg="white")

        #configurações da tela
            #Tamanho da janela
        largura_da_janela = self.janela.winfo_screenwidth()
        altura_da_janela = self.janela.winfo_screenheight()
        janela_width = 400
        janela_height = 400
        x = (largura_da_janela - janela_width) // 2
        y = (altura_da_janela - janela_height) // 2
          #Configuração da janela
        self.janela.geometry(f'{janela_width}x{janela_height}+{x}+{y}')
        self.janela.resizable(False, False)


        #elementos da tela
            #Adicionando imagem ao botão de pesquisa
        try:
            self.label = Label(self.janela, width=49)
            self.imagem = Image.open(r'imagens/voltar.png')
            self.imagem = self.imagem.resize((30, 30))
            self.imagem_voltar = ImageTk.PhotoImage(self.imagem)
        except:
            self.imagem_voltar = None
        

        #frames
        self.frame_superior = Frame(self.janela, bg='black')
        self.pontinhos_do_frame = Label(self.frame_superior, text="⋮", width=2, bg="black", fg="white",
        cursor="hand2", font=("Arial", 20))
        self.cadastrar_produtos = Label(self.frame_superior, text='Cadastrar Produtos',
        width=20, height=2, fg="white", bg="black", font=("Arial", 12, "bold"))

        #outros
        self.voltar = Button(self.frame_superior, image=self.imagem_voltar, command=self.tela_inicial).pack(side="left")


        
        #menu
        self.menu = Menu(self.janela, tearoff=0)
        self.menu.add_command(label="Login", command=lambda: print("login"))
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=self.fechar_programa)

        #Posicionando os elementos da tela
            #grid()

        self.label.grid(row=1, column=1, padx=30)
        self.frame_superior.grid(row=1, column=1, sticky="ew")

            #place()
        self.cadastrar_produtos.place(x=100, y=-2)

            #pack()
        self.pontinhos_do_frame.pack(side="right")

        #Pegar eventos
        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)

    def fechar_programa(self):
        self.janela.quit()
        self.janela.destroy()
    
    def tela_inicial(self):
        self.janela.withdraw()
        self.tela_principal = Toplevel(self.janela)
        self.tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        tela_inicial.Tela(self.tela_principal)
    
    def consultar(self):
        self.descrição.config(text="Carregando...", font=("Arial", 10))
        asyncio.run(self.Consultar_Produtos())    

    async def Consultar_Produtos(self):
        try:
            consultar = consulta()
            dados = self.realizar_pesquisa.get()
            pesquisar = await consultar.Consultar_Estoque(consulta=dados)
            self.descrição.config(text=pesquisar[0], font=("Arial", 20, "bold"))
            if pesquisar[1] == "<":
                interno = "000000"
            else:
                interno = pesquisar[1]

            self.codigo_interno.config(text=interno)
            self.ean.config(text=pesquisar[2])
            self.quantidade.config(text=f"Quantidade: {pesquisar[3]}", font=("Arial", 12, "bold"))
            Frame(self.frame_de_resultado, height=2, width=350, bg='black').place(x=-10, y=130)
        except TypeError as e:
            self.descrição.config(text="Nenhum ítem encotrado!")
            

    def Cadastrar_produtos(self, event):
        print("Cadastrar")


    def Movimentações(self, event):
        print("Movimentar")

    def Logística(self, event):
        print("Logística")

    def Opções(self, event):
        self.menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    tela = Tk()
    Tela(tela)
    tela.mainloop()
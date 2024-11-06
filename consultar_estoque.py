from tkinter import *
from PIL import ImageTk, Image
from connection_with_db import consulta
import asyncio

class Tela:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Consulta de estoque")

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
        #self.janela.resizable(False, False)


        #elementos da tela
            #Adicionando imagem ao botão de pesquisa
        self.realizar_pesquisa = Entry(self.janela, width=50) 
        try:
            self.imagem = Image.open('download.png')
            self.imagem = self.imagem.resize((30, 30))
            self.foto= ImageTk.PhotoImage(self.imagem)
        except:
            self.foto = None

        self.lupa = Label(self.janela, image=self.foto, cursor="hand2")

        #frames
        self.frame_superior = Frame(self.janela, bg='black')
        self.frame_de_resultado = Frame(self.janela, bg='blue', width=300, height=300)
        self.pontinhos_do_frame = Label(self.frame_superior, text="⋮", width=2, bg="black", fg="white",
        cursor="hand2", font=("Arial", 20))
        self.consulta_de_estoque = Label(self.frame_superior, text='Consultar estoque',
        width=20, height=2, fg="white", bg="black", font=("Arial", 12, "bold"))
        
        #menu
        self.menu = Menu(self.janela, tearoff=0)
        self.menu.add_command(label="Login", command=lambda: print("login"))
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=lambda: print("Sair"))


        #Posicionando os elementos da tela
        self.consulta_de_estoque.place(x=100, y=-2)
        self.realizar_pesquisa.grid(row=4, column=1, padx=50, pady=7)
        self.frame_de_resultado.grid(row=5, column=1)
        self.frame_superior.grid(row=1, column=1, sticky="ew")
        self.pontinhos_do_frame.pack(side="right")
        self.lupa.place(x=360, y=39)


        #Pegar eventos

        self.lupa.bind("<Button-1>", self.consultar)

        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)
    

    def consultar(self, event):
        asyncio.run(self.Consultar_Produtos())    

    async def Consultar_Produtos(self):
        consultar = consulta()
        dados = self.realizar_pesquisa.get()
        pesquisar = await consultar.Consultar_Estoque(consulta=dados)
        descrição = Label(self.frame_de_resultado, text=pesquisar[0], bg='blue', fg='white',
        font=("Arial", 20, "bold")).place(x=20, y=30)
        if pesquisar[1] == "<":
            interno = "000000"
        else:
            interno = pesquisar[1]
        codigo_interno = Label(self.frame_de_resultado, text=interno, bg='blue', fg='white').place(x=20, y=80)

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
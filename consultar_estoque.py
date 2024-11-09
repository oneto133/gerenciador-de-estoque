from tkinter import *
from PIL import ImageTk, Image
from connection_with_db import consulta
import asyncio
from threading import Thread
import tela_inicial
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
        self.janela.resizable(False, False)


        #elementos da tela
            #Adicionando imagem ao botão de pesquisa
        self.realizar_pesquisa = Entry(self.janela, width=50) 
        self.realizar_pesquisa.focus_set()
        try:
            self.imagem = Image.open(r'imagens/download.png')
            self.imagem = self.imagem.resize((30, 30))
            self.foto= ImageTk.PhotoImage(self.imagem)
        except:
            self.foto = None
        try:
            self.label = Label(self.janela, width=49)
            self.imagem = Image.open(r'imagens/voltar.png')
            self.imagem = self.imagem.resize((30, 30))
            self.imagem_voltar = ImageTk.PhotoImage(self.imagem)
        except:
            self.imagem_voltar = None
        

        self.lupa = Label(self.janela, image=self.foto, cursor="hand2")
        

        #frames
        self.frame_superior = Frame(self.janela, bg='black')
        self.frame_de_resultado = Frame(self.janela, bg='blue', width=300, height=300)
        self.pontinhos_do_frame = Label(self.frame_superior, text="⋮", width=2, bg="black", fg="white",
        cursor="hand2", font=("Arial", 20))
        self.consulta_de_estoque = Label(self.frame_superior, text='Consultar estoque',
        width=20, height=2, fg="white", bg="black", font=("Arial", 12, "bold"))

        #outros
        self.voltar = Button(self.frame_superior, image=self.imagem_voltar, command=self.tela_inicial).pack(side="left")

            #resultado da pesquisa
        self.descrição = Label(self.frame_de_resultado, text="", bg='blue', fg='white',
        font=("Arial", 20, "bold"))
        self.codigo_interno = Label(self.frame_de_resultado, text="", bg='blue', fg='white')
        self.ean = Label(self.frame_de_resultado, text="", bg='blue', fg='white', font=("Arial", 10, "bold"))
        self.quantidade = Label(self.frame_de_resultado, text="", bg='blue', fg='white')

        
        #menu
        self.menu = Menu(self.janela, tearoff=0)
        self.menu.add_command(label="Login", command=lambda: print("login"))
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=self.fechar_programa)


        #Posicionando os elementos da tela
            #grid()
        self.realizar_pesquisa.grid(row=4, column=1, padx=50, pady=7)
        self.frame_de_resultado.grid(row=5, column=1)
        self.frame_superior.grid(row=1, column=1, sticky="ew")
        self.lupa.place(x=360, y=39)
        
            #place()
        self.descrição.place(x=20, y=30)
        self.consulta_de_estoque.place(x=100, y=-2)
        self.codigo_interno.place(x=20, y=80)
        self.ean.place(x=20, y=100)
        self.quantidade.place(x=180, y=100)

            #pack()
        self.pontinhos_do_frame.pack(side="right")


        #Pegar eventos

        self.lupa.bind("<Button-1>", lambda e: Thread(target=self.consultar).start())
        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)
        self.realizar_pesquisa.bind("<Return>", lambda e: Thread(target=self.consultar).start())
        
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
        self.ean.config(text="")
        self.codigo_interno.config(text="")
        self.quantidade.config(text="")
        asyncio.run(self.Consultar_Produtos())    

    async def Consultar_Produtos(self):
        try:
            consultar = consulta()
            dados = self.realizar_pesquisa.get()
            pesquisar = await consultar.Consultar_Estoque(consulta=dados)
            if pesquisar[0:15] == "de con":
                self.descrição.config(text="erro de conexão", font=("Arial", 20, 'bold') )
            else:
                self.descrição.config(text=pesquisar[0], font=("Arial", 20, "bold"))
                if pesquisar[1] == "<":
                    interno = "000000"
                else:
                    interno = pesquisar[1]

                self.codigo_interno.config(text=interno)
                self.ean.config(text=pesquisar[2])
                self.quantidade.config(text=f"Quantidade: {pesquisar[3]}", font=("Arial", 12, "bold"))
                Frame(self.frame_de_resultado, height=2, width=350, bg='black').place(x=-10, y=130)
                print(pesquisar)
        except TypeError as e:
            self.descrição.config(text="Nenhum ítem encontrado!")
            

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
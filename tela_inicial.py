from tkinter import *
import consultar_estoque
import cadastrar_produtos
from Funções import Graficos

class Tela:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Gerenciador de estoque")
        self.linha_divisória2 = Frame(self.janela, height=2, bg="black")
        self.linha_divisória3 = Frame(self.janela, height=2, bg="black")


        #configurações da tela
            #Tamanho da janela
        largura_da_janela = self.janela.winfo_screenwidth()
        altura_da_janela = self.janela.winfo_screenheight()
        janela_width = 250
        janela_height = 250
        x = (largura_da_janela - janela_width) // 2
        y = (altura_da_janela - janela_height) // 2
          #Configuração da janela
        self.janela.geometry(f'{janela_width}x{janela_height}+{x}+{y}')
        self.janela.resizable(False, False)


        #elementos da tela
        self.consulta_de_estoque = Label(self.janela, text='Consultar estoque', cursor="hand2", width=20, height=2)
        Frame(self.janela, height=2, bg='black').grid(row = 3, column=1, sticky="ew")
        self.cadastro_de_produtos = Label(self.janela, text='Cadastrar produtos', cursor="hand2", width=20, height=2) 
        Frame(self.janela, height=2, bg='black').grid(row = 5, column=1, sticky="ew")  
        self.movimentações_de_estoque = Label(self.janela, text="Movimentações de estoque", 
        cursor="hand2", width=20, height=2)
        Frame(self.janela, height=2, bg='black').grid(row = 7, column=1, sticky="ew")
        self.logistica = Label(self.janela, text="Logística", cursor="hand2", width=20, height=2)
        Frame(self.janela, height=2, bg='black').grid(row = 9, column=1, sticky="ew")
        

        #frames
        self.frame_superior = Frame(self.janela, bg='black')
        self.pontinhos_do_frame = Label(self.frame_superior, text="⋮", width=2, bg="black", fg="white", cursor="hand2")
        
        #menu
        self.menu = Menu(self.janela, tearoff=0)
        self.menu.add_command(label="Login", command=lambda: print("login"))
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=lambda: print("Sair"))


        #Posicionando os elementos da tela
        self.consulta_de_estoque.grid(row=2, column=1, padx=50, pady=7)
        self.cadastro_de_produtos.grid(row=4, column=1, padx=50, pady=7)
        self.movimentações_de_estoque.grid(row=6, column=1, padx=10, pady=7)
        self.logistica.grid(row=8, column=1, padx=10, pady=7)
        self.frame_superior.grid(row=1, column=1, sticky="ew")
        self.pontinhos_do_frame.pack(side="right")


        #Pegar eventos
        self.consulta_de_estoque.bind("<Button-1>", self.Consultar_Estoque)
        self.cadastro_de_produtos.bind("<Button-1>", self.Cadastrar_produtos)
        self.movimentações_de_estoque.bind("<Button-1>", self.Movimentações)
        self.logistica.bind("<Button-1>", self.Logística)
        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)

    def fechar_programa(self):
        self.janela.quit()
        self.janela.destroy()

    def Consultar_Estoque(self, event):
        print("Consultar")
        self.janela.withdraw()
        tela_principal = Toplevel(self.janela)
        tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        consultar_estoque.Tela(tela_principal)

    def Cadastrar_produtos(self, event):
        print("Cadastrar")
        self.janela.withdraw()
        tela_principal = Toplevel(self.janela)
        tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        cadastrar_produtos.Tela(tela_principal)

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
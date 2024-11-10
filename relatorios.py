from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from connection_with_db import consulta
import asyncio
from threading import Thread
import tela_inicial
import re
import pandas as pd
from cadastrar_categoria import janela
class Tela: 
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("relatorios")
        self.janela.configure(bg="lightblue")

        #configurações da tela
            #Tamanho da janela
        largura_da_janela = self.janela.winfo_screenwidth()
        altura_da_janela = self.janela.winfo_screenheight()
        janela_width = 600
        janela_height = 600
        x = (largura_da_janela - janela_width) // 2
        y = (altura_da_janela - janela_height) // 2
        #Configuração da janela
        self.janela.geometry(f'{janela_width}x{janela_height}+{x}+{y}')
        self.janela.resizable(False, False)

        #elementos da tela
        self.label = Label(self.janela, width=77)
        self.relatorio = Button(self.janela, text="Relatório", bg="lightblue", fg='black', command=self.run_gerar_relatorio)
        self.label1 = Label(self.janela, text="", bg="lightblue")
        self.label1.place(x=180, y=300)

        try:
            
            self.imagem = Image.open(r'imagens/voltar.png')
            self.imagem = self.imagem.resize((30, 30))
            self.imagem_voltar = ImageTk.PhotoImage(self.imagem)
        except:
            self.imagem_voltar = None
        

        #frames
        self.frame_superior = Frame(self.janela, bg='black')
        self.pontinhos_do_frame = Label(self.frame_superior, text="⋮", width=2, bg="black", fg="white",
        cursor="hand2", font=("Arial", 20))
        self.cadastrar_produtos = Label(self.frame_superior, text='Gerar relatorios',
        width=20, height=2, fg="white", bg="black", font=("Arial", 12, "bold")).place(x=200, y=2)

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
        self.relatorio.place(x=240, y=250)


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

    def run_gerar_relatorio(self):
        Thread(target=lambda: asyncio.run(self.gerar_relatorio())).start()

    def validação(self, P, max, preço=False):
        if len(P) <= int(max) and re.match(r"^\d*$", P):
            return True
        else:
            return False

    async def gerar_relatorio(self):
        consultar = consulta()
        self.label1.config(text="Carregando...")
        
        gerar = await consultar.relatorio()
        self.label1.config(text=gerar)

        
    def Opções(self, event):
        self.menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    tela = Tk()
    Tela(tela)
    tela.mainloop()
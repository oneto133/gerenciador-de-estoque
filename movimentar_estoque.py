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
        self.janela.title("Movimentar")
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
        self.código_interno = Label(self.janela, text="Código interno", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=40)
        self.código_interno_entry = Entry(self.janela, width=20, highlightcolor='black', validate='key',
        validatecommand=(self.janela.register(self.validação), '%P', 6))

        self.numero_do_pedido = Label(self.janela, text="Número do Pedido", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=180, y=40)
        self.numero_do_pedido_entry = Entry(self.janela, width=20, highlightcolor='black',
        validate='key', validatecommand=(self.janela.register(self.validação), '%P', 11))
        self.quantidade = Label(self.janela, text="Quantidade", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=360, y=40)
        self.quantidade_entry = Entry(self.janela, width=20, highlightcolor='black', validate='key', validatecommand=(self.janela.register(self.validação), '%P', 5))
        self.categoria = Label(self.janela, text="Categoria", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=210, y=110)
        self.categoria_entry = ttk.Combobox(self.janela, width=18, values=["Faturamento"])
        self.observações = Label(self.janela, text="Obs.", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=200)
        self.observações_texto = Text(self.janela, width=70, height=8)
        self.button = Button(self.janela, text='Movimentar', command=self.run_movimentar_estoque,
        font=('Arial', 13, 'bold')).place(x=250, y=400)
        self.Carregando = Label(self.janela, text="", bg="lightblue")
        self.Carregando.place(x=250, y=370)

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
        self.cadastrar_produtos = Label(self.frame_superior, text='Movimentar Produtos',
        width=20, height=2, fg="white", bg="black", font=("Arial", 12, "bold"))

        #outros
        self.voltar = Button(self.frame_superior, image=self.imagem_voltar, command=self.tela_inicial).pack(side="left")
  
        #menu
        self.menu = Menu(self.janela, tearoff=0)
        self.menu.add_command(label="Login", command=self.abrir_tela_de_login)
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=self.fechar_programa)

        #Posicionando os elementos da tela
            #grid()

        self.label.grid(row=1, column=1, padx=30)
        self.frame_superior.grid(row=1, column=1, sticky="ew")

            #place()
        self.código_interno_entry.place(x=5, y=60)
        self.numero_do_pedido_entry.place(x=180, y=60)
        self.quantidade_entry.place(x=360, y=60)
        self.observações_texto.place(x=5, y=220)
        self.categoria_entry.place(x=180, y=130)

            #pack()
        self.pontinhos_do_frame.pack(side="right")
        #Pegar eventos
        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)

    def abrir_tela_de_login(self):
        from Tela_login import Tela_De_Login
        self.janela.withdraw()
        tela_principal = Toplevel(self.janela)
        tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        Tela_De_Login(tela_principal)

    def fechar_programa(self):
        self.janela.quit()
        self.janela.destroy()
    
    def tela_inicial(self):
        self.janela.withdraw()
        self.tela_principal = Toplevel(self.janela)
        self.tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        tela_inicial.Tela(self.tela_principal)  

    def run_movimentar_estoque(self):
        Thread(target=lambda: asyncio.run(self.movimentar())).start()

    def validação(self, P, max, preço=False):
        if len(P) <= int(max) and re.match(r"^\d*$", P):
            return True
        else:
            return False

    async def movimentar(self):
        self.Carregando.config(text="Carregando...")
        consultar = consulta()
        execução = await consultar.Atualizar_Estoque(quantidade_a_ser_reduzida=int(self.quantidade_entry.get()), codigo_interno=str(self.código_interno_entry.get()),
        número_do_pedido=str(self.numero_do_pedido_entry.get()), tipo=str(self.categoria_entry.get()), observacoes=str(self.observações_texto.get('1.0', END)))
        try:
            valor = execução[201:209]
            if valor == "negativo":
                messagebox.showinfo("Estoque insuficiente","Não pode faturar quantidade que não existe em estoque!")
                self.quantidade_entry.delete(0, END)
        except Exception as e:
            print(e)
            messagebox.showinfo("Movimentado!", f"Abra a aba de relatório para verificar os produtos movimentados para o {self.categoria_entry.get()}")
        try:
            messagebox.showinfo("Movimentado!", f"Abra a aba de relatório para verificar os produtos movimentados para o {self.categoria_entry.get()}")
        except Exception as e:
            print(e)
        self.Carregando.config(text="")
        print(execução)
    def Opções(self, event):
        self.menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    tela = Tk()
    Tela(tela)
    tela.mainloop()
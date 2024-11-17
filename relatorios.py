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
from tkcalendar import DateEntry
from tkinter.ttk import Combobox
from Funções import Funcao
from datetime import datetime
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

        self.movimentação = IntVar()
        self.faturamento = IntVar()
        self.valor_inicial = StringVar()
        self.valor_inicial.set("<Selecionar Caminho>")
        self.tipo_de_movimentação = "Faturamento"
        try:
            
            self.imagem = Image.open(r'imagens/voltar.png')
            self.imagem = self.imagem.resize((30, 30))
            self.imagem_voltar = ImageTk.PhotoImage(self.imagem)
        except:
            self.imagem_voltar = None
        self.elementos_da_tela()

    def elementos_da_tela(self):
        self.label = Label(self.janela, width=-50, bg="black", fg="white")
        #Frames
        self.frame_superior = Frame(self.janela, bg='black')

        #Labels
        self.inicio = Label(self.janela, text="Inicio", bg="lightblue", font=("Arial",10, "bold"))
        self.fim = Label(self.janela, text="Até", bg="lightblue", font=("Arial", 10,"bold"))
        self.código_interno_label = Label(self.janela, text="Código interno", bg="lightblue", font=("Arial",10, "bold"))
        self.usuário_label = Label(self.janela, text="Usuário", bg="lightblue", font=("Arial",10, "bold"))
        self.formato_label = Label(self.janela, text="Formato do Arquivo", bg="lightblue", font=("Arial",10, "bold"))
        self.pontinhos_do_frame = Label(self.frame_superior, text="⋮", width=2, bg="black", fg="white", cursor="hand2", font=("Arial", 20))
        self.cadastrar_produtos = Label(self.frame_superior, text='Gerar Relatórios', width=20, height=2, fg="white", bg="black", font=("Arial", 12, "bold"))
        self.label1 = Label(self.janela, text="", bg="lightblue")

        #Entry
        self.código_interno_entry = Entry(self.janela)
        self.usuário_entry = Entry(self.janela)
        self.destino = Entry(self.janela, textvariable=self.valor_inicial, state="disabled", width=50)

        #Combobox
        self.formato_combobox = Combobox(self.janela, values=("PDF", "CSV", "XLSX"), width=16)
        self.formato_combobox.set("XLSX")

        #Checkbutton
        self.relatorio_faturamento = Checkbutton(self.janela, text="Faturamento", bg="lightblue", variable=self.faturamento, command=self.alternar_caixa_movimentação)
        self.relatorio_movimentação = Checkbutton(self.janela, text="Movimentação entre setores", bg="lightblue", variable=self.movimentação, command=self.alternar_caixa_faturamento)

        #DateEntry
        self.data_inicio = DateEntry(self.janela, date_pattern="dd/mm/yyyy", set_date="")
        self.data_fim = DateEntry(self.janela, date_pattern="dd/mm/yyyy")

        #Botões
        self.voltar = Button(self.frame_superior, image=self.imagem_voltar, command=self.tela_inicial).pack(side="left")
        self.relatorio = Button(self.janela, text="Relatório", bg="green", fg='black', command=self.run_gerar_relatorio, font=("Arial", 10, "bold"), relief="solid", overrelief="solid")
        self.botão_destino = Button(self.janela, text="Procurar destino", overrelief="raised", relief="groove", command=self.abrir_gerenciador)

        #menu
        self.menu = Menu(self.janela, tearoff=0)
        self.menu.add_command(label="Login", command=lambda: print("login"))
        self.menu.add_separator()
        self.menu.add_command(label="Sair", command=self.fechar_programa)
        
        #Grid()
        
        self.label.grid(row=1, column=1, padx=300)
        self.frame_superior.grid(row=1, column=1, sticky="ew")
        
        #place()
        self.cadastrar_produtos.place(x=200, y=2)
        self.código_interno_entry.place(x=160, y=160)
        self.código_interno_label.place(x=5, y=160)
        self.data_fim.place(x=120, y=120)
        self.data_inicio.place(x=5, y=120)
        self.formato_combobox.place(x=160, y=240)
        self.formato_label.place(x=5, y=240)
        self.fim.place(x=120, y=100)
        self.relatorio_faturamento.place(x=5, y=60)
        self.inicio.place(x=5, y=100)
        self.relatorio_movimentação.place(x=160, y=60)
        self.label1.place(x=180, y=500)
        self.relatorio.place(x=260, y=400)
        self.usuário_label.place(x=5, y=200)
        self.usuário_entry.place(x=160, y=200)
        self.botão_destino.place(x=350, y=295)
        self.destino.place(x=30, y=300)
        
        #pack()
        self.pontinhos_do_frame.pack(side="right")

        #Pegar eventos
        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)

    def alternar_caixa_faturamento(self):
        if self.movimentação.get() == 1:
            self.faturamento.set(0)
            self.tipo_de_movimentação = "Movimentação"
    
    def alternar_caixa_movimentação(self):
        if self.faturamento.get() == 1:
            self.movimentação.set(0)
            self.tipo_de_movimentação = "Faturamento"

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
        if self.código_interno_entry.get() == "":
            messagebox.showinfo("Código interno não informado", "Por favor, digite um código interno válido para realizar a consulta,"
            "exemplo de código interno: '123456' ")
        elif self.valor_inicial == "<Selecionar Caminho>":
            messagebox.showerror("Você não selecionou um destino", "Por favor, selecione um destino para continuar com"
            " a geração do relatório")
        
        else:
            data_inicio = str(self.data_inicio.get_date())
            data_fim = str(self.data_fim.get_date())
            tipo_movimentação = self.tipo_de_movimentação
            consultar = consulta()
            self.label1.config(text="Carregando...")
            gerar = await consultar.relatorio(self.abrir, str(self.formato_combobox.get()).lower(), self.código_interno_entry.get(),
            data_inicio, data_fim, tipo_movimentação)
            self.label1.config(text=gerar)

        
    def Opções(self, event):
        self.menu.post(event.x_root, event.y_root)

    def abrir_gerenciador(self):
        funcao = Funcao()
        self.abrir = funcao.abrir_gerenciador_de_arquivos_para_destino()
        
        if self.abrir != "":
            self.valor_inicial.set(self.abrir)
            self.janela.update()


if __name__ == "__main__":
    tela = Tk()
    Tela(tela)
    tela.mainloop()
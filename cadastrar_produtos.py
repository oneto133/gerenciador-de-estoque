from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from connection_with_db import Cadastrar_produtos
import asyncio
from threading import Thread
import tela_inicial
import re
import pandas as pd
from cadastrar_categoria import janela

class Tela: 
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastrar")
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

        df = pd.read_csv(r"csv/combobox.csv", header=None, encoding='latin1')

        # Converter cada coluna para uma lista e armazenar em um dicionário
        colunas = {coluna: df[coluna].astype(str).tolist() for coluna in df.columns}
        self.combobox = []
        # Exibir o resultado
        for indice, lista in colunas.items():
            self.combobox.append(lista)


        #elementos da tela
        self.label = Label(self.janela, width=77)
        self.descrição = Label(self.janela, text="Descrição", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=40)
        self.descrição_entry = Entry(self.janela, width=60, highlightcolor='black')
        self.código_interno = Label(self.janela, text="Código interno", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=80)
        self.código_interno_entry = Entry(self.janela, width=20, highlightcolor='black', validate="key", validatecommand=(self.janela.register(self.validação), '%P', 6))
        self.ean = self.código_interno = Label(self.janela, text="EAN", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=150, y=80)
        self.ean_entry = Entry(self.janela, width=20, highlightcolor='black',
        validate='key', validatecommand=(self.janela.register(self.validação), '%P', 13))
        self.preco = Label(self.janela, text="Preço (un.)", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=120)
        self.preco_entry = Entry(self.janela, width=20, highlightcolor='black',
        validate='key', validatecommand=(self.janela.register(self.Validar_preço), '%P'))
        self.quantidade = Label(self.janela, text="Quantidade em estoque", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=150, y=120)
        self.quantidade_entry = Entry(self.janela, width=20, highlightcolor='black', validate='key', validatecommand=(self.janela.register(self.validação), '%P', 5))
        self.categoria = Label(self.janela, text="Categoria", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=160)
        self.categoria_entry = ttk.Combobox(self.janela, width=20, values=self.combobox)
        self.observações = Label(self.janela, text="Obs.", bg="lightblue", fg='black', font=('Arial', 10, 'bold')).place(x=5, y=300)
        self.observações_texto = Text(self.janela, width=70, height=8)
        Frame(self.janela, width=600, height=2, bg="black").place(x=0, y=213)
        self.localização = Label(self.janela, text="Localização na expedição", bg="lightblue", font=("Roboto", 12, "bold"))
        self.button = Button(self.janela, text='Cadastrar', command=self.run_cadastrar_produtos,
        font=('Arial', 13, 'bold')).place(x=250, y=500)
        self.rua = Label(self.janela, text="Rua", bg="lightblue", font=("Arial", 10, "bold"))
        self.módulo = Label(self.janela, text="Módulo", bg="lightblue", font=("Arial", 10, "bold"))
        self.nível = Label(self.janela, text="Nível", bg="lightblue", font=("Arial", 10, "bold"))
        self.rua_entry = Entry(self.janela, validate='key', validatecommand=(self.janela.register(self.validação), '%P', 2))
        self.módulo_entry = Entry(self.janela, validate='key', validatecommand=(self.janela.register(self.validação), '%P', 2))
        self.nível_entry = Entry(self.janela, validate='key', validatecommand=(self.janela.register(self.validação), '%P', 2))
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
        self.cadastrar_produtos = Label(self.frame_superior, text='Cadastrar Produtos',
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
        self.cadastrar_produtos.place(x=200, y=-2)
        self.descrição_entry.place(x=5, y=60)
        self.código_interno_entry.place(x=5, y=100)
        self.ean_entry.place(x=150, y=100)
        self.preco_entry.place(x=5, y=140)
        self.quantidade_entry.place(x=150, y=140)
        self.observações_texto.place(x=5, y=320)
        self.categoria_entry.place(x=5, y=180)
        self.localização.place(x=200, y=200)
        self.rua.place(x=5, y=230)
        self.módulo.place(x=205, y=230)
        self.nível.place(x=405, y=230)
        self.rua_entry.place(x=5, y=260)
        self.módulo_entry.place(x=205, y=260)
        self.nível_entry.place(x=405, y=260)

            #pack()
        self.pontinhos_do_frame.pack(side="right")

        #Pegar eventos
        self.pontinhos_do_frame.bind("<Button-1>", self.Opções)
        self.categoria_entry.set("Selecionar")
        self.categoria_entry.bind("<<ComboboxSelected>>", self.seleção)
    def abrir_tela_de_login(self):
        from Tela_login import Tela_De_Login
        self.janela.withdraw()
        tela_principal = Toplevel(self.janela)
        tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        Tela_De_Login(tela_principal)

    def seleção(self, event):
        seleção = self.categoria_entry.get()
        if seleção == "Cadastrar+":
            tela_principal = Toplevel(self.janela)
            janela(tela_principal)
            self.categoria_entry.set("Selecionar")
            self.categoria_entry.config(values=self.combobox)
            

    def fechar_programa(self):
        self.janela.quit()
        self.janela.destroy()
    
    def tela_inicial(self):
        self.janela.withdraw()
        self.tela_principal = Toplevel(self.janela)
        self.tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        tela_inicial.Tela(self.tela_principal)  

    def run_cadastrar_produtos(self):
        if len(self.código_interno_entry.get()) < 6:
            messagebox.showwarning("Código interno", "Código interno com digitos insuficientes, tamanho tem que ser de 6")         
        else:
            Thread(target=lambda: asyncio.run(self.cadastrar_produtoss())).start()

    def validação(self, P, max, preço=False):
        if len(P) <= int(max) and re.match(r"^\d*$", P):
            return True
        else:
            return False

    def Validar_preço(self, P):
    # Limita a entrada a números e um único ponto decimal
        if re.match(r"^\d*\.?\d{0,2}$", P):
            # Insere o ponto decimal após os dois primeiros dígitos (ajuste conforme necessário)
            if len(P) == 2 and '.' not in P:
                return P + '.'
            return True 
        else:
            return False

    async def cadastrar_produtoss(self):
        if str(self.código_interno_entry.get())== "" or str(self.ean_entry.get()) == "" or self.descrição_entry.get() == "":
            print("Não cadastrado! campos vazios")
        else:
            self.mensagem = Label(self.janela, text="", bg="lightblue", fg='red')
            self.mensagem.place(x=200, y=450)
            cadastro = Cadastrar_produtos()
            self.mensagem.config(text="Carregando...", width=29)
            cadastrar = await cadastro.inserir_dados(codigo_interno=str(self.código_interno_entry.get()),
            ean=str(self.ean_entry.get()), descrição=str(self.descrição_entry.get()),
            observações=str(self.observações_texto.get('1.0', END)), preco=float(self.preco_entry.get()),
            quantidade=str(self.quantidade_entry.get()), categoria=str(self.categoria_entry.get()), rua=int(self.rua_entry.get()),
            modulo=int(self.módulo_entry.get()), nivel=int(self.nível_entry.get()))
            self.descrição_entry.config(textvariable=(''))
            print(cadastrar)
            messagebox.showinfo("Produto Cadastrado", "Produto cadatrado com sucesso, verifique o estoque para saber se as informações estão corretas...")

    def Opções(self, event):
        self.menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    tela = Tk()
    Tela(tela)
    tela.mainloop()
#Arquivo telalogin.py
from tkinter import *
from PIL import ImageTk, Image
from Funções import Horarios
import connection_with_db as conn
from tela_inicial import Tela
import threading
import asyncio


class Tela_De_Login:
    def __init__(self, janela):
        
        #Configuraçãoes da janela
        self.tela = janela
        self.tela.withdraw()
        self.senha = 0
        self.carregado = False
        self.abrir_tela_de_login()


    def abrir_tela_de_login(self):    
        self.janela = Toplevel(self.tela)
        self.janela.title("Login")
        try:
            self.janela.iconbitmap(r'imagens/icone.ico')
        except:
            print("Imagem não encontrada")
            self.janela.iconbitmap(None)
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        
        # Obter a largura e altura da janela
        largura_da_janela = self.janela.winfo_screenwidth()
        altura_da_janela = self.janela.winfo_screenheight()
        
        # Calcular as coordenadas para centralizar a janela
        janela_width = 250
        janela_height = 200
        x = (largura_da_janela - janela_width) // 2
        y = (altura_da_janela - janela_height) // 2
        
        # Configuração da janela
        self.janela.geometry(f'{janela_width}x{janela_height}+{x}+{y}')
        self.janela.resizable(False, False)
        
        self.Elementos_Da_Tela()


    def Mostrar_Senha(self):
        if self.verificar_senha.get():
            self.Password_Entry.config(show='')
        else:
            self.Password_Entry.config(show='*')


    def mover_foco(self, event):
        self.Password_Entry.focus_set()
        self.Mensagem_de_alerta['text'] = 'Digite uma senha.'
        
    def Pegar_dados(self, event):
        hora = Horarios()
        self.inicio = hora.hora_atual()
        self.Mensagem_de_alerta['text'] = "Carregando..."
        threading.Thread(target=self.comparacao).start()

    def abre_a_tela_principal(self):
        self.tela_principal = Toplevel(self.janela)
        self.tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        Tela(self.tela_principal)
    

    def fechar_programa(self):
        self.janela.quit()
        self.janela.destroy()

    async def consultar_banco(self, dado):
        consulta = conn.Query()
        senha = await consulta.consultar_senha_por_usuario(dado)
        self.carregado = True
        print(senha)
        return senha

        
    def clicar_botao(self):
        dado = self.Users_Entry.get()
        if dado:
            self.senha = asyncio.run(self.consultar_banco(dado))


    def comparacao(self):
        if self.carregado:
            #hora = Horarios()
            #fim = hora.hora_atual() - self.inicio
            #print(fim)
            if self.Password_Entry.get():
                if self.senha == self.Password_Entry.get():
                    self.janela.withdraw()
                    self.abre_a_tela_principal()
                else:
                    self.Mensagem_de_alerta['text'] = 'Senha incorreta!'
            else:
                self.Mensagem_de_alerta['text'] = 'Digite uma senha!' 
        else:
            self.janela.after(200, self.comparacao)

     
#Essa função foi retirada por problemas de implementação, logo será acrescentada na pasta de funções, um dia pode ser útil...
    def animacao(self, contador=22):
        pontos = "." * (contador % 4)  # Alterna entre '', '.', '..', '...'
        self.carregando = Label(self.janela, text="", font=("Arial", 12, "bold"), bg="gray", fg="white")
        self.carregando.place(relx=0.5, rely=0.5, anchor="center")
        self.carregando['text'] = f"Carregando{pontos}"
        contador += 1

        if contador < 25:
            self.janela.after(200, self.animacao, contador)
            self.carregando['text'] = ""
 

    def Elementos_Da_Tela(self):
        #Labels
        self.Login = Label(self.janela, text='Login', font=('Sixtyfour Convergence', 16, 'bold')).place(x=60, y=5)
        self.Users = Label(self.janela, text='Usuário:', font=('Arial', 11, 'bold')).place(x=30, y=50)
        self.Password = Label(self.janela, text='Senha:', font=('Arial', 11, 'bold')).place(x=30, y=100)
        self.imagem = Image.open(r'imagens/icone.ico')
        self.imagem = self.imagem.resize((60, 30))
        self.foto= ImageTk.PhotoImage(self.imagem)
        self.rotulo = Label(self.janela, image=self.foto)
        self.rotulo.place(x=140, y=5)
        #Mostrar senha
        self.verificar_senha = BooleanVar()
        self.Checkbutton = Checkbutton(self.janela, text='Mostrar senha', variable=self.verificar_senha, command=self.Mostrar_Senha)
        self.Mensagem_de_alerta = Label(self.janela, text='', font=("Arial", 8, "bold"), fg='red')

        #Entradas de dados    
        self.Users_Entry = Entry(self.janela)
        self.janela.update()
        self.Password_Entry = Entry(self.janela, show='*')

        #Posicionamento
        self.Users_Entry.place(x=100, y=53)
        self.Password_Entry.place(x=100, y=103)
        self.Mensagem_de_alerta.place(x= 95, y= 143)
        #self.rotulo.place(x=140, y= 5)
        self.Checkbutton.place(x=95, y = 125)

        #Botões
        self.Botão_Login = Button(self.janela, text='Entrar', fg='white', bg='blue', relief='raised',
         width=9, height=1, command=self.comparacao).place(x=95, y=160)

        #Bind
        self.Users_Entry.bind("<Return>", self.mover_foco)
        self.Password_Entry.bind("<Return>", self.Pegar_dados)
        self.Users_Entry.bind("<Leave>", lambda e: threading.Thread(target=self.clicar_botao).start() if self.Users_Entry.get() else None)


 


if __name__ == '__main__':
    janela = Tk()
    Tela_De_Login(janela)
    janela.mainloop()
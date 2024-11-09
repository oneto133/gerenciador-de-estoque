from tkinter import *
from tkinter import messagebox

class janela:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Cadastrar categoria")
            #Tamanho da janela
        largura_da_janela = self.janela.winfo_screenwidth()
        altura_da_janela = self.janela.winfo_screenheight()
        janela_width = 200
        janela_height = 100
        x = (largura_da_janela - janela_width) // 2
        y = (altura_da_janela - janela_height) // 2
          #Configuração da janela
        self.janela.geometry(f'{janela_width}x{janela_height}+{x}+{y}')
        self.janela.resizable(False, False)


        categoria = Label(self.janela, text="Categoria").pack()
        self.categoria_entry = Entry(self.janela)
        self.categoria_entry.focus_set()
        self.categoria_entry.pack()
        botão = Button(self.janela, text="Cadastrar", command=self.cadastrar).pack()
        self.label = Label(self.janela, text="")
        self.label.pack()

    def cadastrar(self):
        with open(r'csv/combobox.csv', 'a') as arq:
            if self.categoria_entry.get() == "":
                self.label.config(text="Digite um categoria")
            else:
                self.categoria_nova = str(self.categoria_entry.get()).capitalize()
                arq.write(f',{self.categoria_nova}')
                self.label.config(text='Cadastrado com sucesso!')
                self.fechar_e_voltar()

    def fechar_e_voltar(self):
        from cadastrar_produtos import Tela
        self.janela.withdraw()
        self.tela_principal = Toplevel(self.janela)
        self.tela_principal.protocol("WM_DELETE_WINDOW", self.fechar_programa)
        Tela(self.tela_principal)
        messagebox.showinfo("Voltando a tela anterior", f"{self.categoria_nova} cadastrado com sucesso! Feche e reinicie o programa")

    def fechar_programa(self):
        self.janela.quit()
        self.janela.destroy()




if __name__ == "__main__":
    tela = Tk()
    janela(tela)
    tela.mainloop()

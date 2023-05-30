from tkinter import *

janela = Tk()

class Interface:
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames()
        self.botoes()
        self.textos()
        self.campos()
        janela.mainloop()

    def tela(self):
        self.janela.title('Cadastro de Clientes')
        self.janela.configure(background='#003060')
        self.janela.geometry('1500x900')
        self.janela.resizable(True, True) #permitir que o usuário diminua a tela, tanto verticalmente como horizontalmente.

    def frames(self):
        self.frame1 = Frame(self.janela, bd=4, bg='white', highlightbackground='black', highlightthickness=3)
        self.frame1.place(relx=0.57,rely=0.05, relheight=0.9, relwidth=0.4)

        self.frame2 = Frame(self.janela, bd=4, bg='#c0c0c0', highlightbackground='black', highlightthickness=3)
        self.frame2.place(relx=0.57,rely=0.89, relheight=0.07, relwidth=0.4)

    def botoes(self):
        self.botao_limpar = Button(self.frame2, text='Limpar')
        self.botao_limpar.place(relx=0.05,rely=0.3,relwidth=0.3, relheight=0.5)

        self.botao_buscar = Button(self.frame2, text='Buscar')
        self.botao_buscar.place(relx=0.65,rely=0.3,relwidth=0.3, relheight=0.5)  

        self.botao_novo = Button(self.janela, text='Novo')
        self.botao_novo.place(relx=0.12,rely=0.87,relwidth=0.1, relheight=0.03)

        self.botao_deletar = Button(self.janela, text='Deletar')
        self.botao_deletar.place(relx=0.28,rely=0.87,relwidth=0.1, relheight=0.03)

    def textos(self):
        self.texto_nome = Label(self.janela, text='Nome Completo')
        self.texto_nome.place(relx=0.01,rely=0.05)

        self.texto_cpf = Label(self.janela, text='CPF')
        self.texto_cpf.place(relx=0.01,rely=0.13)

    def campos(self):
        self.campo_nome = Entry(self.janela)
        self.campo_nome.place(relx=0.01,rely=0.08, relwidth=0.25, relheight=0.03)
        
        self.campo_cpf = Entry(self.janela)
        self.campo_cpf.place(relx=0.01, rely=0.16, relwidth=0.25, relheight=0.03)

Interface()
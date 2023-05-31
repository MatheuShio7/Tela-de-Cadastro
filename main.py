from tkinter import *
from tkinter import ttk
import sqlite3

janela = Tk()

class Funcoes:
    def limpar_campos(self):
        self.campo_nome.delete(0, END)
        self.campo_cpf.delete(0, END)
        self.campo_telefone.delete(0, END)
        self.campo_cidade.delete(0, END)

    def conectar_bd(self):
        self.conectar = sqlite3.connect('clientes.bd')
        self.cursor = self.conectar.cursor(); print('Conectando ao banco de dados')
    
    def desconectar_bd(self):
        self.conectar.close(); print('Desconectando do banco de dados')

    def montar_tabela(self):
        self.conectar_bd()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                cpf INTEGER PRIMERY KEY,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20),
                cidade CHAR(40)
            );
        ''')
        self.conectar.commit(); print('Banco de dados criado')
        self.desconectar_bd()

    def cadastrar(self):
        self.cpf = self.campo_cpf.get()
        self.nome = self.campo_nome.get()
        self.telefone = self.campo_telefone.get()
        self.cidade = self.campo_cidade.get()
        self.conectar_bd()

        self.cursor.execute(''' INSERT INTO clientes (cpf, nome_cliente, telefone, cidade)
            VALUES (?, ?, ?, ?)''', (self.cpf, self.nome, self.telefone, self.cidade))
        self.conectar.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpar_campos()

    def select_lista(self):
        self.lista_clientes.delete(*self.lista_clientes.get_children())
        self.conectar_bd()
        lista = self.cursor.execute(''' SELECT cpf, nome_cliente, telefone, cidade FROM clientes
            ORDER BY nome_cliente ASC; ''')
        for i in lista:
            self.lista_clientes.insert('', END, values=i)
        self.desconectar_bd()

class Interface(Funcoes):
    def __init__(self):
        self.janela = janela
        self.tela()
        self.frames()
        self.botoes()
        self.textos()
        self.campos()
        self.lista()
        self.montar_tabela()
        self.select_lista()
        janela.mainloop()

    def tela(self):
        self.janela.title('Cadastro de Clientes')
        self.janela.configure(background='#003060')
        self.janela.geometry('1500x900')
        self.janela.resizable(True, True) #permitir que o usuário diminua a tela, tanto verticalmente como horizontalmente.

    def frames(self):
        self.frame1 = Frame(self.janela, bg='white', highlightbackground='black', highlightthickness=3)
        self.frame1.place(relx=0.57,rely=0.05, relheight=0.9, relwidth=0.4)

        self.frame2 = Frame(self.janela, bg='#c0c0c0', highlightbackground='black', highlightthickness=3)
        self.frame2.place(relx=0.57,rely=0.89, relheight=0.07, relwidth=0.4)

    def botoes(self):
        self.botao_deletar = Button(self.frame2, text='Deletar', bd=4, bg='#003060', fg='white', font=('verdana', 12))
        self.botao_deletar.place(relx=0.05,rely=0.2,relwidth=0.3, relheight=0.6)

        self.botao_buscar = Button(self.frame2, text='Buscar', bd=4, bg='#003060', fg='white', font=('verdana', 12))
        self.botao_buscar.place(relx=0.65,rely=0.2,relwidth=0.3, relheight=0.6)  

        self.botao_novo = Button(self.janela, text='Novo', bd=4, bg='#007500', fg='white',font=('verdana', 12), command=self.cadastrar)
        self.botao_novo.place(relx=0.18,rely=0.5,relwidth=0.07, relheight=0.03)

        self.botao_limpar = Button(self.janela, text='Limpar', bd=4, bg='#750000', fg='white', font=('verdana', 12), command=self.limpar_campos)
        self.botao_limpar.place(relx=0.3,rely=0.5,relwidth=0.07, relheight=0.03)

    def textos(self):
        self.texto_nome = Label(self.janela, text='Nome Completo:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_nome.place(relx=0.15,rely=0.17)

        self.texto_cpf = Label(self.janela, text='CPF:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_cpf.place(relx=0.15,rely=0.25)

        self.texto_telefone = Label(self.janela, text='Telefone:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_telefone.place(relx=0.15,rely=0.33)

        self.texto_cidade = Label(self.janela, text='Cidade:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_cidade.place(relx=0.15,rely=0.41)

    def campos(self):
        self.campo_nome = Entry(self.janela, font=('verdana', 10))
        self.campo_nome.place(relx=0.15,rely=0.20, relwidth=0.25, relheight=0.03)
        
        self.campo_cpf = Entry(self.janela, font=('verdana', 10))
        self.campo_cpf.place(relx=0.15, rely=0.28, relwidth=0.25, relheight=0.03)

        self.campo_telefone = Entry(self.janela, font=('verdana', 10))
        self.campo_telefone.place(relx=0.15, rely=0.36, relwidth=0.25, relheight=0.03)

        self.campo_cidade = Entry(self.janela, font=('verdana', 10))
        self.campo_cidade.place(relx=0.15, rely=0.44, relwidth=0.25, relheight=0.03)
    
    def lista(self):
        self.lista_clientes = ttk.Treeview(self.frame1, height=3, column=('coluna1', 'coluna2', 'coluna3', 'coluna4'))

        self.lista_clientes.heading('#0', text='')
        self.lista_clientes.heading('#1', text='CPF')
        self.lista_clientes.heading('#2', text='Nome')
        self.lista_clientes.heading('#3', text='Telefone')
        self.lista_clientes.heading('#4', text='Cidade')

        self.lista_clientes.column('#0', width=1)
        self.lista_clientes.column('#1', width=125)
        self.lista_clientes.column('#2', width=125)
        self.lista_clientes.column('#3', width=125)
        self.lista_clientes.column('#4', width=125)
        
        self.lista_clientes.place(relx=0.0001, rely=0.0001, relheight=1, relwidth=1)

        self.barra_rolagem = Scrollbar(self.frame1, orient='vertical')
        self.lista_clientes.configure(yscroll=self.barra_rolagem.set)
        self.barra_rolagem.place(relx=0.0001, rely=0.001, relheight=0.935, relwidth=0.04)

Interface()
from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser

janela = Tk()

class Relatorios:
    def abrir_pdf(self):
        webbrowser.open('cliente.pdf')

    def gerar_relatorio(self):
        self.c = canvas.Canvas('cliente.pdf')

        self.cpfRelatorio = self.campo_cpf.get()
        self.nomeRelatorio = self.campo_nome.get()
        self.telefoneRelatorio = self.campo_telefone.get()
        self.cidadeRelatorio = self.campo_cidade.get()

        self.c.setFont('Helvetica-Bold', 24)
        self.c.drawString(200, 790, 'Ficha do Cliente')

        self.c.setFont('Helvetica-Bold', 18)
        self.c.drawString(50, 700, 'CPF: ')
        self.c.drawString(50, 670, 'Nome: ')
        self.c.drawString(50, 640, 'Telefone: ')
        self.c.drawString(50, 610, 'Cidade: ')

        self.c.setFont('Helvetica', 18)
        self.c.drawString(150, 700, self.cpfRelatorio)
        self.c.drawString(150, 670, self.nomeRelatorio)
        self.c.drawString(150, 640, self.telefoneRelatorio)
        self.c.drawString(150, 610, self.cidadeRelatorio)


        self.c.rect(10, 550, 575, 3, fill=True, stroke=False)

        self.c.rect(30, 500, 535, 1, fill=True, stroke= False)
        self.c.rect(30, 470, 535, 1, fill=True, stroke= False)
        self.c.rect(30, 440, 535, 1, fill=True, stroke= False)
        self.c.rect(30, 410, 535, 1, fill=True, stroke= False)
        self.c.rect(30, 380, 535, 1, fill=True, stroke= False)
        self.c.rect(30, 350, 535, 1, fill=True, stroke= False)
        self.c.rect(30, 320, 535, 1, fill=True, stroke= False)

        self.c.rect(147, 125, 300, 160, fill=False, stroke=True)

        self.c.rect(200, 50, 200, 1, fill=True, stroke=False)
        self.c.setFont('Helvetica', 14)
        self.c.drawString(267, 30, 'Assinatura')

        self.c.showPage()
        self.c.save()
        self.abrir_pdf()

class Funcoes:
    def limpar_campos(self):
        self.campo_code.delete(0, END)
        self.campo_nome.delete(0, END)
        self.campo_cpf.delete(0, END)
        self.campo_telefone.delete(0, END)
        self.campo_cidade.delete(0, END)

    def conectar_bd(self):
        self.conectar = sqlite3.connect('clientes_code.bd')
        self.cursor = self.conectar.cursor(); print('Conectando ao banco de dados')
    
    def desconectar_bd(self):
        self.conectar.close(); print('Desconectando do banco de dados')
    
    def variaveis(self):
        self.code = self.campo_code.get()
        self.cpf = self.campo_cpf.get()
        self.nome = self.campo_nome.get()
        self.telefone = self.campo_telefone.get()
        self.cidade = self.campo_cidade.get()

    def montar_tabela(self):
        self.conectar_bd()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes_code (
                code INTEGER PRIMARY KEY,
                cpf INTEGER,
                nome_cliente CHAR(40) NOT NULL,
                telefone INTEGER(20) NOT NULL,
                cidade CHAR(40)
            );
        ''')
        self.conectar.commit(); print('Banco de dados criado') 
        self.desconectar_bd()
    
    def cadastrar(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute(''' INSERT INTO clientes_code (cpf, nome_cliente, telefone, cidade)
            VALUES (?, ?, ?, ?)''', (self.cpf, self.nome, self.telefone, self.cidade))
        self.conectar.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpar_campos()

    def select_lista(self):
        self.lista_clientes.delete(*self.lista_clientes.get_children())
        self.conectar_bd()
        lista = self.cursor.execute(''' SELECT code, cpf, nome_cliente, telefone, cidade FROM clientes_code
            ORDER BY nome_cliente ASC; ''')
        for i in lista:
            self.lista_clientes.insert('', END, values=i)
        self.desconectar_bd()

    def double_click(self, envent):
        self.limpar_campos()
        self.lista_clientes.selection()

        for n in self.lista_clientes.selection():
            col1, col2, col3, col4, col5 = self.lista_clientes.item(n, 'values')
            self.campo_code.insert(END, col1)
            self.campo_cpf.insert(END, col2)
            self.campo_nome.insert(END, col3)
            self.campo_telefone.insert(END, col4)
            self.campo_cidade.insert(END, col5)

    def deletar_cliente(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute('''DELETE FROM clientes_code WHERE cpf = ? ''', (self.cpf,))
        self.conectar.commit()
        self.desconectar_bd()
        self.limpar_campos()
        self.select_lista()

    def alterar_info(self):
        self.variaveis()
        self.conectar_bd()
        self.cursor.execute(''' UPDATE clientes_code SET cpf = ?, nome_cliente = ?, telefone = ?, cidade = ?
            WHERE code = ?''', (self.cpf, self.nome, self.telefone, self.cidade, self.code))
        self.conectar.commit()
        self.desconectar_bd()
        self.select_lista()
        self.limpar_campos()

class Interface(Funcoes, Relatorios):
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
        self.double_click(Event)
        self.deletar_cliente()
        self.alterar_info()
        self.menus()
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
        self.botao_deletar = Button(self.frame2, text='Deletar', bd=4, bg='#003060', fg='white', font=('verdana', 12), command=self.deletar_cliente)
        self.botao_deletar.place(relx=0.05,rely=0.2,relwidth=0.3, relheight=0.6)

        self.botao_alterar = Button(self.frame2, text='Alterar', bd=4, bg='#003060', fg='white', font=('verdana', 12), command=self.alterar_info)
        self.botao_alterar.place(relx=0.65,rely=0.2,relwidth=0.3, relheight=0.6)  

        self.botao_novo = Button(self.janela, text='Novo', bd=4, bg='#007500', fg='white',font=('verdana', 12), command=self.cadastrar)
        self.botao_novo.place(relx=0.18,rely=0.5,relwidth=0.07, relheight=0.03)

        self.botao_limpar = Button(self.janela, text='Limpar', bd=4, bg='#750000', fg='white', font=('verdana', 12), command=self.limpar_campos)
        self.botao_limpar.place(relx=0.3,rely=0.5,relwidth=0.07, relheight=0.03)

    def textos(self):
        self.texto_codigo = Label(self.janela, text='Cod.:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_codigo.place(relx=0.148,rely=0.09)

        self.texto_nome = Label(self.janela, text='Nome Completo:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_nome.place(relx=0.148,rely=0.17)

        self.texto_cpf = Label(self.janela, text='CPF:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_cpf.place(relx=0.148,rely=0.25)

        self.texto_telefone = Label(self.janela, text='Telefone:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_telefone.place(relx=0.148,rely=0.33)

        self.texto_cidade = Label(self.janela, text='Cidade:', bg='#003060', fg='white', font=('verdana', 12))
        self.texto_cidade.place(relx=0.148,rely=0.41)

    def campos(self):
        self.campo_code = Entry(self.janela, font=('verdana', 10))
        self.campo_code.place(relx=0.15,rely=0.12, relwidth=0.03, relheight=0.03)

        self.campo_nome = Entry(self.janela, font=('verdana', 10))
        self.campo_nome.place(relx=0.15,rely=0.20, relwidth=0.25, relheight=0.03)
        
        self.campo_cpf = Entry(self.janela, font=('verdana', 10))
        self.campo_cpf.place(relx=0.15, rely=0.28, relwidth=0.25, relheight=0.03)

        self.campo_telefone = Entry(self.janela, font=('verdana', 10))
        self.campo_telefone.place(relx=0.15, rely=0.36, relwidth=0.25, relheight=0.03)

        self.campo_cidade = Entry(self.janela, font=('verdana', 10))
        self.campo_cidade.place(relx=0.15, rely=0.44, relwidth=0.25, relheight=0.03)
    
    def lista(self):
        self.lista_clientes = ttk.Treeview(self.frame1, height=3, column=('coluna1', 'coluna2', 'coluna3', 'coluna4', 'coluna5'))

        self.lista_clientes.heading('#0', text='')
        self.lista_clientes.heading('#1', text='Código')
        self.lista_clientes.heading('#2', text='CPF')
        self.lista_clientes.heading('#3', text='Nome')
        self.lista_clientes.heading('#4', text='Telefone')
        self.lista_clientes.heading('#5', text='Cidade')

        self.lista_clientes.column('#0', width=1)
        self.lista_clientes.column('#1', width=50)
        self.lista_clientes.column('#2', width=75)
        self.lista_clientes.column('#3', width=150)
        self.lista_clientes.column('#4', width=100)
        self.lista_clientes.column('#5', width=100)
        
        self.lista_clientes.place(relx=0.0001, rely=0.0001, relheight=1, relwidth=1)

        self.barra_rolagem = Scrollbar(self.frame1, orient='vertical')
        self.lista_clientes.configure(yscroll=self.barra_rolagem.set)
        self.barra_rolagem.place(relx=0.0001, rely=0.001, relheight=0.935, relwidth=0.04)
        self.lista_clientes.bind('<Double-1>', self.double_click)

    def menus(self):
        barra_menu = Menu(self.janela)
        self.janela.config(menu=barra_menu)
        arquivo_menu = Menu(barra_menu)
        arquivo_menu2 = Menu(barra_menu)
        
        def quit(): self.janela.destroy()

        barra_menu.add_cascade(label = 'Opções', menu = arquivo_menu)
        barra_menu.add_cascade(label = 'Relatórios', menu = arquivo_menu2)

        arquivo_menu.add_cascade(label = 'Encerrar o programa', command=quit)
        arquivo_menu2.add_cascade(label = 'Ficha do Cliente', command=self.gerar_relatorio)


Interface()
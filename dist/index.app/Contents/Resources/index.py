import customtkinter as ctk
import sqlite3 as sql
import lancamento

# Função para criar a tabela de usuários se não existir
def criar_tabela_usuario():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL,
        senha TEXT NOT NULL
    )'''
    )
    user.commit()

# Função para verificar a estrutura da tabela
def verificar_tabela():
    cursor.execute("PRAGMA table_info(user)")
    colunas = cursor.fetchall()
    print("Estrutura da tabela 'user':", colunas)

# Conectando ao banco de dados
user = sql.connect('user.db')
cursor = user.cursor()

# Criando a tabela de usuários
criar_tabela_usuario()

# Verificando a estrutura da tabela
verificar_tabela()

# Função para adicionar um novo usuário
def cadastrar_usuario():
    def cadastrar():
        novo_usuario = login.get()
        nova_senha = senha.get()

        # Verifica se o login e a senha não estão em branco
        if novo_usuario.strip() == '' or nova_senha.strip() == '':
            resultado.configure(text='Preencha todos os campos!')
            return

        # Incluindo um novo usuário no banco de dados
        cursor.execute('SELECT * FROM user WHERE login = ? AND senha = ?', (novo_usuario, nova_senha))
        if cursor.fetchone():
            resultado.configure(text='Usuário já cadastrado!')
        else:
            try:
                cursor.execute('INSERT INTO user (login, senha) VALUES (?, ?)', (novo_usuario, nova_senha))
                user.commit()
                resultado.configure(text='Usuário cadastrado com sucesso!')
            except sql.Error as e:
                resultado.configure(text=f'Erro ao cadastrar usuário: {e}')

    # Criando uma nova janela para cadastro de usuário
    cadastrar_janela = ctk.CTkToplevel()
    cadastrar_janela.title('Cadastro de usuário')
    cadastrar_janela.geometry('300x300')

    # Centraliza a janela
    largura = 300
    altura = 320
    largura_tela = cadastrar_janela.winfo_screenwidth()
    altura_tela = cadastrar_janela.winfo_screenheight()
    posx = largura_tela / 2 - largura / 2
    posy = altura_tela / 2 - altura / 2
    cadastrar_janela.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

    # Adiciona os inputs de preenchimento do usuário
    ctk.CTkLabel(cadastrar_janela, text='Login').pack(pady=10)
    login = ctk.CTkEntry(cadastrar_janela)
    login.pack(pady=4)

    ctk.CTkLabel(cadastrar_janela, text='Senha').pack(pady=10)
    senha = ctk.CTkEntry(cadastrar_janela, show='*')
    senha.pack(pady=4)

    # Adiciona o botão para salvar o novo usuário
    ctk.CTkButton(cadastrar_janela, text='Cadastrar'.upper(), command=cadastrar).pack(pady=20)
    resultado = ctk.CTkLabel(cadastrar_janela, text='')
    resultado.pack(pady=4)

def tela_lancamento():
    lancamento.abrir_tela_lancamento()

# Função para fazer o login
def btnLog():
    novoLogin = login.get()
    novaSenha = senha.get()
    cursor.execute('SELECT * FROM user WHERE login = ? AND senha = ?', (novoLogin, novaSenha))
    resultado = cursor.fetchone()  # Obter o resultado do cursor
    if resultado:  # Se houver um resultado, o login foi bem-sucedido
        resultado_label.configure(text=(f'Seja bem-vindo {novoLogin}'))  # Configurar a mensagem de boas-vindas
        janela.destroy()  # Fecha a janela de login
        tela_lancamento()  # Abre a tela de lançamento
    else:  # Senão, exibir mensagem de erro
        resultado_label.configure(text='Login ou senha incorretos. Tente novamente.')

# Janela principal
janela = ctk.CTk()
janela.title('Cadastro de Funcionários'.upper())

# Centraliza a janela
largura = 300
altura = 340
largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()
posx = largura_tela / 2 - largura / 2
posy = altura_tela / 2 - altura / 2
janela.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

# Fonte
fonteL = ctk.CTkFont(family='urw geometric', size=16)

# Label
label = ctk.CTkLabel(janela, text='Empresa XPTO'.upper(), font=fonteL)
label.pack()

# Login
loginT = ctk.CTkLabel(janela, text='Login', font=fonteL)
loginT.pack()
login = ctk.CTkEntry(janela, placeholder_text='Digite o usuário')
login.pack(padx=5, pady=5)

# Senha
senhaT = ctk.CTkLabel(janela, text='Senha', font=fonteL)
senhaT.pack(padx=5, pady=5)
senha = ctk.CTkEntry(janela, placeholder_text='Digite sua senha', show='*')
senha.pack()

# Botão de login
btnLogin = ctk.CTkButton(janela, text='Login'.upper(), command=btnLog)
btnLogin.pack(padx=5, pady=5)
resultado_label = ctk.CTkLabel(janela, text='')
resultado_label.pack(pady=4)

# Checkbox
check = ctk.CTkCheckBox(janela, text='Salvar senha')
check.pack(padx=7, pady=7)

# Botão de novo usuário
novoUsuario = ctk.CTkButton(janela, text='Novo Usuário'.upper(), command=cadastrar_usuario)
novoUsuario.pack(padx=1, pady=8)

# Fechar janela
janela.mainloop()

# Fechar DB
user.close()

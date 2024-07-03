import customtkinter as ctk
from tkcalendar import Calendar
import tkinter as tk
import sqlite3
from tkinter import messagebox
from openpyxl import Workbook

# CONECTA AO BANCO DE DADOS SQlite ou clia se nao existir ainda
conn = sqlite3.connect('lancamentos.db') # nessa linha passa o nome do arquivo db
cursor = conn.cursor()

# vai criar uma tabela se nao existir ainda
cursor.execute('''CREATE TABLE IF NOT EXISTS lancamentos (
                id INTEGER PRIMARY KEY
                AUTOINCREMENT, remetente TEXT, 
                data_emissao TEXT,
                data_vencimento TEXT,
                valor TEXT,
                metodo_pagamento TEXT)''')
conn.commit()

# Centraliza a janela
janelaLancamento = ctk.CTk()
janelaLancamento.title('Lançamento mensal'.upper())
largura = 300
altura = 300
largura_tela = janelaLancamento.winfo_screenwidth()
altura_tela = janelaLancamento.winfo_screenheight()
posx = largura_tela/2 - largura/2
posy = altura_tela/2 - altura/2
janelaLancamento.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

bold_font = ctk.CTkFont(family='urw geometric', size=15, weight='bold')

# Função para gerar o relatório e exportar para Excel
def gerar_relatorio():
    conn = sqlite3.connect('lancamentos.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT remetente, data_emissao, data_vencimento, valor, metodo_pagamento
                      FROM lancamentos''')
    dados = cursor.fetchall()
    conn.close()

    if dados:
        # Cria um novo arquivo Excel
        wb = Workbook()
        ws = wb.active
        ws.append(['Remetente', 'Data de Emissão', 'Data de Vencimento', 'Valor', 'Método de Pagamento'])
        
        # Preenche o arquivo Excel com os dados
        for linha in dados:
            ws.append(linha)
        
        # Salva o arquivo Excel
        wb.save('relatorio.xlsx')
        messagebox.showinfo("Relatório Gerado", "O relatório foi gerado e salvo como relatorio.xlsx.")
    else:
        messagebox.showinfo("Relatório Vazio", "Não há dados para gerar o relatório.")

# função de calendario para entrada de data na emissão de documento
def abrir_calendario(entry):
  def pegar_data():
    data_selecionada = calendario.get_date()
    entry.delete(0, tk.END) # limpa o campo de entrada
    entry.insert(0, data_selecionada) # insere a data selecionada
    calendario_window.destroy()
  
  calendario_window = tk.Toplevel()
  calendario_window.grab_set()
  largura = 250
  altura = 250
  largura_tela = calendario_window.winfo_screenwidth()
  altura_tela = calendario_window.winfo_screenheight()
  posx = largura_tela/2 - largura/2
  posy = altura_tela/2 - altura/2
  calendario_window.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))
  calendario = Calendar(calendario_window, selectmode='day')
  calendario.pack(padx=10, pady=10)
  botao_ok = tk.Button(calendario_window, text='OK', command=pegar_data)
  botao_ok.pack(pady=10)

# Função para formatar o valor como moeda
def formatar_valor(valor_documento):
    def callback(*args):
        valor = var_valor.get()
        valor = valor.replace(".", ",").replace(".", "")
        valor = valor.zfill(3)
        valor = f'{int(valor[:-1]):,}.{valor[-1:]}'
        valor = valor.replace(".", ",")
        var_valor.set(valor)

    var_valor = tk.StringVar()
    var_valor.trace_add("write", callback)
    valor_documento.configure(textvariable=var_valor)
    

def verificar_lancamento_cadastrado(remetente, valor_documento):
    conn = sqlite3.connect('lancamentos.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM lancamentos 
                      WHERE remetente=? AND valor=?''', (remetente, valor_documento))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None

#FUNÇAO PARA SALVAR NO BANCO DE DADOS
def salvar_no_banco(remetente, data_emissao, data_vencimento, valor,
                  metodo_pagamento):
  conn = sqlite3.connect('lancamentos.db')
  cursor = conn.cursor()
  cursor.execute('''INSERT INTO lancamentos (remetente, data_emissao,
                data_vencimento, valor, metodo_pagamento)
                VALUES (?, ?, ?, ?, ?)''', (remetente, data_emissao, 
                                            data_vencimento, valor,
                                            metodo_pagamento))
  conn.commit()
  conn.close()

#BOTAO PARA ADD UM NOVO LANCAMENTO
def botaoAdd():
  # quando cliclar no botao, vai abrir essa tela
  janela_nova = ctk.CTkToplevel()
  janela_nova.title('cadastrar gasto'.upper())
  
  # Centraliza a janela
  largura = 500
  altura = 500
  largura_tela = janela_nova.winfo_screenwidth()
  altura_tela = janela_nova.winfo_screenheight()
  posx = largura_tela/2 - largura/2
  posy = altura_tela/2 - altura/2
  janela_nova.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))
  
  # CAMPO DE REMENTENTE
  label_remetente = ctk.CTkLabel(janela_nova, text='Remetente:'.upper())
  label_remetente.place(x=15, y=15)
  remetente = ctk.CTkEntry(janela_nova, width=300)
  remetente.place(x=12, y=40)
  
  # CAMPO DE CALENDÁRIO DA EMISSAO DO DOCUMENTO
  label_emissao = ctk.CTkLabel(janela_nova, text='Data de emissão:'.upper())
  label_emissao.place(x=15, y=70)
  emissao = ctk.CTkEntry(janela_nova, width=300)
  emissao.place(x=12, y=95)
  
  # CAMPO DE CALENDÁRIO DA VENCIMENTO DO DOCUMENTO
  label_vencimento = ctk.CTkLabel(janela_nova, text='data de vencimento:'.upper())
  label_vencimento.place(x=15, y=125)
  vencimento = ctk.CTkEntry(janela_nova, width=300)
  vencimento.place(x=12, y=150)
  
  # BOTÃO PARA ABRIR O CALENDÁRIO DO CAMPO DE EMISSAO
  botao_calendario_emissao = ctk.CTkButton(janela_nova,
                                  text='Selecionar Data'.upper(), 
                                  command=lambda: abrir_calendario(emissao),
                                  fg_color='#40a240',
                                  hover_color='#466646',
                                  text_color='#000')
  botao_calendario_emissao.place(x=320, y=95)
  
  # BOTÃO PARA ABRIR O CALENDÁRIO DO CAMPO DE VENCIMENTO
  botao_calendario_vencimento = ctk.CTkButton(janela_nova,
                                text='Selecionar data'.upper(),
                                command=lambda: abrir_calendario(vencimento),
                                fg_color='#40a240',
                                hover_color='#466646',
                                text_color='#000')
  botao_calendario_vencimento.place(x=320, y=150)
  
  # CAMPO DE ADD O VALOR DO DOCUMENTO
  label_valor_documento = ctk.CTkLabel(janela_nova, text='Insira o valor do documento:'.upper())
  label_valor_documento.place(x=15, y=180)
  valor_documento = ctk.CTkEntry(janela_nova, width=300)
  valor_documento.place(x=12, y=205)
  
  # Chama a função para formatar o valor como moeda
  formatar_valor(valor_documento)
  
  # CAMPO DE METODO DE PAGAMENTO
  label_metodo_pagamento = ctk.CTkLabel(janela_nova, text='Método de pagameno'.upper())
  label_metodo_pagamento.place(x=15, y=235)
  metodos_pagamento = ['Dinheiro', 'Débito', 'Crédito', 'Boleto', 'Pix']
  metodo_pagamento = ctk.CTkOptionMenu(janela_nova, values=metodos_pagamento,
                                        fg_color='#40a240',
                                        button_hover_color='#466646',
                                        text_color='#000')
  metodo_pagamento.place(x=12, y=265)
  
  #funçao para salvar os dados no banco de dados
  def salvar_dados():
      remetente_val = remetente.get()
      emissao_val = emissao.get()
      vencimento_val = vencimento.get()
      valor_documento_val = valor_documento.get()
      metodo_pagamento_val = metodo_pagamento.get()

      if verificar_lancamento_cadastrado(remetente_val, valor_documento_val):
          # Lançamento já existe, mostrar mensagem
          messagebox.showinfo("Aviso", "Este lançamento já foi cadastrado.")
      else:
          # Lançamento não existe, salvar no banco de dados
          salvar_no_banco(remetente_val, emissao_val, vencimento_val,
                          valor_documento_val, metodo_pagamento_val)
          janela_nova.destroy()
  
  # BOTAO PARA SALVAR O LANÇAMENTO
  salvar_lancamento = ctk.CTkButton(janela_nova, text='Salvar'.upper(),
                        fg_color='#40a240',
                        hover_color='#466646',
                        text_color='#000',
                        command=salvar_dados)
  salvar_lancamento.place(x=200, y=350)

# BOTAO DE NOVO LANÇAMENTO
btnNovo = ctk.CTkButton(janelaLancamento, text='novo'.upper(),
                        fg_color='#40a240',
                        hover_color='#466646',
                        text_color='#000',
                        command=botaoAdd)
btnNovo.pack(padx=10, pady=10)


# BOTAO PARA GERAR RELATORIO MENSAL
btnRelatorio = ctk.CTkButton(janelaLancamento, text='relatório'.upper(),
                        fg_color='#40a240',
                        hover_color='#466646',
                        text_color='#000',
                        command=gerar_relatorio)
btnRelatorio.pack(padx=10, pady=10)

def abrir_tela_lancamento():
  janelaLancamento.mainloop()

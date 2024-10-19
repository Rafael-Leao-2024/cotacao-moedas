from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
from tkinter.filedialog import askopenfilename
import pandas as pd
import numpy as np
from datetime import datetime
import requests 

link = 'https://economia.awesomeapi.com.br/json/all'
resposta = requests.get(link)
dicionario = resposta.json()

# funcoes def 

def pegar_cotacao():
    try:
        moeda = combobox.get()
        data = caledario.get()
        dia = data[:2]
        mes = data[3:5]
        ano = data[-4:]
        link = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/?start_date={ano}{mes}{dia}&end_date={ano}{mes}{dia}"
        cotacao = requests.get(link)
        cotacao_moeda = cotacao.json()
        texto = f'Cotaçao {moeda} em {data} é de R$ {cotacao_moeda[0]["bid"]}'
        texto_cotacao.configure(text=texto, foreground='green')
        print(texto)
    except:
        texto = "Algo deu Errado em Data / Moeda ou Sistema!"
        texto_cotacao.configure(text=texto, foreground='red')
        print(texto)

    

def atualizar_cotacao():
    try:
        dataframe = pd.read_excel(ver_caminho_arquivo.get())

        data_inicial = calendario_data_inicial.get()
        data_final = calendario_data_final.get()

        dia_inicial = data_inicial[:2]
        mes_inicial = data_inicial[3:5]
        ano_inicial = data_inicial[-4:]
        dia_final = data_final[:2]
        mes_final = data_final[3:5]
        ano_final = data_final[-4:]

        moedas = dataframe.iloc[:, 0]

        for moeda in moedas:
            link_data = f"https://economia.awesomeapi.com.br/json/daily/{moeda}-BRL/10?start_date={ano_inicial}{mes_inicial}{dia_inicial}&end_date={ano_final}{mes_final}{dia_final}"
            print(link_data)
            
            requisisao = requests.get(link_data)
            cotacoes = requisisao.json()

            for cotacao in cotacoes:
                timestamp = int(cotacao['timestamp'])
                bid = float(cotacao['bid'])
                data = datetime.fromtimestamp(timestamp)
                data = data.strftime('%d/%m/%Y')
                
                if not data in dataframe.columns:
                    print(data)
                    dataframe[data] = np.nan

                dataframe.loc[dataframe.iloc[:, 0] == moeda, data] = bid


        dataframe.to_excel(ver_caminho_arquivo.get(), index=False)
        label_atualizar_cotacao.configure(text='Arquivo atualizado com sucesso', foreground='green')

    except:
        label_atualizar_cotacao.configure(text='Algo deu errado', foreground='red')

           



def escolher_arquivo():
    caminho_arquivo = askopenfilename(title="Selecione o Arquivo")
    ver_caminho_arquivo.set(caminho_arquivo)
    if caminho_arquivo:
        label_arquivo_selecionado.configure(text=caminho_arquivo, foreground='green')



# print(dicionario)

lista_moedas = list(dicionario.keys())
ano = datetime.now().year

# Criacao da janela e config
janela = tk.Tk()
janela.title('Ferramenta de cotação de moedas')
janela.geometry('900x550')

# Priimeira linha titulo 1
label_cotacao_moeda = Label(text='Cotacao de 1 moeda especifica', borderwidth=2, relief='solid')
label_cotacao_moeda.grid(row=0, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

# linha de selecionar moeda
label_selecionar_moeda = Label(text='selecionar moeda', anchor='e')
label_selecionar_moeda.grid(row=1, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

combobox = ttk.Combobox(values=lista_moedas)
combobox.grid(row=1, column=2, padx=10, pady=10, sticky='nsew') # ok

# linha de selecionar data cotaçao
selecionar_data_cotacao = Label(text='selecionar data cotaçao')
selecionar_data_cotacao.grid(row=2, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

caledario = DateEntry(year=ano, locale='pt_br')
caledario.grid(row=2, column=2, padx=10, pady=10, sticky='nsew')

# Criacao da mensagem Vazia para mostrar a cotacao
texto_cotacao = Label(text='')
texto_cotacao.grid(row=3, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)
  

botao = Button(text='Pegar Cotaçao', command=pegar_cotacao)
botao.grid(row=3, column=2, padx=10, pady=10, sticky='nsew')


# Segunda Parte
# Cotacao de multiplas moedas
label_cotacao_varias_moeda = Label(text='Cotacao de multiplas moedas', borderwidth=2, relief='solid')
label_cotacao_varias_moeda.grid(row=4, column=0, padx=10, pady=10, sticky='nsew', columnspan=3)

# linha cinco com funaco butao e rotulo


label_selecione_arquivo = Label(text='Selecione o arquivo excel', anchor='e')
label_selecione_arquivo.grid(row=5, column=0, padx=10, pady=10, sticky='nsew', columnspan=2)

ver_caminho_arquivo = StringVar()

botao_arquivo = Button(text='Escolher', command=escolher_arquivo)
botao_arquivo.grid(row=5, column=2, padx=10, pady=10, sticky='nsew')

# Linha seis de menagem de caminhos e diretorio

label_arquivo_selecionado = Label(text='Nenhum arquivo selecionado', underline=-1, anchor='e')
label_arquivo_selecionado.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nswe')

# data inicial 
label_data_inicial = Label(text='Data inicial', anchor='e')
label_data_inicial.grid(row=7, column=0, padx=10, pady=10, sticky='nswe')

calendario_data_inicial = DateEntry(year=ano, locale='pt_br')
calendario_data_inicial.grid(row=7, column=1, padx=10, pady=10, sticky='nsew')

# data final
label_data_final = Label(text='Data Final', anchor='e')
label_data_final.grid(row=8, column=0, padx=10, pady=10, sticky='nswe')

calendario_data_final = DateEntry(year=ano, locale='pt_br')
calendario_data_final.grid(row=8, column=1, padx=10, pady=10, sticky='nsew')
# print(data_final.get_date())

# Botao tualizar cotacao


botao_atualizar_cotacao = Button(text='atualizar cotacao', command=atualizar_cotacao)
botao_atualizar_cotacao.grid(row=9, column=0, padx=10, pady=10, sticky='nsew')

label_atualizar_cotacao = Label(text='')
label_atualizar_cotacao.grid(row=9, column=1, columnspan=2, padx=10, pady=10, sticky='nsew')

# Botao fechar janela
botao_fechar = Button(text='Fechar', command=janela.quit)
botao_fechar.grid(row=10, column=2, padx=10, pady=10, sticky='nsew')

janela.mainloop()
print('fim de programa')
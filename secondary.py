import tkinter as tk
from tkinter import messagebox, ttk
from ttkbootstrap.constants import *

import pandas as pd
import matplotlib.pyplot as plt
import ttkbootstrap as bstkk

# Arquivos CSV
CSV_FILE_VEICULOS = "fleet_data.csv"
MOTORISTAS_FILE = "motoristas.csv"
ABASTECIMENTO_FILE = "abastecimentos.csv"

# Função para carregar veículos
def load_vehicles():
    try:
        df = pd.read_csv(CSV_FILE_VEICULOS)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Marca", "Modelo", "Placa", "Quilometragem", "Ano", "Combustível"])
    return df

# Função para carregar motoristas
def load_motoristas():
    try:
        df = pd.read_csv(MOTORISTAS_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Nome", "CNH", "ID_Veiculo"])
    return df

# Função para carregar abastecimentos
def load_abastecimentos():
    try:
        df = pd.read_csv(ABASTECIMENTO_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Veiculo_ID", "Data", "Litros", "Valor"])
    return df

# Função para adicionar um veículo
def add_vehicle():
    marca = entry_marca.get()
    modelo = entry_modelo.get()
    placa = entry_placa.get()
    quilometragem = entry_quilometragem.get()
    ano = entry_ano.get()
    combustivel = entry_combustivel.get()

    if not marca or not modelo or not placa or not quilometragem or not ano or not combustivel:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        quilometragem = float(quilometragem)
        ano = int(ano)
    except ValueError:
        messagebox.showerror("Erro", "Quilometragem deve ser um número e Ano deve ser um inteiro!")
        return

    df = load_vehicles()
    new_id = len(df) + 1
    new_vehicle = pd.DataFrame([[new_id, marca, modelo, placa, quilometragem, ano, combustivel]], columns=["ID", "Marca", "Modelo", "Placa", "Quilometragem", "Ano", "Combustível"])
    df = pd.concat([df, new_vehicle], ignore_index=True)
    df.to_csv(CSV_FILE_VEICULOS, index=False)

    messagebox.showinfo("Sucesso", "Veículo adicionado com sucesso!")
    load_vehicles_into_table()


# Função para excluir um veículo
def delete_vehicle():
    selected_item = vehicle_table.selection()   
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um veículo para remover!")
        return

    vehicle_id = vehicle_table.item(selected_item, 'values')[0]  # ID do veículo selecionado
    df = load_vehicles()
    df = df[df["ID"] != int(vehicle_id)]  # Remover o veículo com o ID selecionado
    df.to_csv(CSV_FILE_VEICULOS, index=False)

    messagebox.showinfo("Sucesso", "Veículo removido com sucesso!")
    load_vehicles_into_table()


# Função para adicionar um motorista
def add_motorista():
    nome = entry_nome.get()
    cnh = entry_cnh.get()
    veiculo_id = entry_veiculo_id.get()

    if not nome or not cnh or not veiculo_id:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    motoristas_df = load_motoristas()
    new_id = len(motoristas_df) + 1
    new_motorista = pd.DataFrame([[new_id, nome, cnh, veiculo_id]], columns=["ID", "Nome", "CNH", "ID_Veiculo"])
    motoristas_df = pd.concat([motoristas_df, new_motorista], ignore_index=True)
    motoristas_df.to_csv(MOTORISTAS_FILE, index=False)

    messagebox.showinfo("Sucesso", "Motorista adicionado com sucesso!")




# Adicionar na tela de cadastro de motoristas (modificar a função show_motorist_screen)

def show_motorist_screen():
    # Limpar widgets existentes
    for widget in root.winfo_children():
        widget.grid_forget()

    # Campo de busca por motorista
    tk.Label(root, text="Buscar Motorista:").grid(row=0, column=0)
    entry_motorista_filtro = tk.Entry(root)
    entry_motorista_filtro.grid(row=0, column=1)

    # Botão para filtrar motoristas
    tk.Button(root, text="Filtrar Motorista", command=lambda: filter_motorist(entry_motorista_filtro.get())).grid(row=1, column=0, columnspan=2, pady=5)

    # Tabela para exibir motoristas (modifique a exibição dos dados de motoristas)
    columns_motorista = ("ID", "Nome", "CNH", "Veículo", "Placa", "Telefone")
    global motorista_table  # Tornar a tabela global
    motorista_table = ttk.Treeview(root, columns=columns_motorista, show="headings")

    # Configuração das colunas da tabela
    for col in columns_motorista:
        motorista_table.heading(col, text=col)

    motorista_table.grid(row=2, column=0, columnspan=2, pady=10)
    
    # Carregar dados na tabela
    load_motorists_into_table()

def load_motorists_into_table():
    # Limpar a tabela antes de recarregar
    for row in motorista_table.get_children():
        motorista_table.delete(row)
    
    # Carregar os motoristas do CSV
    df_motoristas = pd.read_csv(MOTORISTAS_FILE)

    for _, row in df_motoristas.iterrows():
        motorista_table.insert("", "end", values=row.tolist())



def filter_motorist(nome_motorista):
    # Carregar motoristas
    df_motoristas = pd.read_csv(MOTORISTAS_FILE)

    # Filtrar motoristas que contenham o nome digitado (ignorando maiúsculas/minúsculas)
    df_motoristas_filtrados = df_motoristas[df_motoristas['Nome'].str.contains(nome_motorista, case=False)]

    # Limpar a tabela antes de exibir os resultados filtrados
    for row in motorista_table.get_children():
        motorista_table.delete(row)

    for _, row in df_motoristas_filtrados.iterrows():
        motorista_table.insert("", "end", values=row.tolist())

    # Exibir uma mensagem se não encontrar resultados
    if df_motoristas_filtrados.empty:
        messagebox.showinfo("Nenhum resultado", "Nenhum motorista encontrado com esse nome!")



def show_motorist_details():
    selected_item = motorista_table.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Selecione um motorista!")
        return
    
    motorista_id = motorista_table.item(selected_item, 'values')[0]  # ID do motorista
    df_motoristas = pd.read_csv(MOTORISTAS_FILE)
    motorista_info = df_motoristas[df_motoristas['ID'] == int(motorista_id)].iloc[0]

    # Exibir detalhes do motorista
    info_text = f"Nome: {motorista_info['Nome']}\nCNH: {motorista_info['CNH']}\nTelefone: {motorista_info['Telefone']}"
    messagebox.showinfo("Informações do Motorista", info_text)

    # Carregar e exibir o veículo associado
    df_veiculos = pd.read_csv(CSV_FILE_VEICULOS)
    veiculo_info = df_veiculos[df_veiculos['ID'] == motorista_info['Veículo']].iloc[0]

    veiculo_text = f"Veículo: {veiculo_info['Marca']} {veiculo_info['Modelo']}\nPlaca: {veiculo_info['Placa']}\nQuilometragem: {veiculo_info['Quilometragem']}"
    messagebox.showinfo("Informações do Veículo", veiculo_text)


    # Botão para exibir detalhes do motorista
    tk.Button(root, text="Ver Detalhes do Motorista", command=show_motorist_details).grid(row=3, column=0, columnspan=2, pady=5)






# Função para adicionar abastecimento
def add_abastecimento():
    veiculo_id = entry_veiculo_id_abastecimento.get()
    litros = entry_litros.get()
    valor = entry_valor.get()
    data = entry_data.get()

    if not veiculo_id or not litros or not valor or not data:
        messagebox.showerror("Erro", "Preencha todos os campos!")
        return

    try:
        litros = float(litros)
        valor = float(valor)
    except ValueError:
        messagebox.showerror("Erro", "Litros e Valor devem ser números!")
        return

    abastecimentos_df = load_abastecimentos()
    new_id = len(abastecimentos_df) + 1
    new_abastecimento = pd.DataFrame([[new_id, veiculo_id, data, litros, valor]], columns=["ID", "Veiculo_ID", "Data", "Litros", "Valor"])
    abastecimentos_df = pd.concat([abastecimentos_df, new_abastecimento], ignore_index=True)
    abastecimentos_df.to_csv(ABASTECIMENTO_FILE, index=False)

    messagebox.showinfo("Sucesso", "Abastecimento registrado com sucesso!")

# Função para exibir a tela de cadastro de veículos
def show_main_screen():
    # Limpar widgets existentes
    for widget in root.winfo_children():
        widget.grid_forget()

    tk.Label(root, text="Marca:").grid(row=0, column=0)
    global entry_marca
    entry_marca = tk.Entry(root)
    entry_marca.grid(row=0, column=1)

    tk.Label(root, text="Modelo:").grid(row=1, column=0)
    global entry_modelo
    entry_modelo = tk.Entry(root)
    entry_modelo.grid(row=1, column=1)

    tk.Label(root, text="Placa:").grid(row=2, column=0)
    global entry_placa
    entry_placa = tk.Entry(root)
    entry_placa.grid(row=2, column=1)

    tk.Label(root, text="Quilometragem:").grid(row=3, column=0)
    global entry_quilometragem
    entry_quilometragem = tk.Entry(root)
    entry_quilometragem.grid(row=3, column=1)

    tk.Label(root, text="Ano:").grid(row=4, column=0)
    global entry_ano
    entry_ano = tk.Entry(root)
    entry_ano.grid(row=4, column=1)

    tk.Label(root, text="Combustível:").grid(row=5, column=0)
    global entry_combustivel
    entry_combustivel = tk.Entry(root)
    entry_combustivel.grid(row=5, column=1)

    tk.Button(root, text="Adicionar Veículo", command=add_vehicle).grid(row=6, column=0, columnspan=2, pady=5)
    tk.Button(root, text="Remover Veículo", command=delete_vehicle).grid(row=7, column=0, columnspan=2, pady=5)

    # Definindo as colunas do Treeview
    columns_tree = ("ID", "Marca", "Modelo", "Placa", "Quilometragem", "Ano", "Combustível")
    global vehicle_table  # Tornar o vehicle_table global para acessá-lo fora da função
    vehicle_table = ttk.Treeview(root, columns=columns_tree, show="headings")
    
    # Configurar o cabeçalho do Treeview
    for col in columns_tree:
        vehicle_table.heading(col, text=col)
    
    # Exibir a tabela
    vehicle_table.grid(row=8, column=0, columnspan=2, pady=10)

    # Carregar os dados dos veículos na tabela
    load_vehicles_into_table()

# Função para carregar os veículos na tabela
def load_vehicles_into_table():
    for row in vehicle_table.get_children():
        vehicle_table.delete(row)

    df = load_vehicles()
    for _, row in df.iterrows():
        vehicle_table.insert("", "end", values=row.tolist())


# Função para exibir a tela de cadastro de motoristas
def show_motorista_form():
    for widget in root.winfo_children():
        widget.grid_forget()

    tk.Label(root, text="Nome Motorista:").grid(row=0, column=0)
    global entry_nome
    entry_nome = tk.Entry(root)
    entry_nome.grid(row=0, column=1)

    tk.Label(root, text="CNH:").grid(row=1, column=0)
    global entry_cnh
    entry_cnh = tk.Entry(root)
    entry_cnh.grid(row=1, column=1)

    tk.Label(root, text="ID do Veículo:").grid(row=2, column=0)
    global entry_veiculo_id
    entry_veiculo_id = tk.Entry(root)
    entry_veiculo_id.grid(row=2, column=1)

    tk.Button(root, text="Adicionar Motorista", command=add_motorista).grid(row=3, column=0, columnspan=2, pady=5)

# Função para exibir a tela de controle de abastecimento
def show_abastecimento_form():
    for widget in root.winfo_children():
        widget.grid_forget()

    tk.Label(root, text="ID do Veículo:").grid(row=0, column=0)
    global entry_veiculo_id_abastecimento
    entry_veiculo_id_abastecimento = tk.Entry(root)
    entry_veiculo_id_abastecimento.grid(row=0, column=1)

    tk.Label(root, text="Litros:").grid(row=1, column=0)
    global entry_litros
    entry_litros = tk.Entry(root)
    entry_litros.grid(row=1, column=1)

    tk.Label(root, text="Valor:").grid(row=2, column=0)
    global entry_valor
    entry_valor = tk.Entry(root)
    entry_valor.grid(row=2, column=1)

    tk.Label(root, text="Data (DD/MM/AAAA):").grid(row=3, column=0)
    global entry_data
    entry_data = tk.Entry(root)
    entry_data.grid(row=3, column=1)

    tk.Button(root, text="Adicionar Abastecimento", command=add_abastecimento).grid(row=4, column=0, columnspan=2, pady=5)

# Função para gerar relatórios e exportar em CSV
def generate_reports():
    # Aqui podemos gerar os relatórios em PDF/CSV
    pass

# Configurar a janela principal
root = bstkk.Window(themename='superhero')
#root = tk.Tk()
root.title("Gestão de Frota")

# Criar o Menu
menu = tk.Menu(root)
root.config(menu=menu)

menu_veiculos = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Veículos", menu=menu_veiculos)
menu_veiculos.add_command(label="Cadastrar Veículo", command=show_main_screen)

menu_motoristas = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Motoristas", menu=menu_motoristas)
menu_motoristas.add_command(label="Cadastrar Motorista", command=show_motorista_form)

menu_abastecimento = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Abastecimentos", menu=menu_abastecimento)
menu_abastecimento.add_command(label="Registrar Abastecimento", command=show_abastecimento_form)

menu_relatorios = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Relatórios", menu=menu_relatorios)
menu_relatorios.add_command(label="Gerar Relatório", command=generate_reports)

# Inicializar a tela principal de veículos
show_main_screen()

# Iniciar a aplicação
root.mainloop()

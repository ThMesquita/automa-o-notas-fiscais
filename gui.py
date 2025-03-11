import tkinter as tk
from tkinter import filedialog, messagebox
from nfse.downloader import baixar_nfse
from nfse.utils import carregar_dados_excel
import time
import logging
import os
import tempfile
import requests

# Criar um diretório temporário para armazenar o arquivo de log
temp_dir = tempfile.gettempdir()
log_file_path = os.path.join(temp_dir, 'app.log')

# Configurar logging para sobrescrever o arquivo de log a cada execução
logging.basicConfig(filename=log_file_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', filemode='w')

def verificar_login(username, password):
    try:
        response = requests.post('http://127.0.0.1:5000/login', json={"username": username, "password": password})
        if response.status_code == 200 and response.json().get("status") == "success":
            return True
        else:
            return False
    except Exception as e:
        logging.error(f"Erro ao verificar login: {e}")
        return False

def mostrar_tela_principal():
    # Criar a interface gráfica principal
    root = tk.Tk()
    root.title("Baixar NFSe")

    # Seleção do arquivo Excel
    tk.Label(root, text="Arquivo Excel:").grid(row=0, column=0, padx=10, pady=10)
    entrada_arquivo = tk.Entry(root, width=50)
    entrada_arquivo.grid(row=0, column=1, padx=10, pady=10)
    tk.Button(root, text="Selecionar", command=lambda: selecionar_arquivo(entrada_arquivo)).grid(row=0, column=2, padx=10, pady=10)

    # Seleção do diretório de destino
    tk.Label(root, text="Diretório de Destino:").grid(row=1, column=0, padx=10, pady=10)
    entrada_diretorio_destino = tk.Entry(root, width=50)
    entrada_diretorio_destino.grid(row=1, column=1, padx=10, pady=10)
    tk.Button(root, text="Selecionar", command=lambda: selecionar_diretorio_destino(entrada_diretorio_destino)).grid(row=1, column=2, padx=10, pady=10)

    # Botão para iniciar o processo
    tk.Button(root, text="Iniciar Processo", command=lambda: iniciar_processo(entrada_arquivo, entrada_diretorio_destino)).grid(row=2, column=0, columnspan=3, padx=10, pady=20)

    root.mainloop()

def mostrar_tela_login():
    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Usuário:").grid(row=0, column=0, padx=10, pady=10)
    entrada_usuario = tk.Entry(login_window, width=30)
    entrada_usuario.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_window, text="Senha:").grid(row=1, column=0, padx=10, pady=10)
    entrada_senha = tk.Entry(login_window, show="*", width=30)
    entrada_senha.grid(row=1, column=1, padx=10, pady=10)

    def tentar_login():
        username = entrada_usuario.get()
        password = entrada_senha.get()
        if verificar_login(username, password):
            login_window.destroy()
            mostrar_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    tk.Button(login_window, text="Login", command=tentar_login).grid(row=2, column=0, columnspan=2, padx=10, pady=20)

    login_window.mainloop()

def selecionar_arquivo(entrada_arquivo):
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsm *.xlsx")])
    if caminho_arquivo:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, caminho_arquivo)
        logging.info(f"Arquivo selecionado: {caminho_arquivo}")

def selecionar_diretorio_destino(entrada_diretorio_destino):
    caminho_diretorio = filedialog.askdirectory()
    if caminho_diretorio:
        entrada_diretorio_destino.delete(0, tk.END)
        entrada_diretorio_destino.insert(0, caminho_diretorio)
        logging.info(f"Diretório de destino selecionado: {caminho_diretorio}")

def obter_diretorio_download():
    # Tentar detectar a pasta de download padrão do usuário
    caminho_download = os.path.join(os.path.expanduser("~"), "Downloads")
    if os.path.exists(caminho_download):
        return caminho_download
    else:
        messagebox.showerror("Erro", "Não foi possível encontrar a pasta de downloads padrão.")
        logging.error("Não foi possível encontrar a pasta de downloads padrão.")
        return None

def iniciar_processo(entrada_arquivo, entrada_diretorio_destino):
    logging.info("Iniciando o processo...")
    caminho_arquivo = entrada_arquivo.get()
    download_dir = obter_diretorio_download()
    destino_dir = entrada_diretorio_destino.get()

    if not caminho_arquivo or not download_dir or not destino_dir:
        messagebox.showerror("Erro", "Por favor, selecione todos os caminhos necessários.")
        logging.error("Caminhos necessários não foram selecionados.")
        return

    try:
        logging.info(f"Carregando dados do arquivo Excel: {caminho_arquivo}")
        df = carregar_dados_excel(caminho_arquivo)
        total = len(df)
        if total == 0:
            messagebox.showerror("Erro", "O arquivo Excel está vazio ou não contém os dados necessários.")
            logging.error("O arquivo Excel está vazio ou não contém os dados necessários.")
            return

        for i, row in df.iterrows():
            logging.info(f"Processando {i+1}/{total}: {row['Nome']}")
            baixar_nfse(row['CNPJ'], row['Senha'], row['Nome'], row['Valor'], download_dir, destino_dir, row['Descricao'], row['CNPJ_Tomador'], row['Codigo_Tributacao'])
            time.sleep(5)  # Evitar bloqueios no site

        messagebox.showinfo("Concluído", "Processo concluído.")
        logging.info("Processo concluído com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        logging.error(f"Ocorreu um erro: {e}")

# Mostrar a tela de login ao iniciar o programa
mostrar_tela_login()
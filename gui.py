import tkinter as tk
from tkinter import filedialog, messagebox
from nfse.downloader import baixar_nfse
from nfse.utils import carregar_dados_excel
import time
import logging

# Configurar logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def selecionar_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsm")])
    if caminho_arquivo:
        entrada_arquivo.delete(0, tk.END)
        entrada_arquivo.insert(0, caminho_arquivo)
        logging.info(f"Arquivo selecionado: {caminho_arquivo}")

def selecionar_diretorio_download():
    caminho_diretorio = filedialog.askdirectory()
    if caminho_diretorio:
        entrada_diretorio_download.delete(0, tk.END)
        entrada_diretorio_download.insert(0, caminho_diretorio)
        logging.info(f"Diretório de download selecionado: {caminho_diretorio}")

def selecionar_diretorio_destino():
    caminho_diretorio = filedialog.askdirectory()
    if caminho_diretorio:
        entrada_diretorio_destino.delete(0, tk.END)
        entrada_diretorio_destino.insert(0, caminho_diretorio)
        logging.info(f"Diretório de destino selecionado: {caminho_diretorio}")

def iniciar_processo():
    logging.info("Iniciando o processo...")
    caminho_arquivo = entrada_arquivo.get()
    download_dir = entrada_diretorio_download.get()
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
            baixar_nfse(row['CNPJ'], row['Senha'], row['Nome'], row['Valor'], download_dir, destino_dir)
            time.sleep(5)  # Evitar bloqueios no site

        messagebox.showinfo("Concluído", "Processo concluído.")
        logging.info("Processo concluído com sucesso.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")
        logging.error(f"Ocorreu um erro: {e}")

# Criar a interface gráfica
root = tk.Tk()
root.title("Baixar NFSe")

# Seleção do arquivo Excel
tk.Label(root, text="Arquivo Excel:").grid(row=0, column=0, padx=10, pady=10)
entrada_arquivo = tk.Entry(root, width=50)
entrada_arquivo.grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_arquivo).grid(row=0, column=2, padx=10, pady=10)

# Seleção do diretório de download
tk.Label(root, text="Diretório de Download:").grid(row=1, column=0, padx=10, pady=10)
entrada_diretorio_download = tk.Entry(root, width=50)
entrada_diretorio_download.grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_diretorio_download).grid(row=1, column=2, padx=10, pady=10)

# Seleção do diretório de destino
tk.Label(root, text="Diretório de Destino:").grid(row=2, column=0, padx=10, pady=10)
entrada_diretorio_destino = tk.Entry(root, width=50)
entrada_diretorio_destino.grid(row=2, column=1, padx=10, pady=10)
tk.Button(root, text="Selecionar", command=selecionar_diretorio_destino).grid(row=2, column=2, padx=10, pady=10)

# Botão para iniciar o processo
tk.Button(root, text="Iniciar Processo", command=iniciar_processo).grid(row=3, column=0, columnspan=3, padx=10, pady=20)

root.mainloop()
import pandas as pd

def carregar_dados_excel(caminho_arquivo):
    return pd.read_excel(caminho_arquivo)
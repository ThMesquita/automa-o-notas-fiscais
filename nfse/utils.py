import pandas as pd

def carregar_dados_excel(caminho_arquivo):
    # Carregar a primeira planilha do arquivo Excel
    df = pd.read_excel(caminho_arquivo, sheet_name=0)
    
    # Verificar se as colunas necessárias estão presentes
    colunas_necessarias = ['CNPJ', 'Senha', 'Nome', 'Valor', 'Descricao', 'CNPJ_Tomador', 'Codigo_Tributacao']
    for coluna in colunas_necessarias:
        if coluna not in df.columns:
            raise ValueError(f"A coluna necessária '{coluna}' não foi encontrada na planilha Excel.")
    
    # Retornar apenas as colunas necessárias
    return df[colunas_necessarias]
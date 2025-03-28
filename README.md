# Automação de Emissão de NFSe

Este projeto é uma aplicação Python que automatiza o processo de emissão de Notas Fiscais de Serviço Eletrônicas (NFSe) no site oficial da NFSe. Ele utiliza a biblioteca Selenium para interagir com o navegador e preencher os formulários necessários para emitir as notas fiscais.

## Funcionalidades

- **Carregamento de Dados**: Lê os dados de um arquivo Excel contendo informações como CNPJ, senha, nome, valor, descrição, CNPJ do tomador e código de tributação.
- **Automação de Login**: Realiza login automático no site da NFSe utilizando as credenciais fornecidas.
- **Preenchimento de Formulários**: Preenche automaticamente os campos necessários para emitir a NFSe, como data de competência, CNPJ do tomador, descrição do serviço, valor e código de tributação.
- **Download de Arquivos**: Faz o download dos arquivos XML e PDF da nota fiscal emitida e os salva em um diretório especificado.
- **Logs**: Gera logs detalhados do processo para facilitar o rastreamento de erros e auditoria.

## Estrutura do Projeto

- **`gui.py`**: Interface gráfica para o usuário selecionar o arquivo Excel e o diretório de destino, além de iniciar o processo de emissão.
- **`nfse/downloader.py`**: Contém a lógica principal para automação do navegador e emissão das notas fiscais.
- **`nfse/utils.py`**: Funções utilitárias, como o carregamento de dados do arquivo Excel.
- **`nfse/chrome_utils.py`**: Gerenciamento de perfis do Chrome e fechamento de instâncias do navegador.

## Como Usar

1. **Pré-requisitos**:
   - Python 3.8 ou superior.
   - Instalar as dependências listadas no arquivo `requirements.txt`:
     ```bash
     pip install -r requirements.txt
     ```

2. **Configuração**:
   - Certifique-se de que o arquivo Excel contém as colunas necessárias:
     - `CNPJ`
     - `Senha`
     - `Nome`
     - `Valor`
     - `Descricao`
     - `CNPJ_Tomador`
     - `Codigo_Tributacao`

3. **Execução**:
   - Execute o arquivo `main.py`:
     ```bash
     python main.py
     ```
   - Use a interface gráfica para selecionar o arquivo Excel e o diretório de destino.

4. **Resultados**:
   - Os arquivos XML e PDF das notas fiscais emitidas serão salvos no diretório de destino especificado.

## Tecnologias Utilizadas

- **Python**: Linguagem principal do projeto.
- **Selenium**: Automação do navegador.
- **Tkinter**: Interface gráfica.
- **Pandas**: Manipulação de dados do Excel.
- **WebDriver Manager**: Gerenciamento do driver do Chrome.

## Observações

- Certifique-se de que o navegador Google Chrome está instalado na máquina.
- O perfil do Chrome utilizado deve estar configurado corretamente para acessar o site da NFSe.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.

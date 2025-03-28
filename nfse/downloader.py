import os
import time
import shutil
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from nfse.chrome_utils import get_chrome_user_data_dir, get_chrome_profile_dir, fechar_instancias_chrome

# URL do site da NFSe
URL_NFSE = "https://www.nfse.gov.br/EmissorNacional/Login?ReturnUrl=%2fEmissorNacional"

# Obter o diretório do perfil do Chrome automaticamente uma vez
try:
    USER_DATA_DIR = get_chrome_user_data_dir()
    PROFILE_DIR = get_chrome_profile_dir(USER_DATA_DIR)
except EnvironmentError as e:
    print(e)
    fechar_instancias_chrome()
    USER_DATA_DIR = None
    PROFILE_DIR = None

def baixar_nfse(cnpj, senha, nome, valor, download_dir, destino_dir, descricao, cnpj_tomador, codigo_tributacao):
    if USER_DATA_DIR is None or PROFILE_DIR is None:
        print(f"Erro ao obter o diretório do perfil do Chrome para {nome}")
        return

    # Fechar todas as instâncias do Chrome antes de iniciar o WebDriver
    fechar_instancias_chrome()

    # Configurar o WebDriver (Chrome)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)  # Para manter o navegador aberto
    
    options.add_argument(f"user-data-dir={USER_DATA_DIR}")
    options.add_argument(f"profile-directory={PROFILE_DIR}")
    options.add_argument("--no-sandbox")  # Adicionar opção para evitar problemas de sandbox
    options.add_argument("--disable-dev-shm-usage")  # Adicionar opção para evitar problemas de uso de memória compartilhada
    options.add_argument("--disable-extensions")  # Desativar extensões
    options.add_argument("--disable-gpu")  # Desativar GPU (necessário para headless em alguns sistemas)
    options.add_argument("--window-size=1920,1080")  # Definir tamanho da janela

    # Inicializar o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    print(f"Acessando o site da NFSe para {nome}...")
    driver.get(URL_NFSE)
    
    try:
        # Espera explícita para garantir que os elementos estejam presentes
        wait = WebDriverWait(driver, 20)
        cnpj_field = wait.until(EC.presence_of_element_located((By.ID, "Inscricao")))
        senha_field = wait.until(EC.presence_of_element_located((By.ID, "Senha")))
        
        print("Campo CNPJ encontrado:", cnpj_field is not None)
        print("Campo Senha encontrado:", senha_field is not None)
        
        # Usar JavaScript para limpar os campos de login e senha
        driver.execute_script("arguments[0].value = '';", cnpj_field)
        driver.execute_script("arguments[0].value = '';", senha_field)
        
        cnpj_field.send_keys(cnpj)
        senha_field.send_keys(senha)
        
        # Pausa adicional para verificar visualmente se os campos foram preenchidos
        time.sleep(2)
        
        senha_field.send_keys(Keys.RETURN)
        
        time.sleep(2)  # Esperar o login processar
        print(f"Login realizado para {nome}")
        
        # Verificar se o login foi bem-sucedido
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='btnAcesso' and @data-original-title='Nova NFS-e']")))
        except:
            print(f"Erro ao fazer login para {nome}: Senha inválida")
            return
        
        # Clicar no botão "Nova NFS-e"
        botao_nova_nfse = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='btnAcesso' and @data-original-title='Nova NFS-e']")))
        botao_nova_nfse.click()
        print("Botão 'Nova NFS-e' clicado.")
        
        # Preencher a Data de Competência com a data de hoje
        data_competencia = wait.until(EC.presence_of_element_located((By.ID, "DataCompetencia")))
        data_competencia.send_keys(time.strftime("%d/%m/%Y"))
        data_competencia.send_keys(Keys.TAB)
        print("Data de Competência preenchida.")
        
        # Esperar um pouco antes de selecionar o botão de rádio "Brasil"
        time.sleep(2)
        
        botao_brasil = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="Tomador.LocalDomicilio"][value="1"]')))
        driver.execute_script("arguments[0].click();", botao_brasil)
        
        # Esperar 1 segundo antes de preencher o CNPJ do tomador do serviço
        time.sleep(1)
        
        # Preencher o CNPJ do tomador do serviço
        cnpj_tomador_field = wait.until(EC.presence_of_element_located((By.ID, "Tomador_Inscricao")))
        cnpj_tomador_field.send_keys(cnpj_tomador)
        cnpj_tomador_field.send_keys(Keys.TAB)
        print("CNPJ do Tomador do Serviço preenchido.")

        time.sleep(2)
        
        # Clicar no botão "Avançar"
        botao_avancar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(., 'Avançar')]")))
        botao_avancar.click()

        time.sleep(2)
        
        # Selecionar município "São Paulo"
        municipio = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@aria-labelledby='select2-LocalPrestacao_CodigoMunicipioPrestacao-container']")))
        municipio.click()
        input_municipio = driver.find_element(By.XPATH, "//input[@aria-controls='select2-LocalPrestacao_CodigoMunicipioPrestacao-results']")
        input_municipio.send_keys("São Paulo")
        
        for _ in range(5):
            time.sleep(0.5)
            input_municipio.send_keys(Keys.ARROW_DOWN)
        time.sleep(0.5)
        input_municipio.send_keys(Keys.ENTER)
        print("Município 'São Paulo' selecionado.")
        
        # Preencher o Código de Tributação Nacional
        codigo_tributacao_field = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@aria-labelledby='select2-ServicoPrestado_CodigoTributacaoNacional-container']")))
        codigo_tributacao_field.click()
        input_codigo_tributacao = driver.find_element(By.XPATH, "//input[@aria-controls='select2-ServicoPrestado_CodigoTributacaoNacional-results']")
        input_codigo_tributacao.send_keys(codigo_tributacao)
        time.sleep(1)
        input_codigo_tributacao.send_keys(Keys.TAB)
        print("Código de Tributação Nacional preenchido.")
        
        # Esperar um pouco antes de selecionar o botão de rádio "Não"
        time.sleep(1)

        # Selecionar o botão "Não" usando CSS Selector (ou XPath similar)
        botao_nao = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="ServicoPrestado.HaExportacaoImunidadeNaoIncidencia"][value="0"]')))

        # Usar JavaScript para clicar no botão "Não"
        driver.execute_script("arguments[0].click();", botao_nao)
        
        # Adicionar a descrição do serviço
        descricao_servico = wait.until(EC.presence_of_element_located((By.ID, "ServicoPrestado_Descricao")))

        # Limitar o texto ao tamanho máximo de 2000 caracteres
        descricao = descricao[:2000]

        # Enviar a descrição para o campo de texto
        descricao_servico.send_keys(descricao)
        
        # Clicar no botão "Avançar"
        botao_avancar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(., 'Avançar')]")))
        botao_avancar.click()
        print("Botão 'Avançar' clicado.")
        
        # Preencher o campo valor
        campo_valor = wait.until(EC.presence_of_element_located((By.ID, "Valores_ValorServico")))
        
        # Garantir que o valor tenha duas casas decimais
        valor_formatado = f"{float(valor):.2f}"
        campo_valor.send_keys(valor_formatado)
        print(f"Campo valor preenchido com: {valor_formatado}")

        #Botão Não informar
        botao_nao_tributos = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[name="ValorTributos.TipoValorTributos"][value="3"]')))

        # Usar JavaScript para clicar no botão
        driver.execute_script("arguments[0].click();", botao_nao_tributos)

        print("Botão 'Não informar nenhum valor estimado para os Tributos' clicado.")

        # Clicar no botão "Avançar"
        botao_avancar = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(@class, 'btn-primary') and contains(., 'Avançar')]")))
        botao_avancar.click()
        print("Botão 'Avançar' clicado.")
        
        # Clicar no botão "Emitir Nota"
        botao_emitir = wait.until(EC.element_to_be_clickable((By.ID, "btnProsseguir")))
        botao_emitir.click()
        print("Botão 'Emitir Nota' clicado.")
        
        time.sleep(3)  # Esperar o processamento
        
        # Fazer o download dos arquivos XML e PDF
        botao_download_xml = wait.until(EC.element_to_be_clickable((By.ID, "btnDownloadXml")))
        botao_download_xml.click()
        print("Botão 'Baixar XML' clicado.")
        time.sleep(1)  # Esperar o download completar
        botao_download_pdf = wait.until(EC.element_to_be_clickable((By.ID, "btnDownloadDANFSE")))
        botao_download_pdf.click()
        print("Botão 'Baixar DANFSe' clicado.")
        
        time.sleep(2)  # Esperar o download completar
        
        # Renomear e salvar os arquivos
        # Encontrar o arquivo XML baixado
        xml_files = glob.glob(os.path.join(download_dir, "*.xml"))
        if xml_files:
            caminho_download_xml = max(xml_files, key=os.path.getctime)
            caminho_destino_xml = os.path.join(destino_dir, f"{nome}.xml")
            shutil.move(caminho_download_xml, caminho_destino_xml)
            print(f"NF XML de {nome} baixada e salva com sucesso!")
        else:
            print(f"Erro ao encontrar o arquivo XML para {nome}")
        
        # Encontrar o arquivo PDF baixado
        pdf_files = glob.glob(os.path.join(download_dir, "*.pdf"))
        if pdf_files:
            caminho_download_pdf = max(pdf_files, key=os.path.getctime)
            caminho_destino_pdf = os.path.join(destino_dir, f"{nome}.pdf")
            shutil.move(caminho_download_pdf, caminho_destino_pdf)
            print(f"NF PDF de {nome} baixada e salva com sucesso!")
        else:
            print(f"Erro ao encontrar o arquivo PDF para {nome}")
    
    except Exception as e:
        print(f"Erro ao preencher os campos de login para {nome}: {e}")
    
    finally:
        driver.quit()  # Fechar o navegador após processar cada cliente
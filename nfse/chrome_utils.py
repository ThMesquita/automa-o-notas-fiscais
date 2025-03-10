import os
import subprocess

def get_chrome_user_data_dir():
    # Diretórios padrão do Chrome no Windows
    possible_dirs = [
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data"),
        os.path.expandvars(r"%APPDATA%\Google\Chrome\User Data")
    ]
    
    for dir in possible_dirs:
        if os.path.exists(dir):
            return dir
    
    raise EnvironmentError("Não foi possível encontrar o diretório do perfil do Chrome.")

def fechar_instancias_chrome():
    # Fechar todas as instâncias do Chrome
    subprocess.run(["powershell", "-Command", "Get-Process chrome | ForEach-Object { $_.CloseMainWindow() }"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
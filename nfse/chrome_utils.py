import os
import subprocess
import time

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

def get_chrome_profile_dir(user_data_dir):
    # Tentar detectar o perfil padrão do Chrome
    default_profile = os.path.join(user_data_dir, "Default")
    if os.path.exists(default_profile):
        return "Default"
    
    # Se o perfil padrão não for encontrado, usar o primeiro perfil disponível
    profiles = [d for d in os.listdir(user_data_dir) if d.startswith("Profile")]
    if profiles:
        return profiles[0]
    
    raise EnvironmentError("Não foi possível encontrar um perfil do Chrome.")

def fechar_instancias_chrome():
    # Fechar todas as instâncias do Chrome
    subprocess.run(["powershell", "-Command", "Get-Process chrome | ForEach-Object { $_.CloseMainWindow() }"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
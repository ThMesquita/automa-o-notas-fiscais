import sqlite3
import json

# Carregar usuários do arquivo JSON
with open('users.json', 'r') as f:
    users_json = json.load(f)

# Conectar ao banco de dados
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Atualizar senhas no banco de dados
for username, password in users_json['users'].items():
    c.execute('UPDATE users SET password = ? WHERE username = ?', (password, username))

# Salvar (commit) as mudanças e fechar a conexão
conn.commit()
conn.close()

print("Senhas atualizadas com sucesso!")
import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Criar a tabela de usuários
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# Adicionar alguns usuários iniciais
users = [
    ('user1', '@#$%'),
    ('user2', '@#$%')
]

c.executemany('INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)', users)

# Salvar (commit) as mudanças e fechar a conexão
conn.commit()
conn.close()
import sqlite3

def criar_banco():
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    # Verifica se a coluna 'categoria' existe, se não existir, adiciona
    cursor.execute("PRAGMA table_info(despesas)")
    colunas = [info[1] for info in cursor.fetchall()]
    if 'categoria' not in colunas:
        cursor.execute("ALTER TABLE despesas ADD COLUMN categoria TEXT")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS despesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            categoria TEXT,
            descricao TEXT,
            valor REAL,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

def adicionar_despesa(user_id, categoria, descricao, valor, data):
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO despesas (user_id, categoria, descricao, valor, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, categoria, descricao, valor, data))
    conn.commit()
    conn.close()

def listar_despesas(user_id):
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, categoria, descricao, valor, data FROM despesas WHERE user_id = ?', (user_id,))
    despesas = cursor.fetchall()
    conn.close()
    return despesas

def deletar_despesa(id_despesa):
    conn = sqlite3.connect('despesas.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM despesas WHERE id = ?', (id_despesa,))
    conn.commit()
    conn.close()
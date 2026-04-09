import sqlite3

def get_connection():
    con = sqlite3.connect('risk.db')
    con.execute("PRAGMA foreign_keys = ON;")
    return con

def _executar(query, params=()):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
    finally:
        con.close()

def _buscar_todos(query, params=()):
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params)
    dados = cur.fetchall()
    con.close()
    return dados

def _buscar_um(query, params=()):
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params)
    dado = cur.fetchone()
    con.close()
    return dado

def _executar_retorno(query, params=()):
    con = get_connection()
    cur = con.cursor()
    cur.execute(query, params)
    con.commit()
    last_id = cur.lastrowid
    con.close()
    return last_id

def init_db():
    con = get_connection()
    cur = con.cursor()
    
    cur.execute("""CREATE TABLE IF NOT EXISTS produtos (
                id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                exige_kg INTEGER NOT NULL DEFAULT 1
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS precos (
                id_preco INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                preco REAL NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1,
                data TEXT NOT NULL DEFAULT(datetime('now', 'localtime')),

                FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS vendas (
                id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
                data_venda TEXT NOT NULL DEFAULT(datetime('now', 'localtime'))
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS custos (
                id_custo INTEGER PRIMARY KEY AUTOINCREMENT,
                id_produto INTEGER NOT NULL,
                custo REAL NOT NULL,
                ativo INTEGER NOT NULL DEFAULT 1,
                data TEXT NOT NULL DEFAULT(datetime('now', 'localtime')),

                FOREIGN KEY (id_produto) REFERENCES produtos(id_produto)
                )""")
    
    cur.execute("""CREATE TABLE IF NOT EXISTS itens_venda (
                id_item INTEGER PRIMARY KEY AUTOINCREMENT,
                id_preco INTEGER NOT NULL,
                id_produto INTEGER NOT NULL,
                id_venda INTEGER NOT NULL,
                id_custo INTEGER NOT NULL,
                quilos REAL NOT NULL DEFAULT 1,
                
                FOREIGN KEY (id_preco) REFERENCES precos(id_preco),
                FOREIGN KEY (id_venda) REFERENCES vendas(id_venda),
                FOREIGN KEY (id_produto) REFERENCES produtos(id_produto),
                FOREIGN KEY (id_custo) REFERENCES custos(id_custo)
                )""")
    
    con.commit()
    con.close()

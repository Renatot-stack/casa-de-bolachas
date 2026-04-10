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
    try:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchall()
    finally:
        con.close()

def _buscar_um(query, params=()):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, params)
        return cur.fetchone()
    finally:
        con.close()

def _executar_retorno(query, params=()):
    con = get_connection()
    try:
        cur = con.cursor()
        cur.execute(query, params)
        con.commit()
        return cur.lastrowid
    finally:
        con.close()

def init_db():
    con = get_connection()
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            exige_kg INTEGER NOT NULL DEFAULT 1
                CHECK (exige_kg IN (0,1))
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS precos (
            id_preco INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            preco REAL NOT NULL CHECK (preco >= 0),
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),
            data TEXT NOT NULL DEFAULT(datetime('now', 'localtime')),
            FOREIGN KEY (id_produto)
                REFERENCES produtos(id_produto)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS custos (
            id_custo INTEGER PRIMARY KEY AUTOINCREMENT,
            id_produto INTEGER NOT NULL,
            custo REAL NOT NULL CHECK (custo >= 0),
            ativo INTEGER NOT NULL DEFAULT 1
                CHECK (ativo IN (0,1)),
            data TEXT NOT NULL DEFAULT(datetime('now', 'localtime')),
            FOREIGN KEY (id_produto)
                REFERENCES produtos(id_produto)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id_venda INTEGER PRIMARY KEY AUTOINCREMENT,
            data_venda TEXT NOT NULL DEFAULT(datetime('now', 'localtime'))
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id_item INTEGER PRIMARY KEY AUTOINCREMENT,
            id_venda INTEGER NOT NULL,
            id_preco INTEGER NOT NULL,
            id_custo INTEGER NOT NULL,
            quilos REAL NOT NULL DEFAULT 1 CHECK (quilos > 0),
            FOREIGN KEY (id_venda)
                REFERENCES vendas(id_venda)
                ON DELETE CASCADE,
            FOREIGN KEY (id_preco)
                REFERENCES precos(id_preco)
                ON UPDATE CASCADE
                ON DELETE RESTRICT,
            FOREIGN KEY (id_custo)
                REFERENCES custos(id_custo)
                ON UPDATE CASCADE
                ON DELETE RESTRICT
        );
    """)

    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_preco_ativo
        ON precos(id_produto)
        WHERE ativo = 1;
    """)

    cur.execute("""
        CREATE UNIQUE INDEX IF NOT EXISTS idx_custo_ativo
        ON custos(id_produto)
        WHERE ativo = 1;
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_precos_produto
        ON precos(id_produto);
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_custos_produto
        ON custos(id_produto);
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_itens_venda_venda
        ON itens_venda(id_venda);
    """)

    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_vendas_data
        ON vendas(data_venda);
    """)

    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_preco_desativar_antigos
        BEFORE INSERT ON precos
        WHEN NEW.ativo = 1
        BEGIN
            UPDATE precos
            SET ativo = 0
            WHERE id_produto = NEW.id_produto
            AND ativo = 1;
        END;
    """)

    cur.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_custo_desativar_antigos
        BEFORE INSERT ON custos
        WHEN NEW.ativo = 1
        BEGIN
            UPDATE custos
            SET ativo = 0
            WHERE id_produto = NEW.id_produto
            AND ativo = 1;
        END;
    """)

    con.commit()
    con.close()

def _lucro_item():
    return _buscar_todos("""SELECT 
            iv.id_item,
            p.nome,
            iv.quilos,
            pr.preco,
            c.custo,
            (iv.quilos * pr.preco) AS receita,
            (iv.quilos * c.custo) AS despesa,
            (iv.quilos * (pr.preco - c.custo)) AS lucro
        FROM itens_venda iv
        JOIN precos pr ON iv.id_preco = pr.id_preco
        JOIN custos c ON iv.id_custo = c.id_custo
        JOIN produtos p ON pr.id_produto = p.id_produto;""")
    
def _lucro_venda():
    return _buscar_todos("""SELECT 
            v.id_venda,
            v.data_venda,
            SUM(iv.quilos * pr.preco) AS receita_total,
            SUM(iv.quilos * c.custo) AS custo_total,
            SUM(iv.quilos * (pr.preco - c.custo)) AS lucro_total
        FROM vendas v
        JOIN itens_venda iv ON v.id_venda = iv.id_venda
        JOIN precos pr ON iv.id_preco = pr.id_preco
        JOIN custos c ON iv.id_custo = c.id_custo
        GROUP BY v.id_venda, v.data_venda
        ORDER BY v.data_venda DESC;""")
    
def _lucro_produto():
    return _buscar_todos("""SELECT 
            p.nome,
            SUM(iv.quilos) AS quantidade_total,
            SUM(iv.quilos * pr.preco) AS receita_total,
            SUM(iv.quilos * c.custo) AS custo_total,
            SUM(iv.quilos * (pr.preco - c.custo)) AS lucro_total
        FROM itens_venda iv
        JOIN precos pr ON iv.id_preco = pr.id_preco
        JOIN custos c ON iv.id_custo = c.id_custo
        JOIN produtos p ON pr.id_produto = p.id_produto
        GROUP BY p.nome
        ORDER BY lucro_total DESC;""")

def _registrar_produto(nome, preco, exige_kg):
    cod = _executar_retorno("INSERT INTO produtos (nome, exige_kg) VALUES (?, ?)", (nome, exige_kg))
    _executar('INSERT INTO precos (id_produto, preco) VALUES (?, ?)', (cod, preco))


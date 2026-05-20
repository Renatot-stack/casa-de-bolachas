import sqlite3

def get_connection():
    con = sqlite3.connect('bolachas.db')
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
            quantidade REAL NOT NULL DEFAULT 1 CHECK (quantidade > 0),
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

    cur.execute("""
        CREATE TABLE IF NOT EXISTS estoque (
            id_produto INTEGER PRIMARY KEY,
            quantidade REAL NOT NULL DEFAULT 0
                CHECK (quantidade >= 0),

            FOREIGN KEY (id_produto)
                REFERENCES produtos(id_produto)
                ON DELETE CASCADE
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
        id_mov INTEGER PRIMARY KEY AUTOINCREMENT,

        id_produto INTEGER NOT NULL,

        tipo TEXT NOT NULL
            CHECK(tipo IN ('ENTRADA', 'SAIDA')),

        quantidade REAL NOT NULL
            CHECK(quantidade > 0),

        motivo TEXT,

        data_mov TEXT NOT NULL
            DEFAULT(datetime('now', 'localtime')),

        FOREIGN KEY (id_produto)
            REFERENCES produtos(id_produto)
            ON DELETE CASCADE
    );""")

    con.commit()
    con.close()

def _lucro_item():
    return _buscar_todos("""SELECT 
            iv.id_item,
            p.nome,
            iv.quantidade,
            pr.preco,
            c.custo,
            (iv.quantidade * pr.preco) AS receita,
            (iv.quantidade * c.custo) AS despesa,
            (iv.quantidade * (pr.preco - c.custo)) AS lucro
        FROM itens_venda iv
        JOIN precos pr ON iv.id_preco = pr.id_preco
        JOIN custos c ON iv.id_custo = c.id_custo
        JOIN produtos p ON pr.id_produto = p.id_produto;""")
    
def _lucro_venda():
    return _buscar_todos("""SELECT 
            v.id_venda,
            v.data_venda,
            SUM(iv.quantidade * pr.preco) AS receita_total,
            SUM(iv.quantidade * c.custo) AS custo_total,
            SUM(iv.quantidade * (pr.preco - c.custo)) AS lucro_total
        FROM vendas v
        JOIN itens_venda iv ON v.id_venda = iv.id_venda
        JOIN precos pr ON iv.id_preco = pr.id_preco
        JOIN custos c ON iv.id_custo = c.id_custo
        GROUP BY v.id_venda, v.data_venda
        ORDER BY v.data_venda DESC;""")
    
def _lucro_produto():
    return _buscar_todos("""SELECT 
            p.nome,
            SUM(iv.quantidade) AS quantidade_total,
            SUM(iv.quantidade * pr.preco) AS receita_total,
            SUM(iv.quantidade * c.custo) AS custo_total,
            SUM(iv.quantidade * (pr.preco - c.custo)) AS lucro_total
        FROM itens_venda iv
        JOIN precos pr ON iv.id_preco = pr.id_preco
        JOIN custos c ON iv.id_custo = c.id_custo
        JOIN produtos p ON pr.id_produto = p.id_produto
        GROUP BY p.nome
        ORDER BY lucro_total DESC;""")

def _registrar_produto(nome, preco, custo, exige_kg):
    cod = _executar_retorno("INSERT INTO produtos (nome, exige_kg) VALUES (?, ?)", (nome, exige_kg))
    _executar('INSERT INTO precos (id_produto, preco) VALUES (?, ?)', (cod, preco))
    _executar('INSERT INTO custos (id_produto, custo) VALUES (?, ?)', (cod, custo))

def _pesquisar(chave):
    return _buscar_todos('SELECT nome, id_produto FROM produtos WHERE LOWER(nome) LIKE ?', (f'%{chave.lower()}%',))

def adicionar_estoque(id_produto, quantidade, motivo='Reposição'):
    
    produto = _buscar_um(
        'SELECT id_produto FROM estoque WHERE id_produto = ?',
        (id_produto,)
    )

    if produto:
        _executar('''
            UPDATE estoque
            SET quantidade = quantidade + ?
            WHERE id_produto = ?
        ''', (quantidade, id_produto))

    else:
        _executar('''
            INSERT INTO estoque (id_produto, quantidade)
            VALUES (?, ?)
        ''', (id_produto, quantidade))

    _executar('''
        INSERT INTO movimentacoes_estoque
        (id_produto, tipo, quantidade, motivo)
        VALUES (?, 'ENTRADA', ?, ?)
    ''', (id_produto, quantidade, motivo))

def registrar_venda(lista_produtos):
    """lista_produtos é um dicionário como este:
    produtos = [
    {
        'id_produto': 1,
        'quantidade': 2
    },
    {
        'id_produto': 3,
        'quantidade': 0.5
    }
    ]
    """

    con = get_connection()

    try:
        cur = con.cursor()

        # cria venda
        cur.execute('INSERT INTO vendas DEFAULT VALUES')

        id_venda = cur.lastrowid

        for item in lista_produtos:

            id_produto = item['id_produto']
            quantidade = item['quantidade']

            # verifica estoque
            cur.execute('''
                SELECT quantidade
                FROM estoque
                WHERE id_produto = ?
            ''', (id_produto,))

            resultado = cur.fetchone()

            if not resultado:
                raise Exception('Produto sem estoque cadastrado')

            estoque_atual = resultado[0]

            if estoque_atual < quantidade:
                raise Exception(
                    f'Estoque insuficiente para produto {id_produto}'
                )

            # pega preço ativo
            cur.execute('''
                SELECT id_preco
                FROM precos
                WHERE id_produto = ?
                AND ativo = 1
            ''', (id_produto,))

            id_preco = cur.fetchone()[0]

            # pega custo ativo
            cur.execute('''
                SELECT id_custo
                FROM custos
                WHERE id_produto = ?
                AND ativo = 1
            ''', (id_produto,))

            id_custo = cur.fetchone()[0]

            # registra item
            cur.execute('''
                INSERT INTO itens_venda
                (id_venda, id_preco, id_custo, quantidade)
                VALUES (?, ?, ?, ?)
            ''', (
                id_venda,
                id_preco,
                id_custo,
                quantidade
            ))

            # baixa estoque
            cur.execute('''
                UPDATE estoque
                SET quantidade = quantidade - ?
                WHERE id_produto = ?
            ''', (quantidade, id_produto))

            # registra movimentação
            cur.execute('''
                INSERT INTO movimentacoes_estoque
                (id_produto, tipo, quantidade, motivo)
                VALUES (?, 'SAIDA', ?, 'VENDA')
            ''', (id_produto, quantidade))

        con.commit()

    except Exception as erro:
        con.rollback()
        raise erro

    finally:
        con.close()

def obter_preco(id_produto):
    return _buscar_um('''
        SELECT preco
        FROM precos
        WHERE id_produto = ?
        AND ativo = 1
    ''', (id_produto,))

def listar_produtos():
    return _buscar_todos('''
        SELECT
            p.id_produto,
            p.nome,
            p.exige_kg,
            IFNULL(e.quantidade, 0),
            pr.preco
        FROM produtos p

        LEFT JOIN estoque e
            ON p.id_produto = e.id_produto

        LEFT JOIN precos pr
            ON p.id_produto = pr.id_produto
            AND pr.ativo = 1

        ORDER BY p.nome
    ''')

def listar_produtos_preco():
    return _buscar_todos('''
        SELECT
            p.id_produto,
            p.nome,
            pr.preco
        FROM produtos p

        JOIN precos pr
            ON p.id_produto = pr.id_produto

        WHERE pr.ativo = 1

        ORDER BY p.nome
    ''')

def pesquisar_produtos_preco(chave):
    return _buscar_todos('''
        SELECT
            p.id_produto,
            p.nome,
            pr.preco
        FROM produtos p

        JOIN precos pr
            ON p.id_produto = pr.id_produto

        WHERE
            pr.ativo = 1
            AND LOWER(p.nome) LIKE ?

        ORDER BY p.nome
    ''', (f'%{chave.lower()}%',))

def pesquisar_produtos_preco_id(chave):
    "Retorna o id, nome e preço do produto pelo id"
    return _buscar_todos('''
        SELECT
            p.id_produto,
            p.nome,
            pr.preco
        FROM produtos p

        JOIN precos pr
            ON p.id_produto = pr.id_produto

        WHERE
            pr.ativo = 1
            AND p.id_produto = ?

        ORDER BY p.nome
    ''', (chave,))
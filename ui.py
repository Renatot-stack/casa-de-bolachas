import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import database as db
import webbrowser

# Cores
beige = "#EEEEEE"
vermelho = "#FF0000"
vermelho_h = "#881111"
branco = "#FFFFFF"
cinza = "#E0E0E0"
marrom_c = "#242424"
branco = "#FFFFFF"
branco_e = "#666666"
branco_hover = "#333333"
cinza_e = "#AAAAAA"
verde = "#00941E"
verde_h = "#007417"
text_cor = "#00FF33"
cinza = "#5F5F5F"

# Inicia o Banco
db.init_db()

# Mensagens
def m_erro(erro):
    CTkMessagebox(janela, title='Erro', message=f'Ocorreu um erro: {erro}', icon='cancel')

def m_sucesso(title, message):
    CTkMessagebox(janela, title=title, message=message, icon='check')

# Funções:

def validar_preco(texto):
    if texto == "":
        return True

    # troca vírgula por ponto para facilitar a validação
    texto = texto.replace(",", ".")

    # não permite mais de um ponto
    if texto.count(".") > 1:
        return False

    try:
        float(texto)
        return True
    except ValueError:
        return False

def produtos_cadastrados(f):
        lista_produtos = ctk.CTkScrollableFrame(
            f,
            height=250
        )

        lista_produtos.grid(
            row=6,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
            sticky='nsew'
        )

        produtos = db.listar_produtos()

        for produto in produtos:

            id_produto = produto[0]
            nome = produto[1]
            estoque = produto[3]
            preco = produto[4]

            item = ctk.CTkFrame(lista_produtos)

            item.columnconfigure(1, weight=1)

            ctk.CTkLabel(
                item,
                text=f'ID: {id_produto}'
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=2
            )

            ctk.CTkLabel(
                item,
                text=nome
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=2,
                sticky='w'
            )

            ctk.CTkLabel(
                item,
                text=f'Estoque: {estoque}'
            ).grid(
                row=0,
                column=2,
                padx=5,
                pady=2
            )

            ctk.CTkLabel(
                item,
                text=f'R$ {preco:.2f}'
            ).grid(
                row=0,
                column=3,
                padx=5,
                pady=2
            )

            item.grid(
                sticky='ew',
                padx=2,
                pady=2
            )

def _main_frame_atualizar(_funcao):
    for i, widget in enumerate(main_frame.winfo_children()):
        if i != 0:
            widget.destroy()
    _funcao()

def deixar_clicavel(widget, comando, *parametros):

    def clique(event):
        comando(*parametros)

    widget.bind('<Button-1>', clique)

    for filho in widget.winfo_children():
        filho.bind('<Button-1>', clique)

def verificar_estoque_baixo():

    produtos = db.produtos_estoque_baixo()

    if not produtos:
        return

    mensagem = ""

    for produto in produtos:

        mensagem += (
            f"{produto[1]} "
            f"({produto[2]})\n"
        )

    CTkMessagebox(
        title="⚠ Estoque Baixo",
        message=mensagem,
        icon="warning"
    )

def _vendas():

    carrinho = []

    title_main_frame.configure(
        text='Venda de Produtos'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(2, weight=1)

    pesquisa = ctk.CTkEntry(
        frame,
        placeholder_text='Pesquise pelo produto...'
    )

    pesquisa.grid(
        row=0,
        column=0,
        sticky='ew',
        padx=2,
        pady=5
    )

    resultados = ctk.CTkScrollableFrame(frame)
    resultados.columnconfigure(0, weight=1)

    resultados.grid(
        row=1,
        column=0,
        sticky='ew',
        padx=2,
        pady=5
    )

    itens = ctk.CTkScrollableFrame(frame, fg_color=beige)

    itens.columnconfigure(0, weight=1)

    itens.grid(
        row=2,
        column=0,
        padx=2,
        pady=2,
        sticky='nsew'
    )

    total_label = ctk.CTkLabel(
        frame,
        text='Total: R$ 0,00',
        font=('Arial', 18, 'bold')
    )

    total_label.grid(
        row=3,
        column=0,
        padx=5,
        pady=5,
        sticky='e'
    )

    def atualizar_total():

        total = 0

        for item in carrinho:

            try:

                valor = float(
                    item['quantidade_widget']
                    .get()
                    .replace(',', '.')
                )

                if item['vende_por_kg']:

                    total += valor

                else:

                    total += (
                        valor
                        * item['preco']
                    )

            except:
                pass

        total_label.configure(
            text=f'Total: R$ {total:.2f}'
        )

    def novo_item(id_produto):

        dados = db.pesquisar_produtos_preco_id(
            id_produto
        )[0]

        produto = db.obter_produto(id_produto)

        vende_por_kg = produto[2] == 1

        sub_widget = ctk.CTkFrame(itens)

        sub_widget.columnconfigure(1, weight=1)

        ctk.CTkLabel(
            sub_widget,
            text=f"ID: {dados[0]}"
        ).grid(
            padx=5,
            pady=2,
            column=0,
            row=0
        )

        ctk.CTkLabel(
            sub_widget,
            text=dados[1]
        ).grid(
            padx=5,
            pady=2,
            column=1,
            row=0,
            sticky='ew'
        )

        ctk.CTkLabel(
            sub_widget,
            text=f'R$ {dados[2]:.2f}'
        ).grid(
            padx=5,
            pady=2,
            column=2,
            row=0
        )

        quantidade = ctk.CTkEntry(
            sub_widget,
            placeholder_text=(
                'Valor R$...'
                if vende_por_kg
                else 'Quantidade...'
            )
        )

        quantidade.insert(0, '1')

        quantidade.grid(
            row=0,
            column=3,
            padx=2,
            pady=2
        )
        quantidade.bind(
            '<KeyRelease>',
            lambda e: atualizar_total()
        )

        item = {
            'id_produto': id_produto,
            'quantidade_widget': quantidade,
            'widget': sub_widget,
            'preco': dados[2],
            'vende_por_kg': vende_por_kg
        }

        carrinho.append(item)
        atualizar_total()

        def remover():

            carrinho.remove(item)

            sub_widget.destroy()

            atualizar_total()

        ctk.CTkButton(
            sub_widget,
            text='X',
            width=10,
            corner_radius=8,
            fg_color=vermelho,
            hover_color='bold',
            text_color=branco,
            command=remover
        ).grid(
            column=4,
            row=0,
            padx=5,
            pady=2,
            sticky='w'
        )

        sub_widget.grid(
            padx=2,
            pady=2,
            sticky='ew',
            column=0
        )

    def finalizar_venda():

        if not carrinho:

            m_erro('Carrinho vazio')
            return

        produtos = []

        try:

            for item in carrinho:

                texto = item[
                    'quantidade_widget'
                ].get()

                valor_digitado = float(
                    texto.replace(',', '.')
                )

                if item['vende_por_kg']:

                    quantidade = (
                        valor_digitado
                        / item['preco']
                    )

                else:

                    quantidade = valor_digitado

                if quantidade <= 0:

                    raise Exception(
                        'Quantidade inválida'
                    )

                quantidade = float(
                    f'{quantidade:.3f}'
                )
                
                produtos.append({
                    'id_produto': item['id_produto'],
                    'quantidade': quantidade
                })

            db.registrar_venda(produtos)
            atualizar_historico()
            atualizar_alertas()
            verificar_estoque_baixo()

        except Exception as erro:

            m_erro(erro)
            return

        m_sucesso(
            'Venda concluída',
            'Estoque atualizado com sucesso'
        )

        _main_frame_atualizar(_vendas)

    botao_comprar = ctk.CTkButton(
        frame,
        text='Finalizar Venda',
        fg_color='green',
        hover_color='#0A5A00',
        command=finalizar_venda
    )

    botao_comprar.grid(
        row=4,
        column=0,
        padx=5,
        pady=5,
        sticky='ew'
    )

    janela.bind(
        '<F5>',
        lambda e: finalizar_venda()
    )

    def pesquisar():

        chave = pesquisa.get()

        produtos = db.pesquisar_produtos_preco(
            chave
        )

        for i in resultados.winfo_children():
            i.destroy()

        if not produtos:

            widget = ctk.CTkFrame(resultados, fg_color=cinza)

            ctk.CTkLabel(
                widget,
                text='Nenhum produto encontrado',
                text_color=branco
            ).grid(
                column=2,
                padx=5,
                pady=2,
                sticky='nsew'
            )

            widget.grid(
                padx=5,
                pady=2
            )

            return
        
        resultados.columnconfigure(0, weight=1)

        for produto in produtos:

            widget = ctk.CTkFrame(resultados, fg_color=cinza)

            ctk.CTkLabel(
                widget,
                text=f'ID: {produto[0]}',
                text_color=branco,
                font=('Consolas', 10)
            ).grid(
                padx=5,
                pady=2,
                row=0,
                column=0
            )

            ctk.CTkLabel(
                widget,
                text=produto[1],
                text_color='gold',
                font=('Arial', 15)
            ).grid(
                padx=5,
                pady=2,
                row=0,
                column=1
            )

            widget.columnconfigure(2, weight=1)

            ctk.CTkLabel(
                widget,
                text=f'R$ {produto[2]:.2f}',
                text_color=text_cor,
                font=('Arial', 18)
            ).grid(
                padx=5,
                pady=2,
                row=0,
                column=2,
                sticky='e'
            )

            widget.grid(
                column=0,
                padx=5,
                pady=2,
                sticky='ew'
            )

            deixar_clicavel(
                widget,
                novo_item,
                produto[0]
            )

    pesquisa.bind(
        '<Return>',
        lambda _: pesquisar()
    )

    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )
    pesquisar()

def _registrar_produto():
    title_main_frame.configure(text='Registrar Produtos')
    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)
    
    entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome...")
    entry_nome.grid(row=0, column=0, pady=5, padx=5)

    ctk.CTkLabel(frame, text="Produto no quilo:").grid(row=3, column=0, padx=5, pady=5)
    exige_peso = ctk.CTkOptionMenu(frame, values=['Sim', 'Não'])
    exige_peso.grid(row=3, column=1, padx=2, pady=5)

    ctk.CTkLabel(frame, text='Preço de venda:').grid(row=1, column=0, padx=2, pady=5)
    entry_preco_venda = ctk.CTkEntry(frame, placeholder_text='Preço...')
    entry_preco_venda.grid(row=1, column=1, padx=2, pady=5)

    ctk.CTkLabel(frame, text='Preço de compra:').grid(row=2, column=0, padx=2, pady=5)
    entry_preco_compra = ctk.CTkEntry(frame, placeholder_text='Preço...')
    entry_preco_compra.grid(row=2, column=1, padx=2, pady=5)

    def __registrar_produto():
        nome = entry_nome.get()
        preco = float(entry_preco_venda.get().replace(',', '.'))
        custo = float(entry_preco_compra.get().replace(',', '.'))
        exige = 1 if exige_peso.get() == 'Sim' else 0

        try:
            db._registrar_produto(nome, preco, custo, exige)
        except Exception as e:
            m_erro(e)
            return
        m_sucesso('Dados inseridos!', 'O novo produto já está pronto para venda!')

        _main_frame_atualizar(_registrar_produto)
    
    button_enviar = ctk.CTkButton(frame, text='Enviar', command= __registrar_produto)
    button_enviar.grid(row=4, column=1, sticky='s', padx=2, pady=5)

    ctk.CTkLabel(
        frame,
        text='Produtos cadastrados:'
    ).grid(
        row=5,
        column=0,
        columnspan=2,
        padx=5,
        pady=(10, 2),
        sticky='w'
    )

    produtos_cadastrados(frame)
    frame.grid(row=1, column=0, sticky='nsew')

def _cadastrar_estoque():

    title_main_frame.configure(
        text='Cadastrar Estoque'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)

    # Produto
    ctk.CTkLabel(
        frame,
        text='ID do Produto:'
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    entry_id = ctk.CTkEntry(
        frame,
        placeholder_text='ID...'
    )

    entry_id.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        sticky='ew'
    )

    # Quantidade
    ctk.CTkLabel(
        frame,
        text='Quantidade:'
    ).grid(
        row=1,
        column=0,
        padx=5,
        pady=5
    )

    entry_quantidade = ctk.CTkEntry(
        frame,
        placeholder_text='Quantidade...'
    )

    entry_quantidade.grid(
        row=1,
        column=1,
        padx=5,
        pady=5,
        sticky='ew'
    )

    def salvar_estoque():

        try:

            id_produto = int(
                entry_id.get()
            )

            quantidade = float(
                entry_quantidade.get().replace(',', '.')
            )

            if quantidade <= 0:
                raise Exception(
                    'Quantidade inválida'
                )

            db.adicionar_estoque(
                id_produto,
                db.arredondar_kg(quantidade)
            )

        except Exception as erro:

            m_erro(erro)
            return

        m_sucesso(
            'Estoque atualizado',
            'Quantidade adicionada com sucesso'
        )

        _main_frame_atualizar(_cadastrar_estoque)


    ctk.CTkButton(
        frame,
        text='Salvar',
        fg_color='green',
        hover_color='#0A5A00',
        command=salvar_estoque
    ).grid(
        row=2,
        column=1,
        padx=5,
        pady=10,
        sticky='e'
    )

    ctk.CTkLabel(
        frame,
        text='Produtos cadastrados:'
    ).grid(
        row=3,
        column=0,
        columnspan=2,
        padx=5,
        pady=(10, 2),
        sticky='w'
    )

    produtos_cadastrados(frame)

    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )

def _configuracoes():

    title_main_frame.configure(
        text='Configurações'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(0, weight=1)

    ctk.CTkButton(
        frame,
        text='Ajuste Manual de Estoque',
        height=50,
        command=lambda:
            _main_frame_atualizar(
                _ajuste_manual
            )
    ).grid(
        row=0,
        column=0,
        padx=20,
        pady=10,
        sticky='ew'
    )

    ctk.CTkButton(
        frame,
        text='Estornar Pedido',
        height=50,
        fg_color='red',
        hover_color="#5E0202",
        command=lambda:
            _main_frame_atualizar(
                _estornar_pedido
            )
    ).grid(
        row=1,
        column=0,
        padx=20,
        pady=10,
        sticky='ew'
    )

    ctk.CTkButton(
        frame,
        text='Estoque Mínimo',
        height=50,
        command=lambda:
            _main_frame_atualizar(
                _estoque_minimo
            )
    ).grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky='ew'
    )

    ctk.CTkButton(
        frame,
        fg_color='green',
        hover_color="#096806",
        text='Lucros',
        height=50,
        command=lambda:
            _main_frame_atualizar(
                _lucros
            )
    ).grid(
        row=3,
        column=0,
        padx=20,
        pady=10,
        sticky='ew'
    )
    
    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )

def _estoque_minimo():

    title_main_frame.configure(
        text='Estoque Mínimo'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(1, weight=1)

    ctk.CTkLabel(
        frame,
        text='ID do Produto:'
    ).grid(row=0, column=0, padx=5, pady=5)

    entry_id = ctk.CTkEntry(frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(
        frame,
        text='Estoque mínimo:'
    ).grid(row=1, column=0, padx=5, pady=5)

    entry_minimo = ctk.CTkEntry(frame)
    entry_minimo.grid(row=1, column=1, padx=5, pady=5)

    def carregar():

        try:

            dados = db.obter_configuracao_produto(
                int(entry_id.get())
            )

            if not dados:
                raise Exception(
                    'Produto não encontrado'
                )

            entry_minimo.delete(0, 'end')

            entry_minimo.insert(
                0,
                str(dados[0])
            )

        except Exception as erro:

            m_erro(erro)

    def salvar():

        try:

            db.atualizar_estoque_minimo(
                int(entry_id.get()),
                float(
                    entry_minimo.get()
                    .replace(',', '.')
                )
            )

        except Exception as erro:

            m_erro(erro)
            return

        m_sucesso(
            'Configurações',
            'Salvo com sucesso'
        )
        atualizar_alertas()
    ctk.CTkButton(
        frame,
        text='Carregar',
        command=carregar
    ).grid(row=2, column=0, padx=5, pady=5)

    ctk.CTkButton(
        frame,
        text='Salvar',
        command=salvar
    ).grid(row=2, column=1, padx=5, pady=5)
    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )

    produtos_cadastrados(frame)


def _lucros():

    title_main_frame.configure(
        text='Lucros'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)

    botoes = ctk.CTkFrame(frame)

    botoes.grid(
        row=0,
        column=0,
        padx=5,
        pady=5,
        sticky='ew'
    )

    resultados = ctk.CTkScrollableFrame(frame)

    resultados.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky='nsew'
    )

    def limpar():

        for widget in resultados.winfo_children():
            widget.destroy()

    def mostrar_dia():

        limpar()

        dados = db.lucro_por_dia()

        total = 0

        for horario, lucro in dados:

            total += lucro

            item = ctk.CTkFrame(resultados)

            ctk.CTkLabel(
                item,
                text=f'Hora: {horario}'
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                item,
                text=f'Lucro: R$ {lucro:.2f}'
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )

            item.pack(
                fill='x',
                padx=2,
                pady=2
            )

        ctk.CTkLabel(
            resultados,
            text=f'Lucro Total do Dia: R$ {total:.2f}',
            font=('Arial', 18)
        ).pack(pady=10)

    def mostrar_semana():

        limpar()

        dados = db.lucro_por_semana()

        total = 0

        for dia, lucro in dados:

            total += lucro

            item = ctk.CTkFrame(resultados)

            ctk.CTkLabel(
                item,
                text=f'Dia: {dia}'
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                item,
                text=f'Lucro: R$ {lucro:.2f}'
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )

            item.pack(
                fill='x',
                padx=2,
                pady=2
            )

        ctk.CTkLabel(
            resultados,
            text=f'Lucro Total Desta Semana: R$ {total:.2f}',
            font=('Arial', 18)
        ).pack(pady=10)

    def mostrar_mes():

        limpar()

        dados = db.lucro_por_mes()

        total = 0

        for dia, lucro in dados:

            total += lucro

            item = ctk.CTkFrame(resultados)

            ctk.CTkLabel(
                item,
                text=f'Dia: {dia}'
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                item,
                text=f'Lucro: R$ {lucro:.2f}'
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )

            item.pack(
                fill='x',
                padx=2,
                pady=2
            )

        ctk.CTkLabel(
            resultados,
            text=f'Lucro Total Deste Mês: R$ {total:.2f}',
            font=('Arial', 18)
        ).pack(pady=10)

    def mostrar_ano():

        limpar()

        meses = {
            '01': 'Janeiro',
            '02': 'Fevereiro',
            '03': 'Março',
            '04': 'Abril',
            '05': 'Maio',
            '06': 'Junho',
            '07': 'Julho',
            '08': 'Agosto',
            '09': 'Setembro',
            '10': 'Outubro',
            '11': 'Novembro',
            '12': 'Dezembro'
        }

        dados = db.lucro_por_ano()

        total = 0

        for mes, lucro in dados:

            total += lucro

            item = ctk.CTkFrame(resultados)

            ctk.CTkLabel(
                item,
                text=f'Mês: {meses[mes]}'
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )

            ctk.CTkLabel(
                item,
                text=f'Lucro: R$ {lucro:.2f}'
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )

            item.pack(
                fill='x',
                padx=2,
                pady=2
            )

        ctk.CTkLabel(
            resultados,
            text=f'Lucro Total Deste Ano: R$ {total:.2f}',
            font=('Arial', 18)
        ).pack(pady=10)

    ctk.CTkButton(
        botoes,
        text='Dia',
        command=mostrar_dia
    ).pack(side='left', padx=5)

    ctk.CTkButton(
        botoes,
        text='Semana',
        command=mostrar_semana
    ).pack(side='left', padx=5)

    ctk.CTkButton(
        botoes,
        text='Mês',
        command=mostrar_mes
    ).pack(side='left', padx=5)

    ctk.CTkButton(
        botoes,
        text='Ano',
        command=mostrar_ano
    ).pack(side='left', padx=5)

    mostrar_dia()

    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )

def atualizar_historico():

    for widget in historico_frame.winfo_children():
        widget.destroy()

    vendas = db.ultimas_vendas()

    if not vendas:

        ctk.CTkLabel(
            historico_frame,
            text='Nenhuma venda registrada'
        ).pack(
            pady=10
        )

        return

    for venda in vendas:

        id_venda = venda[0]
        data = venda[1]
        total = venda[2]

        item = ctk.CTkFrame(
            historico_frame,
            fg_color=cinza
        )

        ctk.CTkLabel(
            item,
            text=f'Pedido #{id_venda}',
            text_color=branco
        ).pack(
            anchor='w',
            padx=5,
            pady=(5,0)
        )

        ctk.CTkLabel(
            item,
            text=data,
            text_color=branco
        ).pack(
            anchor='w',
            padx=5
        )

        ctk.CTkLabel(
            item,
            text=f'R$ {total:.2f}',
            text_color=text_cor
        ).pack(
            anchor='w',
            padx=5,
            pady=(0,5)
        )

        item.pack(
            fill='x',
            padx=2,
            pady=2
        )

def abrir_alertas():

    produtos = db.produtos_estoque_baixo()

    janela_alertas = ctk.CTkToplevel(janela)

    janela_alertas.title(
        'Produtos com Estoque Baixo'
    )

    janela_alertas.geometry(
        '450x300'
    )

    lista = ctk.CTkScrollableFrame(
        janela_alertas
    )

    lista.pack(
        fill='both',
        expand=True,
        padx=10,
        pady=10
    )

    if not produtos:

        ctk.CTkLabel(
            lista,
            text='Nenhum alerta encontrado.'
        ).pack(
            pady=20
        )

        return

    for produto in produtos:

        item = ctk.CTkFrame(lista)

        ctk.CTkLabel(
            item,
            text=produto[1],
            font=('Arial', 16)
        ).pack(
            anchor='w',
            padx=5,
            pady=(5,0)
        )

        ctk.CTkLabel(
            item,
            text=f'Estoque: {produto[2]}'
        ).pack(
            anchor='w',
            padx=5
        )

        ctk.CTkLabel(
            item,
            text=f'Mínimo: {produto[3]}'
        ).pack(
            anchor='w',
            padx=5,
            pady=(0,5)
        )

        item.pack(
            fill='x',
            padx=5,
            pady=5
        )

def atualizar_alertas():
    
    produtos = db.produtos_estoque_baixo()

    total = len(produtos)

    if total == 0:

        alerta_btn.configure(
            text='Estoque OK',
            fg_color='green',
            text_color=branco
        )

    else:

        alerta_btn.configure(
            text=f'⚠️ {total} alerta(s)',
            fg_color='orange',
            text_color='black'
        )

def _estornar_pedido():

    title_main_frame.configure(
        text='Estornar Pedido'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(0, weight=1)

    ctk.CTkLabel(
        frame,
        text='ID da Venda'
    ).grid(
        row=0,
        column=0,
        padx=5,
        pady=5
    )

    entry_id = ctk.CTkEntry(frame)

    entry_id.grid(
        row=1,
        column=0,
        padx=5,
        pady=5,
        sticky='ew'
    )

    def estornar():

        resposta = CTkMessagebox(
            title="Confirmar",
            message=f"Estornar venda #{entry_id.get()}?",
            icon="question",
            option_1="Não",
            option_2="Sim"
        )

        if resposta.get() != "Sim":
            return

        try:

            db.estornar_venda(
                int(entry_id.get())
            )

            atualizar_historico()
            atualizar_alertas()

        except Exception as erro:

            m_erro(erro)
            return

        m_sucesso(
            'Estorno',
            'Venda cancelada'
        )

        _main_frame_atualizar(_vendas)

    ctk.CTkButton(
        frame,
        text='Estornar',
        fg_color='red',
        command=estornar
    ).grid(
        row=2,
        column=0,
        padx=5,
        pady=5
    )

    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )

def _ajuste_manual():

    title_main_frame.configure(
        text='Ajuste Manual'
    )

    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(1, weight=1)

    ctk.CTkLabel(
        frame,
        text='ID Produto'
    ).grid(row=0, column=0, padx=5, pady=5)

    entry_id = ctk.CTkEntry(frame)
    entry_id.grid(row=0, column=1, padx=5, pady=5)

    ctk.CTkLabel(
        frame,
        text='Novo Estoque'
    ).grid(row=1, column=0, padx=5, pady=5)

    entry_estoque = ctk.CTkEntry(frame)
    entry_estoque.grid(row=1, column=1, padx=5, pady=5)

    def salvar():

        try:

            db.corrigir_estoque(
                int(entry_id.get()),
                float(
                    entry_estoque.get()
                    .replace(',', '.')
                )
            )

            atualizar_alertas()

        except Exception as erro:

            m_erro(erro)
            return

        m_sucesso(
            'Ajuste',
            'Estoque corrigido'
        )

        _main_frame_atualizar(_ajuste_manual)


    ctk.CTkButton(
        frame,
        text='Salvar',
        command=salvar
    ).grid(
        row=2,
        column=1,
        pady=5,
        padx=5
    )

    produtos_cadastrados(frame)

    frame.grid(
        row=1,
        column=0,
        sticky='nsew'
    )

# Janela principal
janela = ctk.CTk(fg_color=marrom_c)
janela.title('São João ETE - Sistema de Estoque')
janela.minsize(800, 300)

# Janela configuração
janela.columnconfigure(0, weight=1)
janela.rowconfigure(1, weight=1)

# Header

header_frame = ctk.CTkFrame(janela)
header_frame.grid(row=0, column=0, pady=5, padx=5, sticky='we', columnspan=2)
header_frame.columnconfigure(0, weight=1)
ctk.CTkLabel(header_frame, text='Sistema de Estoque', font=('Arial', 20)).grid(row=0, column=0, padx=5, pady=5, sticky='ew', columnspan=2)

# Div Casa de Bolachas

frame_bolacha = ctk.CTkFrame(janela, fg_color=branco)
frame_bolacha.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Frame Bolacha configuração
frame_bolacha.columnconfigure(0, weight=1)

# Div De Cima

top_frame = ctk.CTkFrame(frame_bolacha)
top_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Para a coluna de Lucros expandir e encostar no lado direito
top_frame.columnconfigure(3, weight=1)

# Botão registrar produto 
registrar_prod = ctk.CTkButton(top_frame, text='Registrar Produto', fg_color=branco_e, hover_color=branco_hover, command=lambda: _main_frame_atualizar(_registrar_produto))
registrar_prod.grid(row=0, column=1, padx=10, pady=10)

# Botão novo pedido
novo_pedido = ctk.CTkButton(top_frame, text='Novo Pedido', fg_color=branco_e, hover_color=branco_hover, command=lambda: _main_frame_atualizar(_vendas))
novo_pedido.grid(row=0, column=0, padx=10, pady=10)

# Botão cadastrar estoque
cadastrar_estoque = ctk.CTkButton(
    top_frame,
    text='Cadastrar Estoque',
    fg_color=branco_e,
    hover_color=branco_hover,
    command=lambda: _main_frame_atualizar(_cadastrar_estoque)
)

cadastrar_estoque.grid(
    row=0,
    column=2,
    padx=10,
    pady=10,
    sticky='w'
)

# Botão ver lucros
# ver_lucro = ctk.CTkButton(
#     top_frame,
#     text='Lucros',
#     command=lambda: _main_frame_atualizar(_lucros),
#     fg_color='green',
#     hover_color="#072A00"
# )
# ver_lucro.grid(row=0, column=3, padx=10, pady=10, sticky='e')

# Div do meio / central / centro

frame_bolacha.rowconfigure(1, weight=1)

main_frame = ctk.CTkFrame(frame_bolacha)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

main_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Título do frame
title_main_frame = ctk.CTkLabel(main_frame, text='Sistema de Gerenciamento de lucros, estoque, pedidos...', text_color=branco, bg_color=cinza_e, corner_radius=10)
title_main_frame.grid(row=0, column=0, sticky='ew')

_vendas()

# Div de baixo / footer / rodape

down_frame = ctk.CTkFrame(frame_bolacha)
down_frame.columnconfigure(1, weight=1)

down_frame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

# Div do histórico

right_frame = ctk.CTkFrame(janela, width=300)
right_frame.grid(row=1, column=1, sticky='nse', pady=5, padx=5)

# Configurações
config_frame = ctk.CTkFrame(right_frame)
config_frame.grid(row=0, column=0, padx=2, pady=2, sticky='ew')

config_frame.columnconfigure(0, weight=1)

ctk.CTkLabel(
    config_frame,
    text='Histórico',
    font=('Consolas', 18)
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5,
    sticky='w'
)
historico_frame = ctk.CTkScrollableFrame(
    right_frame,
    width=280
)

historico_frame.grid(
    row=1,
    column=0,
    padx=5,
    pady=5,
    sticky='nsew'
)

right_frame.rowconfigure(
    1,
    weight=1
)
configuracoes = ctk.CTkButton(
    top_frame,
    text='Configurações',
    fg_color=branco_e,
    hover_color=branco_hover,
    command=lambda:
        _main_frame_atualizar(
            _configuracoes
        )
)

configuracoes.grid(
    row=0,
    column=4,
    padx=10,
    pady=10
)
# Texto de teste
ctk.CTkButton(down_frame, text='Em caso de erros, entrar em contato com +55 81 99127-2066', fg_color='transparent',hover_color='orange', text_color='black', command=lambda: webbrowser.open('https://wa.me/5581991272066?text=')).pack(side='left',padx=2, pady=2)

alerta_btn = ctk.CTkButton(
    down_frame,
    text='✅ Estoque OK',
    fg_color='orange',
    text_color='black',
    command=abrir_alertas
)

alerta_btn.pack(
    side='bottom',
    padx=5,
    pady=5
)
atualizar_alertas()
atualizar_historico()
janela.mainloop()

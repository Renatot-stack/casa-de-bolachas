import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import database as db
import webbrowser

# Cores
marrom_c = "#E8AF76"
marrom = "#BC7F43"
marrom_e = "#43280C"
marrom_bonito = "#724100"

# Inicia o Banco
db.init_db()

# Mensagens
def m_erro(erro):
    CTkMessagebox(janela, title='Erro', message=f'Ocorreu um erro: {erro}', icon='cancel')

def m_sucesso(title, message):
    CTkMessagebox(janela, title=title, message=message, icon='check')

# Funções:

def _main_frame_atualizar(_funcao):
    for i, widget in enumerate(main_frame.winfo_children()):
        if i != 0:
            widget.destroy()
    _funcao()

def _vendas():
    title_main_frame.configure(text='Venda de Produtos')
    frame = ctk.CTkFrame(main_frame)

    ctk.CTkLabel(frame, text='Caixa Aberto', font=('Arial', 50), text_color='green').grid(column=0)

def _registrar_produto():
    title_main_frame.configure(text='Registrar Produtos')
    frame = ctk.CTkFrame(main_frame)

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    frame.rowconfigure(3, weight=1)
    
    entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome...")
    entry_nome.grid(row=1, column=0, pady=5, padx=5)

    ctk.CTkLabel(frame, text="Produto no quilo:").grid(row=2, column=0, padx=5, pady=5)
    exige_peso = ctk.CTkOptionMenu(frame, values=['Sim', 'Não'])
    exige_peso.grid(row=2, column=1, padx=2, pady=5)

    entry_preco = ctk.CTkEntry(frame, placeholder_text='Preço...')
    entry_preco.grid(row=1, column=1, padx=2, pady=5)

    def __registrar_produto():
        nome = entry_nome.get()
        preco = float(entry_preco.get().replace(',', '.'))
        exige = 1 if exige_peso.get() == 'Sim' else 0

        try:
            db._registrar_produto(nome, preco, exige)
        except Exception as e:
            m_erro(e)
            return
        m_sucesso('Dados inseridos!', 'O novo produto já está pronto para venda!')
        _main_frame_atualizar(_vendas)
    
    button_enviar = ctk.CTkButton(frame, text='Enviar', command= __registrar_produto)
    button_enviar.grid(row=3, column=1, sticky='s', padx=2, pady=5)

    frame.grid(row=1, column=0, sticky='nsew')

# Janela principal
janela = ctk.CTk(fg_color=marrom_c)
janela.title('Casa de Bolachas - Sistema de Estoque')
janela.minsize(800, 300)

# Janela configuração
janela.columnconfigure(0, weight=1)
janela.rowconfigure(1, weight=1)

# Header

header_frame = ctk.CTkFrame(janela)
header_frame.grid(row=0, column=0, pady=5, padx=5, sticky='we', columnspan=2)
header_frame.columnconfigure(0, weight=1)
ctk.CTkLabel(header_frame, text='🍪 Casa de Bolachas 🍪', font=('Arial', 20)).grid(row=0, column=0, padx=5, pady=5, sticky='ew', columnspan=2)

# Div Casa de Bolachas

frame_bolacha = ctk.CTkFrame(janela, fg_color=marrom)
frame_bolacha.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Frame Bolacha configuração
frame_bolacha.columnconfigure(0, weight=1)

# Div De Cima

top_frame = ctk.CTkFrame(frame_bolacha)
top_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Para a coluna de Lucros expandir e encostar no lado direito
top_frame.columnconfigure(2, weight=1)

# Botão registrar produto 
registrar_prod = ctk.CTkButton(top_frame, text='Registrar Produto', fg_color=marrom_e, command=lambda: _main_frame_atualizar(_registrar_produto))
registrar_prod.grid(row=0, column=0, padx=10, pady=10)

# Botão novo pedido
novo_pedido = ctk.CTkButton(top_frame, text='Novo Pedido', fg_color=marrom_e, command=lambda: print('heloo'))
novo_pedido.grid(row=0, column=1, padx=10, pady=10)

# Botão ver lucros
ver_lucro = ctk.CTkButton(top_frame, text='Lucros', command=lambda: print('hello'), fg_color='green', hover_color="#072A00")
ver_lucro.grid(row=0, column=2, padx=10, pady=10, sticky='e')

# Div do meio / central / centro

frame_bolacha.rowconfigure(1, weight=1)

main_frame = ctk.CTkFrame(frame_bolacha)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(1, weight=1)

main_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Título do frame
title_main_frame = ctk.CTkLabel(main_frame, text='Sistema de Gerenciamento de lucros, estoque, pedidos...', text_color='white', bg_color=marrom_bonito, corner_radius=10)
title_main_frame.grid(row=0, column=0, sticky='ew')

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

# Preços
config = ctk.CTkButton(config_frame, text='⚙️', font=('Arial', 20))
config.grid(row=0, column=0, sticky='e')

# Texto de teste
ctk.CTkButton(down_frame, text='Em caso de erros, entrar em contato com +55 81 99127-2066', fg_color='transparent',hover_color='orange', text_color='black', command=lambda: webbrowser.open('https://wa.me/5581991272066?text=')).pack(padx=2, pady=2)

janela.mainloop()

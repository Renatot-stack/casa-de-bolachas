import customtkinter as ctk
import CTkMessagebox
import database

# Cores
marrom_c = "#E8AF76"
marrom = "#BC7F43"
marrom_e = "#43280C"

# Inicia o Banco
database.init_db()

# Funções:

def _registrar_produto():
    level_registrar = ctk.CTkToplevel(janela)
    level_registrar.title('Registrar Produtos')
    level_registrar.focus()

    entry_nome = ctk.CTkEntry(level_registrar, placeholder_text="Nome...")
    entry_nome.grid(row=0, column=0, pady=5, padx=5)

    ctk.CTkLabel(level_registrar, text="Produto no quilo:").grid(row=0, column=1, padx=5, pady=5)
    exige_peso = ctk.CTkOptionMenu(level_registrar, values=['Sim', 'Não'])
    exige_peso.grid(row=0, column=2, padx=2, pady=5)

    entry_preco = ctk.CTkEntry(level_registrar, fg_color=marrom_c, placeholder_text='Preço...')
    entry_preco.grid(row=0, column=3)

# Janela principal
janela = ctk.CTk(fg_color="#E8AF76")
janela.title('Casa de Bolachas - Sistema de Estoque')
janela.minsize(450, 300)

# Janela configuração
janela.columnconfigure(0, weight=1)
janela.rowconfigure(1, weight=1)

# Div Casa de Bolachas
frame_bolacha = ctk.CTkFrame(janela, fg_color=marrom)
frame_bolacha.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
ctk.CTkLabel(janela, text='🍪 Casa de Bolachas').grid(row=0, column=0, padx=5, pady=5, sticky='new')

# Frame Bolacha configuração
frame_bolacha.columnconfigure(0, weight=1)

# Div De Cima / header / cabeçalho

top_frame = ctk.CTkFrame(frame_bolacha)
top_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Para a coluna de Lucros expandir e encostar no lado direito
top_frame.columnconfigure(2, weight=1)

# Botão registrar produto 
registrar_prod = ctk.CTkButton(top_frame, text='Registrar Produto', fg_color=marrom_e, command=_registrar_produto)
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

main_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Texto de teste
ctk.CTkLabel(main_frame, text='Sistema de Gerenciamento de lucros, estoque, pedidos...').grid()

# Div de baixo / footer / rodape

down_frame = ctk.CTkFrame(frame_bolacha)

down_frame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

# Texto de teste
ctk.CTkLabel(down_frame, text='All rights reserved').grid()

janela.mainloop()

import customtkinter as ctk
# import CTkMessagebox
import database

# Cores
marrom_c = "#E8AF76"
marrom = "#BC7F43"
marrom_e = "#43280C"
marrom_bonito = "#724100"

# Inicia o Banco
database.init_db()

# Funções:

def _pegar_foco(window = ctk.CTkToplevel):
    window.lift()
    window.focus_force()
    window.grab_set()

def _main_frame_atualizar(_funcao):
    for i, widget in enumerate(main_frame.winfo_children()):
        if i != 0:
            widget.destroy()
    _funcao()
        
def _registrar_produto():
    title_main_frame.configure(text='Registrar Produtos')
    frame = ctk.CTkFrame(main_frame)
    frame.grid(row=1, column=0, sticky='nsew')

    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    
    entry_nome = ctk.CTkEntry(frame, placeholder_text="Nome...")
    entry_nome.grid(row=1, column=0, pady=5, padx=5)

    ctk.CTkLabel(frame, text="Produto no quilo:").grid(row=2, column=0, padx=5, pady=5)
    exige_peso = ctk.CTkOptionMenu(frame, values=['Sim', 'Não'])
    exige_peso.grid(row=2, column=1, padx=2, pady=5)

    entry_preco = ctk.CTkEntry(frame, placeholder_text='Preço...')
    entry_preco.grid(row=1, column=1)
    
    button_enviar = ctk.CTkButton(down_frame, text='Enviar')
    button_enviar.grid(row=0, column=1, sticky='e', padx=10, pady=10)

# Janela principal
janela = ctk.CTk(fg_color=marrom_c)
janela.title('Casa de Bolachas - Sistema de Estoque')
janela.minsize(450, 300)

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

historico_frame = ctk.CTkFrame(janela, width=300)
historico_frame.grid(row=1, column=1, sticky='nse', pady=5, padx=5)

# Texto de teste
ctk.CTkLabel(down_frame, text='All rights reserved').grid()

janela.mainloop()

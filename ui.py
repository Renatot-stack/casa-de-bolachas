import customtkinter as ctk
import CTkMessagebox

# Janela principal
janela = ctk.CTk()
janela.title('Casa de Bolachas - Sistema de Estoque')
janela.minsize(450, 300)

# Para as Divs se expandirem
janela.columnconfigure(0, weight=1)

# Div De Cima / header / cabeçalho

top_frame = ctk.CTkFrame(janela)
top_frame.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

# Para a coluna de Lucros expandir e encostar no lado direito
top_frame.columnconfigure(2, weight=1)

# Botão registrar produto 
registrar_prod = ctk.CTkButton(top_frame, text='Registrar Produto', command=lambda: print('Hello'))
registrar_prod.grid(row=0, column=0, padx=10, pady=10)

# Botão novo pedido
novo_pedido = ctk.CTkButton(top_frame, text='Novo Pedido', command=lambda: print('heloo'))
novo_pedido.grid(row=0, column=1, padx=10, pady=10)

# Botão ver lucros
ver_lucro = ctk.CTkButton(top_frame, text='Lucros', command=lambda: print('hello'), fg_color='green', hover_color="#072A00")
ver_lucro.grid(row=0, column=2, padx=10, pady=10, sticky='e')

# Div do meio / central / centro

janela.rowconfigure(1, weight=1)

main_frame = ctk.CTkFrame(janela)

main_frame.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

# Texto de teste
ctk.CTkLabel(main_frame, text='Sistema de Gerenciamento de lucros, estoque, pedidos...').grid()

# Div de baixo / footer / rodape

down_frame = ctk.CTkFrame(janela)

down_frame.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

# Texto de teste
ctk.CTkLabel(down_frame, text='All rights reserved').grid()

janela.mainloop()

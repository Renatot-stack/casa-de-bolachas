import customtkinter as ctk
import CTkMessagebox

janela = ctk.CTk()
janela.title('Casa de Bolachas - Sistema de Estoque')

# Div De Cima

top_frame = ctk.CTkFrame(janela)
top_frame.grid(row=0, column=0, padx=5, pady=5)

registrar_prod = ctk.CTkButton(top_frame, text='Registrar Produto', command=lambda: print('Hello'))
registrar_prod.grid(row=0, column=0, padx=10, pady=10)

novo_pedido = ctk.CTkButton(top_frame, text='Novo Pedido', command=lambda: print('heloo'))
novo_pedido.grid(row=0, column=1, padx=10, pady=10)

ver_lucro = ctk.CTkButton(top_frame, text='Lucros', command=lambda: print('hello'), fg_color='green', hover_color="#072A00")
ver_lucro.grid(row=0, column=2, padx=10, pady=10)

# Div do meio / central / centro

 

janela.mainloop()
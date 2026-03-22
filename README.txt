Códigos principais:

CTk() -> cria a janela
mainloop() -> faz com que a janela não feche por padrão


parâmetros:

text='?' -> define o texto do objeto
command=... -> define um comando para executar quando o objeto for clicado
values=[] -> define os valores possíveis do objeto através de uma lista


métodos:

.grid(row=?, column=?, stikcy='?', pad?=?) -> posiciona o objeto usando linha (row) e coluna (column), usa padx e pady para deixar um espaço em pixeis entre a borda e o objeto, estica (sticky) usando o padrão da rosa dos ventos (em inglês) North, South, East, West

.get() -> retorna o valor da maioria dos objetos em qual for usada


Objetos:

CTkLabel(janela, text='?') -> é um texto normal

CTkFrame(janela) -> é como uma div, também precisa ser posicionada
CTkButton(janela) -> é um botão
CTkEntry(janela) -> é uma caixa de entrada
CTkOptionMenu(janela) -> é como uma caixa de seleção única de múltipla escolha
CTkComboBox(janela) -> é como uma caixa de entrada com multípla escolha
CTkTopLevel(janela) -> é uma subjanela herdada da janela principal

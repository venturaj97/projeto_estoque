
import tkinter as tk
from tkinter import messagebox
import sqlite3

class LojaDeRoupa:
    def __init__(self, root, conn=None, c=None):
        self.root = root
        self.root.title("Loja de Roupas")
        self.conn = conn
        self.c = c
        
        if self.conn is None:
            self.conn = sqlite3.connect('estoque.db')
        if self.c is None:
            self.c = self.conn.cursor()
            
        self.c.execute('''CREATE TABLE IF NOT EXISTS estoque (
                            id INTEGER PRIMARY KEY,
                            produto TEXT,
                            quantidade INTEGER,
                            reposicao INTEGER,
                            vendido INTEGER)''')
        self.conn.commit()
        self.create_widgets()

    def create_widgets(self):
        # Título da loja
        label_title = tk.Label(self.root, text="Loja de Roupas", font=("Helvetica", 16, "bold"))
        label_title.pack(pady=10)

        # Entrada de Produto e Quantidade
        frame_input = tk.Frame(self.root)
        frame_input.pack(pady=5)

        self.label_produto = tk.Label(frame_input, text="Produto:", font=("Helvetica", 12))
        self.label_produto.grid(row=0, column=0, padx=5, pady=5)

        self.entry_produto = tk.Entry(frame_input, font=("Helvetica", 12), width=20)
        self.entry_produto.grid(row=0, column=1, padx=5, pady=5)

        self.label_quantidade = tk.Label(frame_input, text="Quantidade:", font=("Helvetica", 12))
        self.label_quantidade.grid(row=0, column=2, padx=5, pady=5)

        self.entry_quantidade = tk.Entry(frame_input, font=("Helvetica", 12), width=10)
        self.entry_quantidade.grid(row=0, column=3, padx=5, pady=5)

        # Botão Adicionar Estoque
        self.btn_adicionar = tk.Button(self.root, text="Adicionar ao Estoque", command=self.adicionar_estoque)
        self.btn_adicionar.pack(pady=5)

        # Vendas Atualizadas
        frame_vendas = tk.Frame(self.root)
        frame_vendas.pack(pady=5)

        self.label_vendido = tk.Label(frame_vendas, text="Vendido hoje:", font=("Helvetica", 12))
        self.label_vendido.grid(row=0, column=0, padx=5, pady=5)

        self.entry_vendido = tk.Entry(frame_vendas, font=("Helvetica", 12), width=10)
        self.entry_vendido.grid(row=0, column=1, padx=5, pady=5)

        # Botão Atualizar Vendas
        self.btn_atualizar = tk.Button(self.root, text="Atualizar Vendas", command=self.atualizar_vendas)
        self.btn_atualizar.pack(pady=5)

        # Botão Verificar Estoque
        self.btn_alerta = tk.Button(self.root, text="Verificar Estoque", command=self.verificar_estoque)
        self.btn_alerta.pack(pady=5)

    def adicionar_estoque(self):
        produto = self.entry_produto.get()
        quantidade = int(self.entry_quantidade.get())

        self.c.execute("SELECT * FROM estoque WHERE produto=?", (produto,))
        produto_existente = self.c.fetchone()

        if produto_existente:
            quantidade_atual = produto_existente[2]
            nova_quantidade = quantidade_atual + quantidade
            self.c.execute("UPDATE estoque SET quantidade=? WHERE produto=?", (nova_quantidade, produto))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Quantidade do produto atualizada no estoque.")
        else:
            self.c.execute("INSERT INTO estoque (produto, quantidade, reposicao, vendido) VALUES (?, ?, 0, 0)", (produto, quantidade))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto adicionado ao estoque.")

        self.entry_produto.delete(0, 'end')
        self.entry_quantidade.delete(0, 'end')

    def atualizar_vendas(self):
        vendido_str = self.entry_vendido.get()

        if vendido_str.strip(): 
            vendido = int(vendido_str)
            produto = self.entry_produto.get()

            self.c.execute("SELECT quantidade FROM estoque WHERE produto=?", (produto,))
            estoque_atual = self.c.fetchone()

            if estoque_atual is not None:
                estoque_atual = estoque_atual[0]
                if estoque_atual >= vendido:
                    self.c.execute("UPDATE estoque SET quantidade = quantidade - ? WHERE produto = ?", (vendido, produto))
                    self.conn.commit()
                    messagebox.showinfo("Sucesso", "Vendas atualizadas com sucesso.")
                else:
                    messagebox.showerror("Erro", "Não há estoque suficiente para realizar essa venda.")
            else:
                messagebox.showerror("Erro", "Produto não encontrado no estoque.")
        else:
            messagebox.showerror("Erro", "Por favor, insira a quantidade vendida.")
        
        self.entry_produto.delete(0, 'end')
        self.entry_quantidade.delete(0, 'end')
        self.entry_vendido.delete(0, 'end')

    def verificar_estoque(self):
        self.c.execute("SELECT produto, quantidade FROM estoque WHERE quantidade <= 5")
        baixo_estoque = self.c.fetchall()

        if baixo_estoque:
            mensagem = "Os seguintes produtos estão com estoque baixo:\n"
            for produto in baixo_estoque:
                mensagem += f"{produto[0]}: {produto[1]}\n"
            messagebox.showwarning("Estoque Baixo", mensagem)
        else:
            messagebox.showinfo("Estoque", "Todos os produtos têm estoque suficiente.")

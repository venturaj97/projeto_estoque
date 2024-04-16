
import tkinter as tk
from tkinter import messagebox
import sqlite3

class LojaDeRoupa:
    def __init__(self, root):
        self.root = root
        self.root.title("Loja de Roupas")
        self.conn = sqlite3.connect('estoque.db')
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
        labelpr = tk.Label(self.root, text="Aleatorios Store")
        labelpr.pack()
        self.label_produto = tk.Label(self.root, text="Produto:")
        self.label_produto.pack()
        self.entry_produto = tk.Entry(self.root)
        self.entry_produto.pack()

        self.label_quantidade = tk.Label(self.root, text="Quantidade:")
        self.label_quantidade.pack()
        self.entry_quantidade = tk.Entry(self.root)
        self.entry_quantidade.pack()

        self.btn_adicionar = tk.Button(self.root, text="Adicionar ao Estoque", command=self.adicionar_estoque)
        self.btn_adicionar.pack()

        self.label_vendido = tk.Label(self.root, text="Vendido hoje:")
        self.label_vendido.pack()
        self.entry_vendido = tk.Entry(self.root)
        self.entry_vendido.pack()

        self.btn_atualizar = tk.Button(self.root, text="Atualizar Vendas", command=self.atualizar_vendas)
        self.btn_atualizar.pack()

        self.btn_alerta = tk.Button(self.root, text="Verificar Estoque", command=self.verificar_estoque)
        self.btn_alerta.pack()

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

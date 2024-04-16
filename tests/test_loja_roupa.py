import tkinter as tk
import sqlite3
import pytest
from app.app_loja import LojaDeRoupa

@pytest.fixture
def loja_de_roupa():
    # Criar um banco de dados temporário em memória para os testes
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()
    c.execute('''CREATE TABLE estoque (
                    id INTEGER PRIMARY KEY,
                    produto TEXT,
                    quantidade INTEGER,
                    reposicao INTEGER,
                    vendido INTEGER)''')
    conn.commit()

    # Instanciar a classe LojaDeRoupa com o banco de dados temporário
    return LojaDeRoupa(tk.Tk(), conn, c)

def test_adicionar_estoque(loja_de_roupa):
    # Teste para adicionar um novo produto ao estoque
    loja_de_roupa.entry_produto.insert(0, "Camiseta")
    loja_de_roupa.entry_quantidade.insert(0, "10")
    loja_de_roupa.adicionar_estoque()
    loja_de_roupa.c.execute("SELECT * FROM estoque")
    estoque = loja_de_roupa.c.fetchall()
    print("Resultado da adição ao estoque:", estoque)
    assert ("Camiseta", 10) in [(row[1], row[2]) for row in estoque]


def test_atualizar_vendas(loja_de_roupa):
    # Teste para atualizar as vendas de um produto
    loja_de_roupa.entry_produto.insert(0, "Calça")
    loja_de_roupa.entry_quantidade.insert(0, "20")
    loja_de_roupa.adicionar_estoque()

    loja_de_roupa.entry_produto.insert(0, "Calça")
    loja_de_roupa.entry_vendido.insert(0, "5")
    loja_de_roupa.atualizar_vendas()

    loja_de_roupa.c.execute("SELECT quantidade FROM estoque WHERE produto=?", ("Calça",))
    quantidade_atualizada = loja_de_roupa.c.fetchone()[0]
    assert quantidade_atualizada == 15

def test_verificar_estoque(loja_de_roupa, monkeypatch):
        # Teste para verificar se o estoque está baixo
        loja_de_roupa.entry_produto.insert(0, "Blusa")
        loja_de_roupa.entry_quantidade.insert(0, "3")
        loja_de_roupa.adicionar_estoque()

        # Definir uma função de monkeypatch para capturar a saída
        messagebox_output = []
        def capture_messagebox(*args):
            messagebox_output.append(args[1])
        monkeypatch.setattr(tk.messagebox, 'showwarning', capture_messagebox)

        # Chamar verificar_estoque()
        loja_de_roupa.verificar_estoque()

        # Verificar se a mensagem esperada foi capturada
        assert "Blusa" in messagebox_output[0]
        assert "3" in messagebox_output[0]


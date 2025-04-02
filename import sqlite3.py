import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def conectar():
    """Conecta ao banco de dados."""
    return sqlite3.connect('clientes_varejo.db')

def criar_tabela():
    """Cria a tabela de clientes se ela não existir."""
    conn = conectar()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clientes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT,
            endereco TEXT,
            historico_compras TEXT
        )
    ''')
    conn.commit()
    conn.close()

def inserir_cliente():
    """Insere um novo cliente no banco de dados."""
    nome = entry_nome.get()
    email = entry_email.get()
    telefone = entry_telefone.get()
    endereco = entry_endereco.get()
    historico_compras = entry_historico_compras.get()

    if nome:
        conn = conectar()
        c = conn.cursor()
        try:
            c.execute('INSERT INTO clientes(nome, email, telefone, endereco, historico_compras) VALUES (?, ?, ?, ?, ?)', (nome, email, telefone, endereco, historico_compras))
            conn.commit()
            messagebox.showinfo('Sucesso', 'Cliente cadastrado com sucesso!')
            mostrar_clientes()
        except sqlite3.IntegrityError:
            messagebox.showerror('Erro', 'Erro ao cadastrar cliente.')
        finally:
            conn.close()
    else:
        messagebox.showerror('Erro', 'O nome do cliente é obrigatório.')

def mostrar_clientes():
    """Exibe os clientes na tabela."""
    for row in tree.get_children():
        tree.delete(row)
    conn = conectar()
    c = conn.cursor()
    c.execute('SELECT * FROM clientes')
    clientes = c.fetchall()
    for cliente in clientes:
        tree.insert("", "end", values=(cliente[0], cliente[1], cliente[2], cliente[3], cliente[4], cliente[5]))
    conn.close()

def delete_cliente():
    """Deleta um cliente selecionado."""
    dado_del = tree.selection()
    if dado_del:
        cliente_id = tree.item(dado_del)['values'][0]
        conn = conectar()
        c = conn.cursor()
        c.execute('DELETE FROM clientes WHERE id = ?', (cliente_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo('Sucesso', 'Cliente deletado.')
        mostrar_clientes()
    else:
        messagebox.showerror('Erro', 'Selecione um cliente para deletar.')

def editar_cliente():
    """Edita um cliente selecionado."""
    selecao = tree.selection()
    if selecao:
        cliente_id = tree.item(selecao)['values'][0]
        novo_nome = entry_nome.get()
        novo_email = entry_email.get()
        novo_telefone = entry_telefone.get()
        novo_endereco = entry_endereco.get()
        novo_historico_compras = entry_historico_compras.get()

        if novo_nome:
            conn = conectar()
            c = conn.cursor()
            c.execute('UPDATE clientes SET nome = ?, email = ?, telefone = ?, endereco = ?, historico_compras = ? WHERE id = ?', (novo_nome, novo_email, novo_telefone, novo_endereco, novo_historico_compras, cliente_id))
            conn.commit()
            conn.close()
            messagebox.showinfo('Sucesso', 'Dados do cliente atualizados.')
            mostrar_clientes()
        else:
            messagebox.showwarning('Aviso', 'O nome do cliente é obrigatório.')
    else:
        messagebox.showerror('Erro', 'Selecione um cliente para editar.')

# Interface Gráfica
root = tk.Tk()
root.title('Cadastro de Clientes - Varejo')

# Labels e Entradas
tk.Label(root, text='Nome:').grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text='Email:').grid(row=1, column=0)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1)

tk.Label(root, text='Telefone:').grid(row=2, column=0)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=2, column=1)

tk.Label(root, text='Endereço:').grid(row=3, column=0)
entry_endereco = tk.Entry(root)
entry_endereco.grid(row=3, column=1)

tk.Label(root, text='Histórico de Compras:').grid(row=4, column=0)
entry_historico_compras = tk.Entry(root)
entry_historico_compras.grid(row=4, column=1)

# Botões
tk.Button(root, text='Cadastrar', command=inserir_cliente).grid(row=5, column=0)
tk.Button(root, text='Editar', command=editar_cliente).grid(row=5, column=1)
tk.Button(root, text='Deletar', command=delete_cliente).grid(row=5, column=2)

# Tabela
tree = ttk.Treeview(root, columns=('ID', 'Nome', 'Email', 'Telefone', 'Endereço', 'Histórico de Compras'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Nome', text='Nome')
tree.heading('Email', text='Email')
tree.heading('Telefone', text='Telefone')
tree.heading('Endereço', text='Endereço')
tree.heading('Histórico de Compras', text='Histórico de Compras')
tree.grid(row=6, column=0, columnspan=3)

# Inicialização
criar_tabela()
mostrar_clientes()

root.mainloop()
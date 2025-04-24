from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from app.models import Product, Category, Supplier # Importa os modelos necessários
from app import db # Importa a instância do SQLAlchemy

# Cria uma instância de Blueprint para as rotas de estoque/produtos
# url_prefix='/estoque' significa que todas as rotas neste blueprint
# começarão com /estoque (ex: /estoque/produtos)
estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque.route('/produtos')
@login_required # Esta rota exige que o usuário esteja autenticado
def listar_produtos():
    """
    Rota para listar todos os produtos cadastrados em uma tabela.
    """
    # Consulta todos os produtos no banco de dados
    # Usamos .all() para obter uma lista de objetos Product
    # Podemos adicionar .order_by(Product.name) para ordenar por nome, por exemplo
    produtos = Product.query.all()

    # Renderiza o template de listagem de produtos, passando a lista de produtos para ele
    return render_template('estoque/produtos.html', title='Listar Produtos', produtos=produtos)

# --- Futuras rotas para adicionar, editar, excluir produtos aqui ---

# Exemplo de rota para adicionar produto (apenas esqueleto por enquanto)
# @estoque.route('/produtos/novo', methods=['GET', 'POST'])
# @login_required
# def adicionar_produto():
#     # form = ProductForm() # Precisamos criar este formulário depois
#     # ... lógica para adicionar ...
#     return render_template('estoque/adicionar_produto.html', title='Novo Produto', form=None) # Trocar None pelo form real

# Exemplo de rota para editar produto (apenas esqueleto por enquanto)
# @estoque.route('/produtos/editar/<int:product_id>', methods=['GET', 'POST'])
# @login_required
# def editar_produto(product_id):
#     # product = Product.query.get_or_404(product_id) # Busca o produto pelo ID
#     # form = ProductForm(obj=product) # Preenche o formulário com os dados do produto
#     # ... lógica para editar ...
#     return render_template('estoque/editar_produto.html', title='Editar Produto', form=None) # Trocar None pelo form real

# Exemplo de rota para excluir produto (apenas esqueleto por enquanto)
# @estoque.route('/produtos/excluir/<int:product_id>', methods=['POST'])
# @login_required
# def excluir_produto(product_id):
#     # product = Product.query.get_or_404(product_id)
#     # db.session.delete(product)
#     # db.session.commit()
#     # flash('Produto excluído com sucesso!', 'success')
#     return redirect(url_for('estoque.listar_produtos'))
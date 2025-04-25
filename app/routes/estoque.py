# app/routes/estoque.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
# Importa ProductForm
from app.forms import ProductForm
from app.models import Product, Category, Supplier # Importa os modelos necessários
from app import db # Importa a instância do SQLAlchemy
from datetime import datetime # Para a data da última atualização

# Cria uma instância de Blueprint para as rotas de estoque/produtos
estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque.route('/produtos')
@login_required
def listar_produtos():
    """
    Rota para listar todos os produtos cadastrados em uma tabela.
    """
    produtos = Product.query.all()
    return render_template('estoque/produtos.html', title='Listar Produtos', produtos=produtos)

@estoque.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    """
    Rota para adicionar um novo produto.
    Exibe o formulário (GET) ou processa o cadastro (POST).
    """
    form = ProductForm() # Cria uma instância do formulário de produto

    # Note que os QuerySelectFields no formulário (categoria e fornecedor)
    # já vêm populados automaticamente pelo QuerySelectField ao criar a instância do form,
    # pois definimos as query_factories lá em forms.py.
    # Não precisamos popular form.campo.choices aqui explicitamente para QuerySelectField.

    # Se o formulário for enviado (POST) e for válido
    if form.validate_on_submit():
        # Cria uma nova instância do modelo Product
        novo_produto = Product(
            code=form.code.data,
            name=form.name.data,
            price=form.price.data, # DecimalField retorna um objeto Decimal
            quantity_in_stock=form.quantity_in_stock.data,
            minimum_stock=form.minimum_stock.data if form.minimum_stock.data is not None else 0, # Lida com Optional
            # QuerySelectField retorna o objeto modelo selecionado (ou None se 'allow_blank=True' e nada for selecionado)
            category=form.category.data,
            supplier=form.supplier.data,
            last_updated=datetime.utcnow() # Define a data/hora atual
        )

        # Adiciona o novo produto à sessão do banco de dados
        db.session.add(novo_produto)
        # Salva as mudanças no banco de dados
        db.session.commit()

        flash(f'Produto "{novo_produto.name}" cadastrado com sucesso!', 'success')
        # Redireciona para a página de listagem de produtos
        return redirect(url_for('estoque.listar_produtos'))

    # Se a requisição for GET ou o formulário não for válido, renderiza o template com o formulário
    # Os erros de validação do formulário serão exibidos automaticamente no template onde os campos do form forem renderizados
    return render_template('estoque/adicionar_produto.html', title='Adicionar Novo Produto', form=form)

# --- Futuras rotas para editar, excluir produtos aqui ---
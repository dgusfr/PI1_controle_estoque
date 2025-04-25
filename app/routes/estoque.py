# app/routes/estoque.py

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
# Importa os novos formulários
from app.forms import ProductForm, CategoryForm, SupplierForm
from app.models import Product, Category, Supplier
from app import db
from datetime import datetime

# Cria uma instância de Blueprint para as rotas de estoque/produtos
estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

@estoque.route('/produtos')
@login_required
def listar_produtos():
    """Rota para listar todos os produtos."""
    produtos = Product.query.all()
    return render_template('estoque/produtos.html', title='Listar Produtos', produtos=produtos)

@estoque.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    """Rota para adicionar um novo produto."""
    form = ProductForm()
    if form.validate_on_submit():
        novo_produto = Product(
            code=form.code.data,
            name=form.name.data,
            price=form.price.data,
            quantity_in_stock=form.quantity_in_stock.data,
            minimum_stock=form.minimum_stock.data if form.minimum_stock.data is not None else 0,
            category=form.category.data, # QuerySelectField retorna o objeto
            supplier=form.supplier.data, # QuerySelectField retorna o objeto
            last_updated=datetime.utcnow()
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash(f'Produto "{novo_produto.name}" cadastrado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_produtos'))
    return render_template('estoque/adicionar_produto.html', title='Adicionar Novo Produto', form=form)

# --- Novas Rotas para Categoria ---

@estoque.route('/categorias')
@login_required
def listar_categorias():
    """
    Rota para listar todas as categorias cadastradas.
    """
    categorias = Category.query.order_by(Category.name).all() # Ordena por nome
    return render_template('estoque/listar_categorias.html', title='Listar Categorias', categorias=categorias)

@estoque.route('/categorias/novo', methods=['GET', 'POST'])
@login_required
def adicionar_categoria():
    """
    Rota para adicionar uma nova categoria.
    """
    form = CategoryForm()
    if form.validate_on_submit():
        nova_categoria = Category(name=form.name.data)
        db.session.add(nova_categoria)
        db.session.commit()
        flash(f'Categoria "{nova_categoria.name}" cadastrada com sucesso!', 'success')
        # Redireciona para a listagem de categorias
        return redirect(url_for('estoque.listar_categorias'))
    return render_template('estoque/adicionar_categoria.html', title='Adicionar Nova Categoria', form=form)


# --- Novas Rotas para Fornecedor ---

@estoque.route('/fornecedores')
@login_required
def listar_fornecedores():
    """
    Rota para listar todos os fornecedores cadastrados.
    """
    fornecedores = Supplier.query.order_by(Supplier.name).all() # Ordena por nome
    return render_template('estoque/listar_fornecedores.html', title='Listar Fornecedores', fornecedores=fornecedores)


@estoque.route('/fornecedores/novo', methods=['GET', 'POST'])
@login_required
def adicionar_fornecedor():
    """
    Rota para adicionar um novo fornecedor.
    """
    form = SupplierForm()
    if form.validate_on_submit():
        novo_fornecedor = Supplier(
            name=form.name.data,
            contact_info=form.contact_info.data if form.contact_info.data else None # Salva None se Optional e vazio
            )
        db.session.add(novo_fornecedor)
        db.session.commit()
        flash(f'Fornecedor "{novo_fornecedor.name}" cadastrado com sucesso!', 'success')
        # Redireciona para a listagem de fornecedores
        return redirect(url_for('estoque.listar_fornecedores'))
    return render_template('estoque/adicionar_fornecedor.html', title='Adicionar Novo Fornecedor', form=form)


# --- Futuras rotas para editar/excluir categorias/fornecedores aqui ---
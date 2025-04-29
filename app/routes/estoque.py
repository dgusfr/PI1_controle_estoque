from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required
# Importar FlaskForm para o formulário simples na listagem (se ainda não estiver)
from flask_wtf import FlaskForm
from app.forms import ProductForm, CategoryForm, SupplierForm
from app.models import Product, Category, Supplier
from app import db
from datetime import datetime

# Cria uma instância de Blueprint para as rotas de estoque/produtos
estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

# --- Rotas de Produtos (existente) ---
@estoque.route('/produtos')
@login_required
def listar_produtos():
    """Rota para listar todos os produtos."""
    produtos = Product.query.all()
    form_exclusao = FlaskForm() # Para o botão excluir POST
    return render_template('estoque/produtos.html', title='Listar Produtos', produtos=produtos, form=form_exclusao)

@estoque.route('/produtos/novo', methods=['GET', 'POST'])
@login_required
def adicionar_produto():
    """Rota para adicionar um novo produto."""
    form = ProductForm()
    if form.validate_on_submit():
        # ... lógica de adicionar produto ...
        novo_produto = Product(
            code=form.code.data,
            name=form.name.data,
            price=form.price.data,
            quantity_in_stock=form.quantity_in_stock.data,
            minimum_stock=form.minimum_stock.data if form.minimum_stock.data is not None else 0,
            category=form.category.data,
            supplier=form.supplier.data,
            last_updated=datetime.utcnow()
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash(f'Produto "{novo_produto.name}" cadastrado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_produtos'))
    return render_template('estoque/adicionar_produto.html', title='Adicionar Novo Produto', form=form)

@estoque.route('/produtos/editar/<int:product_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(product_id):
    """Rota para editar um produto existente."""
    produto = Product.query.get_or_404(product_id)
    form = ProductForm(obj=produto)
    if form.validate_on_submit():
        # ... lógica de editar produto ...
        form.populate_obj(produto)
        produto.last_updated = datetime.utcnow()
        db.session.commit()
        flash(f'Produto "{produto.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_produtos'))
    return render_template('estoque/editar_produto.html', title='Editar Produto', form=form, produto=produto) # Passar 'produto' é opcional, mas útil

@estoque.route('/produtos/excluir/<int:product_id>', methods=['POST'])
@login_required
def excluir_produto(product_id):
    """Rota para excluir um produto existente."""
    produto = Product.query.get_or_404(product_id)
    db.session.delete(produto)
    db.session.commit()
    flash(f'Produto "{produto.name}" excluído com sucesso.', 'info')
    return redirect(url_for('estoque.listar_produtos'))


# --- Rotas de Categoria (existente e novas) ---

@estoque.route('/categorias')
@login_required
def listar_categorias():
    """Rota para listar todas as categorias."""
    categorias = Category.query.order_by(Category.name).all()
    form_exclusao = FlaskForm() # Para o botão excluir POST
    return render_template('estoque/listar_categorias.html', title='Listar Categorias', categorias=categorias, form=form_exclusao) # Passar o form

@estoque.route('/categorias/novo', methods=['GET', 'POST'])
@login_required
def adicionar_categoria():
    """Rota para adicionar nova categoria."""
    form = CategoryForm()
    if form.validate_on_submit():
        # ... lógica de adicionar categoria ...
        nova_categoria = Category(name=form.name.data)
        db.session.add(nova_categoria)
        db.session.commit()
        flash(f'Categoria "{nova_categoria.name}" cadastrada com sucesso!', 'success')
        return redirect(url_for('estoque.listar_categorias'))
    return render_template('estoque/adicionar_categoria.html', title='Adicionar Nova Categoria', form=form)

# --- Nova Rota para Edição de Categoria ---
@estoque.route('/categorias/editar/<int:category_id>', methods=['GET', 'POST'])
@login_required
def editar_categoria(category_id):
    """
    Rota para editar uma categoria existente.
    """
    categoria = Category.query.get_or_404(category_id)
    # Passamos o objeto 'categoria' para preencher o formulário
    form = CategoryForm(obj=categoria)
    if form.validate_on_submit():
        # Atualiza o objeto 'categoria' com os dados do formulário
        form.populate_obj(categoria)
        db.session.commit()
        flash(f'Categoria "{categoria.name}" atualizada com sucesso!', 'success')
        return redirect(url_for('estoque.listar_categorias'))
    # No método GET, renderiza o formulário preenchido
    return render_template('estoque/editar_categoria.html', title='Editar Categoria', form=form, categoria=categoria)


# --- Nova Rota para Exclusão de Categoria ---
@estoque.route('/categorias/excluir/<int:category_id>', methods=['POST'])
@login_required
def excluir_categoria(category_id):
    """
    Rota para excluir uma categoria existente.
    Aceita apenas requisições POST.
    """
    categoria = Category.query.get_or_404(category_id)

    # TODO: Considerar o que fazer com produtos que usam esta categoria antes de excluir
    # Por exemplo: impedir exclusão se houver produtos associados, ou definir produtos para 'N/A' categoria.
    # Por enquanto, SQLAlchemy pode impedir a exclusão (devido à ForeignKey) se houver produtos.

    db.session.delete(categoria)
    db.session.commit()
    flash(f'Categoria "{categoria.name}" excluída com sucesso.', 'info')
    return redirect(url_for('estoque.listar_categorias'))


# --- Rotas de Fornecedor (existente e novas) ---

@estoque.route('/fornecedores')
@login_required
def listar_fornecedores():
    """Rota para listar todos os fornecedores."""
    fornecedores = Supplier.query.order_by(Supplier.name).all()
    form_exclusao = FlaskForm() # Para o botão excluir POST
    return render_template('estoque/listar_fornecedores.html', title='Listar Fornecedores', fornecedores=fornecedores, form=form_exclusao) # Passar o form


@estoque.route('/fornecedores/novo', methods=['GET', 'POST'])
@login_required
def adicionar_fornecedor():
    """Rota para adicionar novo fornecedor."""
    form = SupplierForm()
    if form.validate_on_submit():
        # ... lógica de adicionar fornecedor ...
        novo_fornecedor = Supplier(
            name=form.name.data,
            contact_info=form.contact_info.data if form.contact_info.data else None
            )
        db.session.add(novo_fornecedor)
        db.session.commit()
        flash(f'Fornecedor "{novo_fornecedor.name}" cadastrado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_fornecedores'))
    return render_template('estoque/adicionar_fornecedor.html', title='Adicionar Novo Fornecedor', form=form)


# --- Nova Rota para Edição de Fornecedor ---
@estoque.route('/fornecedores/editar/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def editar_fornecedor(supplier_id):
    """
    Rota para editar um fornecedor existente.
    """
    fornecedor = Supplier.query.get_or_404(supplier_id)
    # Passamos o objeto 'fornecedor' para preencher o formulário
    form = SupplierForm(obj=fornecedor)
    if form.validate_on_submit():
        # Atualiza o objeto 'fornecedor' com os dados do formulário
        form.populate_obj(fornecedor)
        db.session.commit()
        flash(f'Fornecedor "{fornecedor.name}" atualizado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_fornecedores'))
    # No método GET, renderiza o formulário preenchido
    return render_template('estoque/editar_fornecedor.html', title='Editar Fornecedor', form=form, fornecedor=fornecedor)

# --- Nova Rota para Exclusão de Fornecedor ---
@estoque.route('/fornecedores/excluir/<int:supplier_id>', methods=['POST'])
@login_required
def excluir_fornecedor(supplier_id):
    """
    Rota para excluir um fornecedor existente.
    Aceita apenas requisições POST.
    """
    fornecedor = Supplier.query.get_or_404(supplier_id)

    # TODO: Considerar o que fazer com produtos que usam este fornecedor antes de excluir
    # Por exemplo: impedir exclusão se houver produtos associados, ou definir produtos para 'N/A' fornecedor.
    # Por enquanto, SQLAlchemy pode impedir a exclusão (devido à ForeignKey) se houver produtos.

    db.session.delete(fornecedor)
    db.session.commit()
    flash(f'Fornecedor "{fornecedor.name}" excluído com sucesso.', 'info')
    return redirect(url_for('estoque.listar_fornecedores'))

# --- Futuras rotas para movimentações de estoque, vendas, relatórios aqui ---
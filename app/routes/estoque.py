from flask import Blueprint, render_template, request, flash, redirect, url_for, abort # Importar abort
from flask_login import login_required
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
            category=form.category.data,
            supplier=form.supplier.data,
            last_updated=datetime.utcnow()
        )
        db.session.add(novo_produto)
        db.session.commit()
        flash(f'Produto "{novo_produto.name}" cadastrado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_produtos'))
    return render_template('estoque/adicionar_produto.html', title='Adicionar Novo Produto', form=form)


# --- Nova Rota para Edição de Produto (RF03) ---
@estoque.route('/produtos/editar/<int:product_id>', methods=['GET', 'POST'])
@login_required
def editar_produto(product_id):
    """
    Rota para editar um produto existente.
    Exibe o formulário preenchido (GET) ou processa a atualização (POST).
    """
    # Busca o produto no banco de dados pelo ID fornecido na URL.
    # get_or_404 retorna o objeto Product ou uma página de erro 404 se não encontrado.
    produto = Product.query.get_or_404(product_id)

    # Cria uma instância do formulário.
    # Se for uma requisição GET, o formulário é preenchido com os dados do objeto 'produto'
    # (graças ao argumento obj=produto).
    # Se for uma requisição POST, o formulário será preenchido com os dados enviados pelo usuário.
    form = ProductForm(obj=produto)

    # Se o formulário for enviado (POST) e for válido
    if form.validate_on_submit():
        # Atualiza os atributos do objeto produto existente com os dados do formulário.
        # Note que não criamos um novo objeto Product.
        form.populate_obj(produto) # Este método Flask-WTF atualiza o objeto diretamente com os dados validados do form

        # Atualiza a data da última atualização
        produto.last_updated = datetime.utcnow()

        # As mudanças já estão na sessão do banco de dados porque o objeto 'produto'
        # foi buscado da sessão. Basta commitar.
        db.session.commit()

        flash(f'Produto "{produto.name}" atualizado com sucesso!', 'success')
        # Redireciona de volta para a página de listagem
        return redirect(url_for('estoque.listar_produtos'))

    # Se a requisição for GET ou o formulário não for válido, renderiza o template de edição
    # Passamos o objeto 'produto' e o 'form' para o template
    return render_template('estoque/editar_produto.html', title='Editar Produto', form=form, produto=produto)


# --- Nova Rota para Exclusão de Produto (RF03) ---
# Usamos o método POST para exclusão para evitar exclusões acidentais via links de navegação
@estoque.route('/produtos/excluir/<int:product_id>', methods=['POST'])
@login_required
def excluir_produto(product_id):
    """
    Rota para excluir um produto existente.
    Aceita apenas requisições POST.
    """
    # Busca o produto a ser excluído
    produto = Product.query.get_or_404(product_id)

    # Remove o objeto da sessão do banco de dados
    db.session.delete(produto)
    # Salva as mudanças (executa a exclusão no banco)
    db.session.commit()

    flash(f'Produto "{produto.name}" excluído com sucesso.', 'info') # 'info' para exclusão
    # Redireciona de volta para a página de listagem
    return redirect(url_for('estoque.listar_produtos'))


# --- Rotas existentes para Categoria e Fornecedor ---

@estoque.route('/categorias')
@login_required
def listar_categorias():
    """Rota para listar todas as categorias."""
    categorias = Category.query.order_by(Category.name).all()
    return render_template('estoque/listar_categorias.html', title='Listar Categorias', categorias=categorias)

@estoque.route('/categorias/novo', methods=['GET', 'POST'])
@login_required
def adicionar_categoria():
    """Rota para adicionar nova categoria."""
    form = CategoryForm()
    if form.validate_on_submit():
        nova_categoria = Category(name=form.name.data)
        db.session.add(nova_categoria)
        db.session.commit()
        flash(f'Categoria "{nova_categoria.name}" cadastrada com sucesso!', 'success')
        return redirect(url_for('estoque.listar_categorias'))
    return render_template('estoque/adicionar_categoria.html', title='Adicionar Nova Categoria', form=form)


@estoque.route('/fornecedores')
@login_required
def listar_fornecedores():
    """Rota para listar todos os fornecedores."""
    fornecedores = Supplier.query.order_by(Supplier.name).all()
    return render_template('estoque/listar_fornecedores.html', title='Listar Fornecedores', fornecedores=fornecedores)


@estoque.route('/fornecedores/novo', methods=['GET', 'POST'])
@login_required
def adicionar_fornecedor():
    """Rota para adicionar novo fornecedor."""
    form = SupplierForm()
    if form.validate_on_submit():
        novo_fornecedor = Supplier(
            name=form.name.data,
            contact_info=form.contact_info.data if form.contact_info.data else None
            )
        db.session.add(novo_fornecedor)
        db.session.commit()
        flash(f'Fornecedor "{novo_fornecedor.name}" cadastrado com sucesso!', 'success')
        return redirect(url_for('estoque.listar_fornecedores'))
    return render_template('estoque/adicionar_fornecedor.html', title='Adicionar Novo Fornecedor', form=form)

@estoque.route('/produtos')
@login_required
def listar_produtos():
    """Rota para listar todos os produtos."""
    produtos = Product.query.all()
    # Cria uma instância de um formulário simples (sem campos visíveis) apenas para gerar o token CSRF para o formulário de exclusão
    form_exclusao = FlaskForm()
    # Passa o formulário para o template
    return render_template('estoque/produtos.html', title='Listar Produtos', produtos=produtos, form=form_exclusao)
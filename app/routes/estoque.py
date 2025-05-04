# app/routes/estoque.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, abort
from flask_login import login_required
from flask_wtf import FlaskForm # Importar FlaskForm se usado em listagens
# Importar StockMovementForm
from app.forms import ProductForm, CategoryForm, SupplierForm, StockMovementForm
from app.models import Product, Category, Supplier, StockMovement # Importar StockMovement
from app import db
from datetime import datetime

# Cria uma instância de Blueprint para as rotas de estoque/produtos
estoque = Blueprint('estoque', __name__, url_prefix='/estoque')

# --- Rotas de Produtos (existente) ---
# ... listar_produtos, adicionar_produto, editar_produto, excluir_produto ...

# --- Rotas de Categoria (existente) ---
# ... listar_categorias, adicionar_categoria, editar_categoria, excluir_categoria ...

# --- Rotas de Fornecedor (existente) ---
# ... listar_fornecedores, adicionar_fornecedor, editar_fornecedor, excluir_fornecedor ...


# --- Novas Rotas para Movimentação de Estoque (RF04, RF05) ---

@estoque.route('/movimentar/entrada', methods=['GET', 'POST'])
@login_required
def movimentar_entrada():
    """
    Rota para registrar uma ENTRADA de estoque.
    """
    form = StockMovementForm()
    # Define o tipo de movimento no campo oculto do formulário
    form.movement_type.data = 'entrada'

    if form.validate_on_submit():
        # Busca o produto selecionado (o QuerySelectField.data já é o objeto)
        produto = form.product.data
        quantidade_movimentada = form.quantity.data

        # Atualiza a quantidade em estoque do produto (adiciona)
        produto.quantity_in_stock += quantidade_movimentada
        produto.last_updated = datetime.utcnow() # Atualiza data de modificação

        # Cria um novo registro de movimentação
        movimentacao = StockMovement(
            date=datetime.utcnow(),
            movement_type='entrada',
            quantity=quantidade_movimentada,
            # O motivo é opcional para entradas, então pode ser None
            reason=form.reason.data if form.reason.data else None,
            product=produto # Associa a movimentação ao produto
        )

        # Adiciona as mudanças (produto atualizado e nova movimentação) à sessão
        db.session.add(produto) # O SQLAlchemy já rastreia o produto se ele veio de uma query, mas adicionar explicitamente não faz mal
        db.session.add(movimentacao)
        # Salva tudo no banco
        db.session.commit()

        flash(f'Entrada de {quantidade_movimentada} unidades de "{produto.name}" registrada com sucesso!', 'success')
        # Redireciona para a listagem de produtos ou para uma página de histórico de movimentação
        return redirect(url_for('estoque.listar_produtos')) # Podemos criar uma rota para histórico depois

    # Se a requisição for GET ou validação falhar, renderiza o template
    # Passamos o tipo de movimento e o formulário para o template
    return render_template('estoque/movimentar_estoque.html', title='Registrar Entrada de Estoque', form=form, movement_type='entrada')


@estoque.route('/movimentar/saida', methods=['GET', 'POST'])
@login_required
def movimentar_saida():
    """
    Rota para registrar uma SAÍDA de estoque.
    """
    form = StockMovementForm()
    # Define o tipo de movimento no campo oculto do formulário
    form.movement_type.data = 'saida'

    if form.validate_on_submit():
        # Busca o produto selecionado
        produto = form.product.data
        quantidade_movimentada = form.quantity.data

        # A validação de quantidade suficiente já foi feita no validador customizado do formulário,
        # mas podemos adicionar uma verificação extra aqui por segurança, se desejar.
        if quantidade_movimentada > produto.quantity_in_stock:
             flash(f'Erro: Quantidade de saída ({quantidade_movimentada}) maior que o estoque disponível ({produto.quantity_in_stock}) para "{produto.name}".', 'danger')
             # Retorna para a página, permitindo ao usuário corrigir o formulário
             return render_template('estoque/movimentar_estoque.html', title='Registrar Saída de Estoque', form=form, movement_type='saida')


        # Atualiza a quantidade em estoque do produto (subtrai)
        produto.quantity_in_stock -= quantidade_movimentada
        produto.last_updated = datetime.utcnow() # Atualiza data de modificação

        # Cria um novo registro de movimentação
        movimentacao = StockMovement(
            date=datetime.utcnow(),
            movement_type='saida',
            quantity=quantidade_movimentada,
            # O motivo é obrigatório para saídas (validado no formulário)
            reason=form.reason.data, # reason.data já vem validado como não vazio para saídas
            product=produto # Associa a movimentação ao produto
        )

        # Adiciona as mudanças (produto atualizado e nova movimentação) à sessão
        db.session.add(produto)
        db.session.add(movimentacao)
        # Salva tudo no banco
        db.session.commit()

        flash(f'Saída de {quantidade_movimentada} unidades de "{produto.name}" registrada com sucesso!', 'success')
        # Redireciona para a listagem de produtos ou para uma página de histórico
        return redirect(url_for('estoque.listar_produtos')) # Podemos criar uma rota para histórico depois

    # Se a requisição for GET ou validação falhar, renderiza o template
    return render_template('estoque/movimentar_estoque.html', title='Registrar Saída de Estoque', form=form, movement_type='saida')
# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, IntegerField, TextAreaField, HiddenField # Importar HiddenField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError

from wtforms.ext.sqlalchemy.fields import QuerySelectField

# Importamos os modelos Product e StockMovement (se necessário para validação futura)
from app.models import Category, Supplier, Product, StockMovement, db

# --- Formulários existentes (LoginForm, ProductForm, CategoryForm, SupplierForm) ---
# ... mantenha os códigos existentes desses formulários ...

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

def get_categories():
     return db.session.query(Category).order_by(Category.name).all()

def get_suppliers():
     return db.session.query(Supplier).order_by(Supplier.name).all()

# Nova função de query para buscar produtos
def get_products():
    """Retorna todos os produtos ordenados por nome."""
    return db.session.query(Product).order_by(Product.name).all()


class ProductForm(FlaskForm):
    # ... código do ProductForm ...
    code = StringField('Código do Produto', validators=[DataRequired(), Length(max=64)])
    name = StringField('Nome do Produto', validators=[DataRequired(), Length(max=128)])
    price = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0, message='O preço deve ser um número positivo.')], places=2)
    quantity_in_stock = IntegerField('Quantidade em Estoque', validators=[DataRequired(), NumberRange(min=0, message='A quantidade deve ser um número positivo ou zero.')])
    minimum_stock = IntegerField('Estoque Mínimo', validators=[Optional(), NumberRange(min=0, message='O estoque mínimo deve ser um número positivo ou zero.')])
    category = QuerySelectField('Categoria', query_factory=get_categories, get_label='name', allow_blank=True, blank_text='-- Selecione uma Categoria --')
    supplier = QuerySelectField('Fornecedor', query_factory=get_suppliers, get_label='name', allow_blank=True, blank_text='-- Selecione um Fornecedor --')
    submit = SubmitField('Salvar Produto')

class CategoryForm(FlaskForm):
     # ... código do CategoryForm ...
     name = StringField('Nome da Categoria', validators=[DataRequired(), Length(max=64)])
     submit = SubmitField('Salvar Categoria')
     def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
             raise ValidationError('Já existe uma categoria com este nome. Por favor, escolha um nome diferente.')

class SupplierForm(FlaskForm):
     # ... código do SupplierForm ...
     name = StringField('Nome do Fornecedor', validators=[DataRequired(), Length(max=64)])
     contact_info = TextAreaField('Informações de Contato', validators=[Optional(), Length(max=128)])
     submit = SubmitField('Salvar Fornecedor')
     def validate_name(self, name):
        supplier = Supplier.query.filter_by(name=name.data).first()
        if supplier is not None:
             raise ValidationError('Já existe um fornecedor com este nome. Por favor, escolha um nome diferente.')


# --- Novo Formulário para Movimentação de Estoque ---

class StockMovementForm(FlaskForm):
    """
    Formulário para registrar uma movimentação de estoque (entrada ou saída).
    """
    # Campo para selecionar o produto a ser movimentado
    product = QuerySelectField('Produto', query_factory=get_products, get_label='name', validators=[DataRequired()], blank_text='-- Selecione um Produto --')

    # Campo para a quantidade movimentada
    quantity = IntegerField('Quantidade', validators=[DataRequired(), NumberRange(min=1, message='A quantidade deve ser um número positivo.')])

    # Campo para o motivo da movimentação (obrigatório para saídas, opcional para entradas)
    # Usaremos validação customizada ou na rota para tornar obrigatório apenas na saída
    reason = TextAreaField('Motivo (obrigatório para saídas)', validators=[Optional(), Length(max=128)])

    # Campo oculto para identificar o tipo de movimento ('entrada' ou 'saida')
    # O valor será definido na rota que renderiza o formulário ou na rota que processa
    movement_type = HiddenField(validators=[DataRequired()]) # Campo oculto, mas obrigatório

    submit = SubmitField('Registrar Movimentação')

    # Validador customizado para o motivo (tornar obrigatório se for saída)
    def validate_reason(self, reason):
        # A validação só faz sentido se o tipo de movimento for 'saida'
        if self.movement_type.data == 'saida' and not reason.data:
             raise ValidationError('O motivo é obrigatório para saídas de estoque.')

    # Validador customizado para a quantidade na saída (não pode ser maior que o estoque atual)
    def validate_quantity(self, quantity):
        # A validação só faz sentido se o tipo de movimento for 'saida' e a quantidade for fornecida
        if self.movement_type.data == 'saida' and quantity.data is not None:
            # Precisamos acessar o produto selecionado para verificar o estoque atual
            # O objeto Product selecionado está em self.product.data
            produto_selecionado = self.product.data
            if produto_selecionado and quantity.data > produto_selecionado.quantity_in_stock:
                 raise ValidationError(f'Quantidade insuficiente em estoque. Disponível: {produto_selecionado.quantity_in_stock}.')
# app/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, IntegerField, TextAreaField # Adicione TextAreaField se quiser mais espaço para contato do fornecedor
from wtforms.validators import DataRequired, Length, NumberRange, Optional, ValidationError # Importar ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField

# Importamos os modelos Category e Supplier para usar no QuerySelectField e para validação
from app.models import Category, Supplier, db

# --- Formulários existentes (LoginForm, ProductForm) ---
class LoginForm(FlaskForm):
    # ... código do LoginForm ...
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')

# Funções de query para QuerySelectField
def get_categories():
    # ... código da função get_categories ...
     return db.session.query(Category).order_by(Category.name).all()

def get_suppliers():
    # ... código da função get_suppliers ...
     return db.session.query(Supplier).order_by(Supplier.name).all()

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


# --- Novos Formulários para Categoria e Fornecedor ---

class CategoryForm(FlaskForm):
    """
    Formulário para adicionar ou editar uma categoria.
    """
    name = StringField('Nome da Categoria', validators=[DataRequired(), Length(max=64)])
    submit = SubmitField('Salvar Categoria')

    # Validador customizado para verificar se o nome da categoria já existe
    def validate_name(self, name):
        category = Category.query.filter_by(name=name.data).first()
        if category is not None:
            # Se encontrou uma categoria com o mesmo nome E ela não é a categoria que estamos editando
            # (útil para reuso deste formulário na edição)
            # Para adicionar, basta verificar se category is not None
             raise ValidationError('Já existe uma categoria com este nome. Por favor, escolha um nome diferente.')


class SupplierForm(FlaskForm):
    """
    Formulário para adicionar ou editar um fornecedor.
    """
    name = StringField('Nome do Fornecedor', validators=[DataRequired(), Length(max=64)])
    contact_info = TextAreaField('Informações de Contato', validators=[Optional(), Length(max=128)]) # Campo opcional para contato
    submit = SubmitField('Salvar Fornecedor')

    # Validador customizado para verificar se o nome do fornecedor já existe
    def validate_name(self, name):
        supplier = Supplier.query.filter_by(name=name.data).first()
        if supplier is not None:
            # Se encontrou um fornecedor com o mesmo nome E ele não é o fornecedor que estamos editando
            # Para adicionar, basta verificar se supplier is not None
             raise ValidationError('Já existe um fornecedor com este nome. Por favor, escolha um nome diferente.')
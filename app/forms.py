# app/forms.py

from flask_wtf import FlaskForm
# Importamos novos tipos de campo para Categoria/Fornecedor (SelectField)
# e para Preço (DecimalField), além de IntegerField para quantidade
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange, Optional
# Importamos QuerySelectField para facilitar a seleção de modelos do SQLAlchemy
from wtforms.ext.sqlalchemy.fields import QuerySelectField

# Importamos os modelos Category e Supplier para usar no QuerySelectField
from app.models import Category, Supplier, db # Importar db também para as queries


class LoginForm(FlaskForm):
    """
    Formulário de login.
    """
    username = StringField('Nome de Usuário', validators=[DataRequired(), Length(min=2, max=64)])
    password = PasswordField('Senha', validators=[DataRequired()])
    remember_me = BooleanField('Lembrar-me')
    submit = SubmitField('Entrar')


# Funções de query para QuerySelectField (buscam dados no banco)
# Serão usadas nos campos de Categoria e Fornecedor no ProductForm
def get_categories():
    """Retorna todas as categorias ordenadas por nome."""
    return db.session.query(Category).order_by(Category.name).all()

def get_suppliers():
    """Retorna todos os fornecedores ordenados por nome."""
    return db.session.query(Supplier).order_by(Supplier.name).all()

class ProductForm(FlaskForm):
    """
    Formulário para adicionar ou editar um produto.
    """
    code = StringField('Código do Produto', validators=[DataRequired(), Length(max=64)])
    name = StringField('Nome do Produto', validators=[DataRequired(), Length(max=128)])
    # Usamos DecimalField para preço para garantir precisão monetária
    # NumberRange garante que o valor seja positivo
    price = DecimalField('Preço', validators=[DataRequired(), NumberRange(min=0, message='O preço deve ser um número positivo.')], places=2) # places=2 para 2 casas decimais
    # IntegerField para quantidade e estoque mínimo
    # Optional() permite que o campo seja vazio se não for obrigatório
    # NumberRange garante que o valor seja positivo ou zero (min=0)
    quantity_in_stock = IntegerField('Quantidade em Estoque', validators=[DataRequired(), NumberRange(min=0, message='A quantidade deve ser um número positivo ou zero.')])
    minimum_stock = IntegerField('Estoque Mínimo', validators=[Optional(), NumberRange(min=0, message='O estoque mínimo deve ser um número positivo ou zero.')])

    # Usamos QuerySelectField para selecionar Categoria e Fornecedor do banco de dados
    # query_factory aponta para a função que busca os dados
    # get_label define qual atributo do objeto será exibido na lista
    # allow_blank=True permite que a seleção seja opcional (ou que haja uma opção "Nenhum")
    # blank_text define o texto para a opção em branco
    category = QuerySelectField('Categoria', query_factory=get_categories, get_label='name', allow_blank=True, blank_text='-- Selecione uma Categoria --')
    supplier = QuerySelectField('Fornecedor', query_factory=get_suppliers, get_label='name', allow_blank=True, blank_text='-- Selecione um Fornecedor --')

    submit = SubmitField('Salvar Produto')
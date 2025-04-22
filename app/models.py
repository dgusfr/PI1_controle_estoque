from app import db 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash 
from flask_login import UserMixin
from decimal import Decimal 

# Tabela auxiliar para a relação muitos-para-muitos entre Produtos e Fornecedores (opcional, depende de como você quer modelar)
# Neste modelo inicial, Product tem apenas UM fornecedor (db.ForeignKey),
# mas se um produto pudesse ter múltiplos fornecedores, precisaríamos de uma tabela intermediária.
# Por enquanto, vamos manter a relação um-para-muitos (Um fornecedor tem muitos produtos).


class User(UserMixin, db.Model):
    """
    Modelo para representar um usuário do sistema.
    Integrado com Flask-Login via UserMixin.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), default='user') # Ex: 'admin', 'manager', 'user'
    is_active = db.Column(db.Boolean, default=True) # Para habilitar/desabilitar usuários

    # Relacionamento inverso: Obter as vendas associadas a este usuário
    sales = db.relationship('Sale', backref='seller', lazy='dynamic')

    def set_password(self, password):
        """Define a senha criptografando-a."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica se a senha fornecida corresponde à hash armazenada."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """Representação do objeto User."""
        return f'<User {self.username}>'

    # Métodos necessários para Flask-Login (já fornecidos por UserMixin, mas bom saber)
    # is_authenticated, is_active, is_anonymous, get_id()


class Category(db.Model):
    """
    Modelo para representar uma categoria de produto.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)

    # Relacionamento inverso: Obter os produtos desta categoria
    products = db.relationship('Product', backref='category', lazy='dynamic')

    def __repr__(self):
        """Representação do objeto Category."""
        return f'<Category {self.name}>'

class Supplier(db.Model):
    """
    Modelo para representar um fornecedor de produto.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    contact_info = db.Column(db.String(128)) # Opcional: email, telefone, etc.

    # Relacionamento inverso: Obter os produtos deste fornecedor
    products = db.relationship('Product', backref='supplier', lazy='dynamic')

    def __repr__(self):
        """Representação do objeto Supplier."""
        return f'<Supplier {self.name}>'

class Product(db.Model):
    """
    Modelo para representar um produto no estoque.
    """
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), unique=True, nullable=False) 
    name = db.Column(db.String(128), nullable=False)             
    price = db.Column(db.Numeric(10, 2), nullable=False)         
    quantity_in_stock = db.Column(db.Integer, default=0)       
    minimum_stock = db.Column(db.Integer, default=5)           
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    # Chaves estrangeiras para os relacionamentos (RF01)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'))

    # Relacionamento inverso: Obter os itens de venda associados a este produto
    sales_items = db.relationship('SaleItem', backref='product', lazy='dynamic')

    # Relacionamento inverso: Obter as movimentações de estoque associadas a este produto
    stock_movements = db.relationship('StockMovement', backref='product', lazy='dynamic')


    def __repr__(self):
        """Representação do objeto Product."""
        return f'<Product {self.code} - {self.name}>'

# --- Modelos adicionais (para serem implementados depois) ---

class Sale(db.Model):
    """
    Modelo para representar uma venda.
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # Data da venda (RF07, RF15)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)         # Valor total da venda (RF07)
    amount_paid = db.Column(db.Numeric(10, 2))                          # Valor pago pelo cliente (RF08)
    change = db.Column(db.Numeric(10, 2))                               # Troco calculado (RF08)

    # Chave estrangeira para o usuário que realizou a venda (RF15)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relacionamento: Obter os itens de venda associados a esta venda
    items = db.relationship('SaleItem', backref='sale', lazy='dynamic', cascade='all, delete-orphan') # cascade para deletar itens ao deletar venda

    def __repr__(self):
        """Representação do objeto Sale."""
        return f'<Sale {self.id} - {self.date.strftime("%Y-%m-%d %H:%M")}>'

class SaleItem(db.Model):
    """
    Modelo para representar um item individual dentro de uma venda.
    """
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)                  # Quantidade vendida do produto (RF07)
    price_per_item = db.Column(db.Numeric(10, 2), nullable=False)     # Preço unitário do produto no momento da venda (pode ser diferente do preço atual do produto)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)           # Subtotal para este item (quantidade * preço_por_item)

    # Chaves estrangeiras
    sale_id = db.Column(db.Integer, db.ForeignKey('sale.id'), nullable=False)        # Venda a que este item pertence
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # Produto vendido

    def __repr__(self):
        """Representação do objeto SaleItem."""
        return f'<SaleItem {self.id} - Product: {self.product_id} Qty: {self.quantity}>'


class StockMovement(db.Model):
    """
    Modelo para registrar movimentações de estoque (entrada/saída).
    """
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) # Data da movimentação (RF04, RF05, RF15)
    movement_type = db.Column(db.String(10), nullable=False)             # 'entrada' ou 'saida' (RF04, RF05)
    quantity = db.Column(db.Integer, nullable=False)                   # Quantidade movimentada (RF04, RF05)
    reason = db.Column(db.String(128))                                   # Motivo da saída (RF05)

    # Chave estrangeira para o produto movimentado
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False) # RF04, RF05

    def __repr__(self):
        """Representação do objeto StockMovement."""
        return f'<StockMovement {self.id} - Type: {self.movement_type} Product: {self.product_id} Qty: {self.quantity}>'


# --- Configuração para criação do banco de dados ---
# Esta parte não é código de modelo, mas é útil para lembrar como criar as tabelas
# Você precisará executar isso no terminal ou em um script separado.

# Exemplo de como seria no shell Python interativo:
# >>> from app import create_app, db
# >>> app = create_app()
# >>> app.app_context().push() # Entra no contexto da aplicação
# >>> db.create_all() # Cria todas as tabelas definidas nos modelos
# >>> exit()
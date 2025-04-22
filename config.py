import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma_chave_secreta_padrao_muito_dificil_de_adivinhar_substitua_isso'

    # Configuração do banco de dados SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database', 'estoque.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

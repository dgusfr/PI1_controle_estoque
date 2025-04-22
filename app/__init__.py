from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect 
from config import Config
import os 


db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect() 

def create_app(config_class=Config):
    """
    Cria e configura a instância da aplicação Flask.

    Args:
        config_class (object): A classe de configuração a ser usada.
                               Defaulta para a classe Config de config.py.
    """
    app = Flask(__name__)

    # Carrega as configurações definidas na classe Config
    app.config.from_object(config_class)

    # Cria o diretório 'database' se ele não existir.
    # Isso garante que o SQLAlchemy tenha onde colocar o arquivo estoque.db
    database_dir = os.path.join(app.root_path, 'database')
    if not os.path.exists(database_dir):
        os.makedirs(database_dir)

    # Vincula as extensões à instância da aplicação Flask
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # Inicializa CSRFProtect com a aplicação

    # Configurações adicionais para o Flask-Login
    login_manager.login_view = 'auth.login' # Define a rota para a página de login
    login_manager.login_message_category = 'info' # Categoria da mensagem flash (opcional)

    # Importa e registra os blueprints (onde as rotas e a lógica estarão)
    # Faremos isso em arquivos separados para organizar o código.
    # Por exemplo, vamos criar um blueprint para autenticação (auth)
    from app.routes.auth import auth as auth_bp
    app.register_blueprint(auth_bp)

    # Adicionar outros blueprints aqui conforme avançamos (estoque, vendas, etc.)
    # from app.routes.estoque import estoque as estoque_bp
    # app.register_blueprint(estoque_bp, url_prefix='/estoque')

    # from app.routes.vendas import vendas as vendas_bp
    # app.register_blueprint(vendas_bp, url_prefix='/vendas')

    # Configurar um user_loader para o Flask-Login
    # Precisamos importar o modelo User para isso
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        """
        Função de callback do Flask-Login para carregar um usuário dado seu ID.
        Usada para recriar o objeto de usuário a partir do ID armazenado na sessão.
        """
        # Converte user_id para int, pois ele vem como string da sessão
        if user_id is not None:
             return User.query.get(int(user_id))
        return None # Retorna None se o user_id for inválido/não encontrado


    # Um exemplo de rota simples para a página inicial (ainda não usaremos blueprints aqui)
    # Depois podemos mover isso para um blueprint 'main' ou 'dashboard'
    # from flask import render_template
    # @app.route('/')
    # def index():
    #    return render_template('dashboard.html') # Precisaremos criar este template

    return app

# Nota: Com a estrutura de fábrica (create_app), não criamos a instância 'app'
# diretamente neste arquivo, apenas definimos a função que a cria.
# O arquivo run.py chamará create_app() para obter a instância.
from flask import Blueprint, render_template
from flask_login import login_required, current_user # Importamos current_user também

# Cria uma instância de Blueprint para as rotas gerais/principais
main = Blueprint('main', __name__) # Não definimos um url_prefix aqui, pois a rota '/' é a raiz

@main.route('/')
@main.route('/dashboard') # Podemos ter a mesma página acessível por duas URLs
@login_required # Esta rota agora exige que o usuário esteja autenticado
def index():
    """
    Rota para a página inicial (dashboard).
    Exige autenticação para acesso.
    """
    # Podemos passar informações do usuário logado para o template, se necessário
    # user = current_user # current_user é fornecido pelo Flask-Login

    return render_template('dashboard.html', title='Dashboard')
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User # Importa o modelo User
from app.forms import LoginForm # Importa o formulário de login

# Cria uma instância de Blueprint para as rotas de autenticação
# url_prefix='/auth' significa que todas as rotas neste blueprint
# começarão com /auth (ex: /auth/login, /auth/logout)
auth = Blueprint('auth', __name__, url_prefix='/auth')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    Rota para a página de login.
    Exibe o formulário (GET) ou processa o login (POST).
    """
    # Se o usuário já estiver autenticado, redireciona para a página inicial (dashboard)
    if current_user.is_authenticated:
        return redirect(url_for('index')) # 'index' será a rota da página inicial/dashboard

    form = LoginForm() # Cria uma instância do formulário de login

    # Se o formulário for enviado (POST) e for válido
    if form.validate_on_submit():
        # Busca o usuário no banco de dados pelo nome de usuário fornecido
        user = User.query.filter_by(username=form.username.data).first()

        # Verifica se o usuário existe E se a senha está correta
        if user is None or not user.check_password(form.password.data):
            # Se as credenciais estiverem incorretas, mostra uma mensagem de erro
            flash('Nome de usuário ou senha inválidos', 'danger') # 'danger' é uma categoria Bootstrap para alerta vermelho
            return redirect(url_for('auth.login')) # Redireciona de volta para a página de login

        # Se as credenciais estiverem corretas, loga o usuário
        # remember=form.remember_me.data lida com a opção 'Lembrar-me'
        login_user(user, remember=form.remember_me.data)

        # Redireciona para a página anterior que o usuário tentou acessar
        # ou para a página inicial se não houver página anterior registrada
        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'): # Validação básica para segurança
            next_page = url_for('index') # Redireciona para 'index' se não houver 'next' ou for inválido

        flash('Login realizado com sucesso!', 'success') # 'success' é uma categoria Bootstrap para alerta verde
        return redirect(next_page)

    # Se a requisição for GET ou o formulário não for válido, renderiza o template de login
    return render_template('login.html', title='Login', form=form)

@auth.route('/logout')
@login_required # Garante que apenas usuários logados podem acessar esta rota
def logout():
    """
    Rota para realizar o logout do usuário.
    """
    logout_user() # Desloga o usuário atual
    flash('Sessão encerrada com sucesso.', 'info') # 'info' é uma categoria Bootstrap para alerta azul/informativo
    return redirect(url_for('auth.login')) # Redireciona para a página de login após o logout

# Exemplo de rota protegida que exige login
# @auth.route('/protected')
# @login_required
# def protected_route():
#     return "Esta é uma página protegida. Você está logado!"
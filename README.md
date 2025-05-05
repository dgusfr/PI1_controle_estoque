# Sistema de Controle de Caixa e Estoque

## Sumário
1.  [Sobre o Projeto](#sobre-o-projeto)
2.  [Funcionalidades (Requisitos Funcionais)](#funcionalidades-requisitos-funcionais)
3.  [Tecnologias Utilizadas](#tecnologias-utilizadas)
4.  [Arquitetura do Sistema](#arquitetura-do-sistema)
5.  [Estrutura de Diretórios](#estrutura-de-diretórios)
6.  [Configuração do Ambiente e Instalação](#configuração-do-ambiente-e-instalação)
    * [Pré-requisitos](#pré-requisitos)
    * [Clonando o Repositório](#clonando-o-repositório)
    * [Criando e Ativando o Ambiente Virtual](#criando-e-ativando-o-ambiente-virtual)
    * [Instalando Dependências](#instalando-dependências)
    * [Configuração do Banco de Dados](#configuração-do-banco-de-dados)
    * [Criando o Primeiro Usuário](#criando-o-primeiro-usuário)
7.  [Como Executar a Aplicação](#como-executar-a-aplicação)
8.  [Status do Projeto](#status-do-projeto)
9.  [Próximos Passos e Melhorias Futuras](#próximos-passos-e-melhorias-futuras)
10. [Contribuição](#contribuição)
11. [Licença](#licença)
12. [Autor](#autor)

---

## 1. Sobre o Projeto

Este projeto é um sistema web simples para controle de caixa e estoque, desenvolvido em Python utilizando o framework Flask. 


Ele foi criado como parte de uma disciplina de projetos, com o objetivo de aplicar conceitos de desenvolvimento web, bancos de dados (ORM) e gestão de projetos.

O sistema permitirá gerenciar produtos, registrar movimentações de estoque, realizar vendas, calcular troco e gerar relatórios básicos.

## 2. Funcionalidades (Requisitos Funcionais)

Lista dos requisitos funcionais previstos para o sistema (conforme o relatório de requisitos):

* [x] RF01. Cadastro de produtos (nome, código, categoria, preço, fornecedor, quantidade disponível, estoque mínimo).
* [x] RF02. Listagem de produtos com ordenação e busca (usando DataTables.js).
* [x] RF03. Edição e exclusão de produtos.
* [x] RF04. Registro de entradas de estoque.
* [x] RF05. Registro de saídas de estoque (venda, perda).
* [x] RF06. Alerta visual de estoque baixo (na listagem de produtos).
* [x] RF07. Registro de vendas (produtos vendidos, quantidade, valor final).
* [ ] RF08. Cálculo automático do troco.
* [ ] RF09. Geração de comprovante de venda em PDF.
* [x] RF10. Cadastro de categorias e fornecedores.
* [ ] RF11. Relatório de vendas diário.
* [x] RF12. Autenticação para uso (Login/Logout).
* [ ] RF13. Gerenciamento de usuários com permissões.
* [x] RF14. Sistema rodando localmente via servidor Flask.
* [x] RF15. Histórico de vendas e movimentações (Modelos definidos).
* [x] RF16. Interface responsiva e intuitiva (Uso inicial de Bootstrap 5).
* [x] RF17. Utilização de Git para controle de versão.

*(Marquei com [x] as funcionalidades cuja estrutura básica ou implementação inicial já abordamos, e com [ ] as que ainda serão desenvolvidas ou completadas).*

## 3. Tecnologias Utilizadas

* **Backend:**
    * Python 3
    * Flask (Framework Web)
    * SQLAlchemy e Flask-SQLAlchemy (ORM para banco de dados)
    * Flask-WTF (Integração com WTForms para formulários seguros)
    * Flask-Login (Gerenciamento de autenticação de usuários)
    * `python-dotenv` (Para carregar variáveis de ambiente)
    * `werkzeug.security` (Para hash de senhas)
    * `decimal.Decimal` (Para precisão em valores monetários)
* **Frontend:**
    * HTML5
    * CSS3 (com Bootstrap 5 para estilização)
    * JavaScript (para interatividade, incluindo DataTables.js)
    * Jinja2 (Motor de templates do Flask)
    * DataTables.js (Para tabelas interativas com ordenação e busca)
* **Banco de Dados:**
    * SQLite (Banco de dados leve e auto-contido - `estoque.db`)
* **Outras Ferramentas:**
    * Git (Controle de Versão)

## 4. Arquitetura do Sistema

O sistema segue um padrão de projeto inspirado em **MVC (Model-View-Controller)** com algumas camadas adicionais sugeridas:

* **Model:** Definição da estrutura de dados e interação com o banco de dados usando SQLAlchemy ORM (`app/models.py`).
* **View:** Templates HTML com Jinja2 para renderizar a interface do usuário (`app/templates/`). Estilização com Bootstrap 5.
* **Controller:** Rotas Flask que processam requisições HTTP, contêm a lógica de negócio básica e interagem com os modelos e views (`app/routes/`). Organizado em Blueprints (ex: `auth`, `main`, `estoque`).
* **Service Layer (Futuro):** Camada opcional para isolar regras de negócio mais complexas, separando-as das rotas.
* **Utilitários (Futuro):** Módulos para funcionalidades de apoio (ex: geração de PDF - `app/utils/pdf.py`).

## 5. Estrutura de Diretórios

A estrutura de diretórios do projeto é organizada da seguinte forma:

```
controle_estoque/
|
|-- app/
|   |-- __init__.py       # Inicialização da aplicação e extensões
|   |-- models.py         # Definição dos modelos do banco de dados (SQLAlchemy)
|   |-- forms.py          # Definição dos formulários web (Flask-WTF)
|   |-- routes/           # Blueprints e definições de rotas
|   |   |-- auth.py       # Rotas de autenticação (login, logout)
|   |   |-- main.py       # Rotas principais (dashboard)
|   |   |-- estoque.py    # Rotas de estoque (produtos, categorias, fornecedores)
|   |-- templates/        # Arquivos de template HTML (Jinja2)
|   |   |-- base.html         # Template base para herança
|   |   |-- login.html        # Template da página de login
|   |   |-- dashboard.html    # Template do dashboard
|   |   |-- estoque/          # Templates relacionados a estoque
|   |   |   |-- produtos.html
|   |   |   |-- adicionar_produto.html
|   |   |   |-- editar_produto.html
|   |   |   |-- listar_categorias.html
|   |   |   |-- adicionar_categoria.html
|   |   |   |-- listar_fornecedores.html
|   |   |   |-- adicionar_fornecedor.html
|   |-- static/           # Arquivos estáticos (CSS customizado, JS, imagens, etc.)
|   |-- utils/            # Funções utilitárias
|
|-- database/             # Diretório para o arquivo do banco de dados SQLite
|   |-- estoque.db        # Arquivo do banco de dados (IGNORADO pelo Git)
|
|-- config.py             # Configurações da aplicação
|-- run.py                # Ponto de entrada para executar a aplicação
|-- requirements.txt      # Lista de dependências Python
|-- .gitignore            # Arquivos e diretórios a serem ignorados pelo Git
|-- README.md             # Este arquivo
```

## 6. Configuração do Ambiente e Instalação

Siga estes passos para configurar o ambiente de desenvolvimento e rodar o projeto na sua máquina.

### Pré-requisitos

* Python 3.6 ou superior instalado.
* Git instalado.

### Clonando o Repositório

Abra o terminal e clone o repositório para o seu computador:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd controle_estoque
```

### Criando e Ativando o Ambiente Virtual

É altamente recomendado usar um ambiente virtual.

No Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

No Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Você verá `(venv)` no início da linha de comando se o ambiente virtual estiver ativo.

### Instalando Dependências

Com o ambiente virtual ativo, instale as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados

O projeto utiliza SQLite. O arquivo do banco de dados será criado automaticamente na primeira vez que você executar a criação das tabelas.

Dentro do diretório do projeto e com o ambiente virtual ativo, use o `flask shell` para criar as tabelas:

```bash
flask shell
```

No shell interativo Python que abrir:

```python
>>> from app import db, create_app
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
```

Isso criará o diretório `database/` e o arquivo `estoque.db` (se não existirem) e todas as tabelas definidas em `app/models.py`.

### Criando o Primeiro Usuário (Obrigatório para Login)

Para poder acessar a maioria das páginas (protegidas por `@login_required`), você precisa de pelo menos um usuário no banco de dados. Você pode criá-lo usando o `flask shell` novamente:

```bash
flask shell
```

No shell interativo:

```python
>>> from app.models import User
>>> from app import db
>>> user = User(username='admin', role='admin') # Você pode escolher o username e role
>>> user.set_password('sua_senha_segura') # SUBSTITUA por uma senha forte!
>>> db.session.add(user)
>>> db.session.commit()
>>> print(f"Usuário '{user.username}' criado com sucesso!")
>>> exit()
```
Lembre-se de **substituir `'sua_senha_segura'`** por uma senha real e segura.

Você também pode querer adicionar algumas categorias e fornecedores manualmente no shell para poder testar o cadastro de produtos:

```python
>>> from app.models import Category, Supplier
>>> from app import db
>>> db.session.add(Category(name='Eletrônicos'))
>>> db.session.add(Category(name='Alimentos'))
>>> db.session.add(Supplier(name='Fornecedor A', contact_info='contato@fornecedora.com'))
>>> db.session.add(Supplier(name='Fornecedor B'))
>>> db.session.commit()
>>> exit()
```

## 7. Como Executar a Aplicação

Com o ambiente virtual ativo e as dependências instaladas, execute o arquivo `run.py`:

```bash
python run.py
```

O servidor de desenvolvimento do Flask será iniciado. Você verá uma mensagem no terminal indicando o endereço onde a aplicação está rodando (geralmente `http://127.0.0.1:5000/`).

Abra este endereço no seu navegador. Você deverá ser redirecionado para a página de login. Use o usuário e senha que você criou no Passo 6.

## 8. Status do Projeto

Até o momento, as seguintes partes do projeto foram implementadas (estruturas básicas ou completas):

* Estrutura inicial do projeto Flask (`run.py`, `config.py`, `app/`, `__init__.py`).
* Modelos de banco de dados básicos definidos (Usuário, Categoria, Fornecedor, Produto, Venda, ItemVenda, MovimentaçãoEstoque).
* Autenticação de usuário (Login e Logout) usando Flask-Login.
* Página Dashboard (inicial, protegida por login).
* Templates base e uso de herança.
* Listagem de Produtos com DataTables.js (busca e ordenação cliente-side) e alerta visual de estoque baixo.
* Cadastro de Produtos.
* Listagem e Cadastro de Categorias.
* Listagem e Cadastro de Fornecedores.
* Configuração inicial de `.gitignore`.

## 9. Próximos Passos e Melhorias Futuras

Há várias funcionalidades e melhorias a serem implementadas para completar o projeto:

* Completar RF03: Implementar Edição e Exclusão de Produtos (Rotas e lógica já criadas, template de edição e ativação na listagem prontos).
* Implementar Edição e Exclusão de Categorias e Fornecedores.
* Implementar RF04 e RF05: Registro de Entradas e Saídas de Estoque (CRUD para MovimentaçãoEstoque e atualização da quantidade em Produto).
* Implementar RF07 e RF08: Registro de Vendas (Interface para selecionar produtos, calcular total/troco, salvar Venda e ItensVenda).
* Implementar RF09: Geração de comprovante de venda em PDF.
* Implementar RF11: Relatório de Vendas Diário (Consulta no banco, exibição).
* Implementar RF13: Gerenciamento de Usuários e Permissões (CRUD de usuários, controle de acesso baseado em role).
* Melhorar RF16: Refinar a interface responsiva e intuitiva (uso completo do Bootstrap, validações no frontend).
* Adicionar validações mais robustas e tratamento de erros.
* Implementar paginação nas listagens (DataTables já ajuda, mas otimizar para grandes volumes).
* Adicionar testes unitários e de integração.
* Configurar o Git para usar branches, pull requests, etc. (RF17).
* Considerar o Service Layer para regras de negócio mais complexas.
* Internacionalização (opcional).

## 10. Contribuição

Contribuições são bem-vindas! Se você encontrar um bug ou tiver uma sugestão de melhoria, sinta-se à vontade para:

1.  Abrir uma Issue descrevendo o problema ou sugestão.
2.  Criar um Fork do projeto.
3.  Criar uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
4.  Fazer suas alterações e testar.
5.  Comitar suas mudanças (`git commit -m 'feat: adiciona funcionalidade X'`).
6.  Enviar para o seu Fork (`git push origin feature/nome-da-feature`).
7.  Abrir um Pull Request para o repositório original.

## 11. Licença

Este projeto é para fins educacionais, desenvolvido no contexto de uma disciplina de faculdade. Sinta-se à vontade para usar o código como referência para seus próprios estudos e projetos, mas lembre-se das regras da sua instituição em relação a plágio.

## 12. Autor

Desenvolvido por Diego Franco.
Orientação/Contexto: Disciplina de Projeto Integrador 1

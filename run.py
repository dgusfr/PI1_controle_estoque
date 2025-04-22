from app import create_app

app = create_app()

if __name__ == '__main__':
    # run() inicia o servidor web.
    # debug=True habilita o modo de depuração, que mostra erros detalhados
    # no navegador e recarrega o servidor automaticamente a cada mudança no código.
    app.run(debug=True)
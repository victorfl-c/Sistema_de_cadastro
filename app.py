from auth import Autenticador
from proj import Projeto

def main():
    # Estanciar o autenticador
    autenticador = Autenticador()
    autenticador.carregar_usuarios()
    # Executar o menu de autenticação
    while True:
        if autenticador.menu_autenticacao():
            projeto = Projeto('datasets/projetos.json')
            projeto.menu()

        else:
            break


if __name__ == '__main__':
    main()
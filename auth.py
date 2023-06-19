import os
import getpass
import json


# Criar classe Autenticador
class Autenticador:
    # Definir os atributos da classe
    def __init__(self):
        self.arquivo_usuarios = "datasets/usuarios.json"
        self.usuarios = self.carregar_usuarios()
        self.arquivo_usuario_online = "datasets/online.json"
        self.usuario_online = self.carregar_usuario_online()
   
    # Carregar o arquivo de usuários
    def carregar_usuarios(self):
        try:
            if not os.path.exists("datasets"):
                os.makedirs("datasets")
                
            with open(self.arquivo_usuarios, "r") as arquivo:
                self.usuarios = json.load(arquivo)
        # Criar arquivo caso não exista
        except (FileNotFoundError, json.JSONDecodeError):
            self.usuarios = {}
        
        return self.usuarios
    
    # carregar arquivo dos usuários online
    def carregar_usuario_online(self):
        try:
            with open(self.arquivo_usuario_online, "r") as arquivo:
                self.usuario_online = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            self.usuario_online = {}
        
        return self.usuario_online
    
    # Ler as informações do usuário necessárias para o envio de emails
    def autenticar_app_email(self, email, token):
        with open(self.arquivo_usuario_online, "w") as arquivo:
            self.usuario_online["email"] = email
            self.usuario_online["token"] = token
            json.dump(self.usuario_online, arquivo)


    def criar_arquivo_usuarios(self):
        if not os.path.exists(self.arquivo_usuarios):           
            with open(self.arquivo_usuarios, "x") as arquivo:
                arquivo.write("{}")
    

    def criar_arquivo_usuario_online(self):
        if not os.path.exists(self.arquivo_usuario_online):
            with open(self.arquivo_usuario_online, "x") as arquivo:
                arquivo.write("{}")


    def salvar_usuarios(self):
        with open(self.arquivo_usuarios, "w") as arquivo:
            json.dump(self.usuarios, arquivo)


    def excluir_arquivo(self, arquivo):
        if os.path.exists(arquivo):
            os.remove(arquivo)
            print("Offline...")

        else:
            print(f"Arquivo {arquivo} não encontrado.")


    def cadastrar_nome(self):
        nome = input("\nDigite seu nome de usuário: ")

        while not nome:
            return self.cadastrar_nome()

        print(f"Nome: {nome}")

        conf = input("Confirmar nome? (s/n): ").lower() == 's'

        if not conf:
            self.cadastrar_nome()

        return nome


    def cadastrar_email(self):
        email = input("Digite seu e-mail: ")

        while not email:
            return self.cadastrar_email()

        conf = input("Confirmar e-mail? (s/n): ").lower() == 's'

        if not conf:
            return self.cadastrar_email()

        return email


    def cadastrar_senha(self):
        senha = getpass.getpass("Digite a senha: ")

        while not senha:
          return self.cadastrar_senha()

        rep_senha = getpass.getpass("Digite novamente: ")
        if senha == rep_senha:
          print("Senha cadastrada.\n")

        else:
          print("Senhas não compatíveis.\nAs senhas precisam ser iguais.\n")
          return self.cadastrar_senha()

        return senha

    def cadastrar_token(self):
        print("\nA Senha de App serve para habilitar o envio de e-mails automáticos")
        print("A cada vez que houver projetos criados, atualizados ou excluídos")
        print("Central de ajuda: https://support.google.com/accounts/answer/185833?hl=pt-BR")
        print("Para prosseguir sem uma, pressione [Enter])")

        token = getpass.getpass("Copie sua senha de app do gmail e cole aqui: ")
        
        while not token:
            conf = input("Seguir sem uma senha de app? (s/n): ").lower() == 's'

            if conf:
                token = 'n/a'
                break

            else:
                return self.cadastrar_token()

        return token


    def cadastrar_usuario(self):

        nome = self.cadastrar_nome()

        if nome in self.usuarios.keys():
            print("Usuário já cadastrado.")
        else:
            dados_usuario = [
                self.cadastrar_senha(),
                self.cadastrar_email(),
                self.cadastrar_token()
            ]

            self.usuarios[nome] = dados_usuario
            self.salvar_usuarios()
            print("Usuário cadastrado com sucesso.")


    def fazer_login(self):
        nome = input("\nDigite o nome de usuário: ")
        senha = getpass.getpass("Digite a senha: ")

        if nome in self.usuarios and self.usuarios[nome][0] == senha:
            email, token = self.usuarios[nome][1], self.usuarios[nome][2]
            self.carregar_usuario_online()
            self.autenticar_app_email(email, token)
            
            print("Login realizado com sucesso.")
            return True
        else:
            print("\nNome de usuário ou senha incorretos.")
            return False


    def excluir_usuario(self):
        nome = input("Digite o nome de usuário que deseja excluir: ")
        if nome in self.usuarios:
            senha = getpass.getpass("Digite a senha: ")

            if self.usuarios[nome] and self.usuarios[nome][0] == senha:
                del self.usuarios[nome]
                self.salvar_usuarios()
                print("Usuário excluído com sucesso.")
            else:
                print("Senha incorreta.")
        else:
            print("Usuário não encontrado.")


    def alterar_senha(self):
        nome = input("Digite o nome de usuário: ")
        if nome in self.usuarios:
            senha_atual = getpass.getpass("Digite a senha atual: ")
            if self.usuarios[nome] and self.usuarios[nome][0] == senha_atual:
                nova_senha = getpass.getpass("Digite a nova senha: ")
                self.usuarios[nome][0] = nova_senha
                self.salvar_usuarios()
                print("Senha alterada com sucesso.")
            else:
                print("Senha atual incorreta.")
        else:
            print("Usuário não encontrado.")


    def menu_autenticacao(self):
        
        while True:
            print("\n------ MENU AUTENTICAÇÃO ------")
            print("1. Cadastrar usuário")
            print("2. Fazer login")
            print("3. Excluir usuário")
            print("4. Alterar senha")
            print("0. Sair")

            opcao = input("Digite o número da opção desejada: ")

            if opcao == "1":
                self.cadastrar_usuario()
            elif opcao == "2":
                if self.fazer_login():
                    return True
            elif opcao == "3":
                self.excluir_usuario()
            elif opcao == "4":
                self.alterar_senha()
            elif opcao == "0":
                print("Encerrando o programa...")
                return False                
            else:
                print("Opção inválida. Digite um número válido.")

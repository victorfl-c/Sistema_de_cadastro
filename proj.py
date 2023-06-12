from auth import Autenticador
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import pytz
import json


class Projeto(Autenticador):

    def __init__(self, database_file):
        super().__init__()
        self.database_file = database_file
        self.projetos = self.carregar_projetos()
        self.chave_app = self.usuario_online


    def carregar_projetos(self):
        try:
            with open(self.database_file, 'r', encoding='utf-8') as file:
                projetos = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            projetos = []
        
        return projetos


    def salvar_projetos(self):
        with open(self.database_file, 'w', encoding='utf-8') as file:
            json.dump(self.projetos, file, indent=4)


    def criar_projeto(self, dados):
        self.projetos.append(dados)
        self.enviar_email(dados, 'Novo projeto cadastrado')
        self.salvar_projetos()


    def atualizar_projeto(self, indice, novos_dados):
        projeto = self.projetos[indice]
        projeto.update(novos_dados)
        self.enviar_email(projeto, 'Projeto atualizado')
        self.salvar_projetos()


    def excluir_projeto(self, indice):
        projeto = self.projetos.pop(indice)
        self.enviar_email(projeto, 'Projeto excluído')
        self.salvar_projetos()


    def corpo_email(self, dados):
        corpo = "<ul>"
        for chave, valor in dados.items():
            if chave == 'Descricao':
                corpo += f"<br><b>{chave}:</b><br>{valor}"
            else:
                corpo += f"<li><b>{chave}:</b> {valor}</li>"
        corpo += "</ul>"
        return corpo


    def enviar_email(self, dados, assunto):
        if self.chave_app["token"] == 'n/a':
          print('Senha de app não cadastrada (notificação por e-mail desativada)')
          return 

        else:
          while True:
            email_remetente = input("Insira o e-mail do remetente: ")
            conf = input("Confirmar e-mail? (s/n) ").lower() == 's'

            if conf == True:
              break

          try:
              # Configurar as informações do servidor de e-mail
              host = 'smtp.gmail.com'
              porta = 587
              usuario = self.chave_app["email"]
              senha = self.chave_app["token"]

              # Construir o objeto do e-mail
              msg = MIMEMultipart()
              msg['From'] = usuario
              msg['To'] = email_remetente
              msg['Subject'] = f"{assunto} | {dados['Projeto']}"

              # Adicionar os dados do projeto ao corpo do e-mail
              corpo = self.corpo_email(dados)
              msg.attach(MIMEText(corpo, 'html'))

              # Conectar ao servidor de e-mail e enviar o e-mail
              with smtplib.SMTP(host, porta) as servidor:
                  servidor.starttls()
                  servidor.login(usuario, senha)
                  servidor.send_message(msg)

              print('E-mail enviado com sucesso!')

          except smtplib.SMTPAuthenticationError:
              print('Erro de autenticação. Verifique seu e-mail e senha e tente novamente.')

          except smtplib.SMTPException as e:
              print('Ocorreu um erro ao enviar o e-mail. Por favor, verifique as informações e tente novamente.')
              print(f'Erro: {str(e)}')

          except Exception as e:
              print('Ocorreu um erro inesperado.')
              print(f'Erro: {str(e)}')


    def cadastrar_projeto(self):
        try:
            # Formatando a data de cadastro para o fuso-horario local
            fuso_horario_pe = pytz.timezone('America/Sao_Paulo')
            data_hora_pe = datetime.now(fuso_horario_pe).strftime('%d-%m-%Y %H:%M:%S')

            perguntas = [
                ("Projeto", "\nInforme o nome do Projeto: "),
                ("Inicio", "Data de início (dd-mm-yyyy): "),
                ("Encerramento", "Data de Encerramento (dd-mm-yyyy): "),
                ("Participantes", "Quantidade de participantes: "),
                ("Modalidade", "Informe a modalidade do projeto:\n1 - Presencial\n2 - Online\n3 - Híbrido\nOpção: "),
                ("Publico", "Digite 1 - Público Interno\nDigite 2 - Público Externo\nOpção: "),
                ("Descricao", "Descrição do Projeto: ")
            ]

            dados = {"Cadastro": data_hora_pe}

            opcoes_escolha = {
                "Modalidade": {
                    "1": "Presencial",
                    "2": "Online",
                    "3": "Híbrido"
                },
                "Publico": {
                    "1": "Interno",
                    "2": "Externo"
                }
            }

            # Coleta os dados do usuário
            for chave, pergunta in perguntas:
                valor = None
                while not valor:
                    valor = input(pergunta)
                    if chave in opcoes_escolha:
                        if valor in opcoes_escolha[chave]:
                            valor = opcoes_escolha[chave][valor]
                        else:
                            print(f"{chave} inválido!\nDigite uma opção válida.")
                            valor = None
                dados[chave] = valor

            self.criar_projeto(dados)

        except ValueError:
            # Tratamento de erro para valor inválido inserido para a quantidade de participantes
            print("Erro: valor inválido inserido para a quantidade de participantes.")
            self.cadastrar_projeto()

        except Exception as e:
            # Tratamento de erro genérico para outras exceções não esperadas
            print(f"Erro: {str(e)}")
            self.cadastrar_projeto()


    def listar_projetos(self):
        if self.projetos:
            print("Lista de projetos:")
            for i, projeto in enumerate(self.projetos):
                print(f"\nProjeto {i + 1}:")
                for chave, valor in projeto.items():
                    print(f"{chave}: {valor}")
        else:
            print("Nenhum projeto cadastrado.")


    def atualizar_projeto_menu(self):
        self.listar_projetos()
        if self.projetos:
            try:
                indice = int(input("\nDigite o número do projeto que deseja atualizar: ")) - 1
                if 0 <= indice < len(self.projetos):
                    projeto = self.projetos[indice]

                    print("\nDados atuais do projeto:")
                    for chave, valor in projeto.items():
                        print(f"{chave}: {valor}")

                    print("\nDigite os novos dados do projeto:")
                    novos_dados = {}
                    for chave, valor in projeto.items():
                        if chave == 'Cadastro':
                          continue
                          
                        novo_valor = input(f"{chave} (atual: {valor}): ")
                        if novo_valor:
                            novos_dados[chave] = novo_valor

                    self.atualizar_projeto(indice, novos_dados)
                else:
                    print("Índice inválido.")
            except ValueError:
                print("Erro: Valor inválido inserido para o número do projeto.")
        else:
            print("Nenhum projeto cadastrado.")


    def excluir_projeto_menu(self):
        self.listar_projetos()
        if self.projetos:
            try:
                indice = int(input("\nDigite o número do projeto que deseja excluir: ")) - 1
                if 0 <= indice < len(self.projetos):
                    self.excluir_projeto(indice)
                else:
                    print("Índice inválido! Digite um número de projeto válido.")
            except ValueError:
                print("Erro: Valor inválido inserido para o número do projeto.")
        else:
            print("Nenhum projeto cadastrado.")


    def menu(self):
        while True:
            print("\n===== Menu =====")
            print("1 - Cadastrar Projeto")
            print("2 - Listar Projetos")
            print("3 - Atualizar Projeto")
            print("4 - Excluir Projeto")
            print("5 - Voltar para a Pagina de Login")
            print("0 - Sair")

            opcao = input("Digite a opção desejada: ")

            if opcao == '1':
                self.cadastrar_projeto()
            elif opcao == '2':
                self.listar_projetos()
            elif opcao == '3':
                self.atualizar_projeto_menu()
            elif opcao == '4':
                self.excluir_projeto_menu()
            elif opcao == '5':
                self.menu_autenticacao()
            elif opcao == '0':
                self.excluir_arquivo('datasets/online.json')

                break
            else:
                print("\nOpção inválida! Digite uma opção válida.")

# Documentação do Sistema de Cadastro de Projetos Educacionais

## Visão Geral
O Sistema de Cadastro de Projetos Educacionais é uma aplicação que permite o cadastro, atualização, exclusão e listagem de projetos educacionais. Ele foi desenvolvido com o objetivo de facilitar o gerenciamento de projetos no contexto educacional, permitindo que os usuários possam cadastrar e acompanhar os detalhes dos projetos em andamento.
A aplicação foi implementada utilizando a linguagem de programação Python e segue uma arquitetura orientada a objetos. O código fonte foi estruturado em duas classes principais: Projeto e Autenticador.

## Ferramentas
* Python 3.9.13
* Visual Studio Code

## Dependências
A aplicação faz uso das seguintes bibliotecas Python:
* json: utilizada para carregar e salvar os usuários e projetos no formato JSON.
* os: fornece acesso a várias funcionalidades relacionadas ao sistema operacional.
* datetime: utilizada para obter a data e hora atual no momento do cadastro do projeto.
* pytz: utilizada para converter a data e hora para o fuso-horário local.
* smtplib: utilizada para enviar e-mails.
* email.mime.multipart: utilizada para construir o objeto de e-mail com várias partes.
* email.mime.text: utilizada para adicionar o corpo de texto ao e-mail.

## Funcionalidades
### Autenticação de Usuários
O sistema possui um mecanismo de autenticação de usuários implementado na classe Autenticador. Ele permite que apenas usuários autenticados tenham acesso às funcionalidades do sistema. Os usuários são armazenados em um arquivo JSON e podem ser cadastrados, autenticados, editados e deslogados.

### Cadastro de Projetos
O sistema permite o cadastro de projetos educacionais por meio da funcionalidade "Cadastrar Projeto". Ao cadastrar um projeto, o usuário pode informar o nome do projeto, a data de início, a data de encerramento, a quantidade de participantes, a modalidade do projeto (presencial, online ou híbrido), o público-alvo (interno ou externo) e uma descrição do projeto.

### Atualização de Projetos
O sistema permite a atualização dos dados de um projeto já cadastrado. A funcionalidade "Atualizar Projeto" lista todos os projetos cadastrados e solicita ao usuário o número do projeto que deseja atualizar. Em seguida, o usuário pode digitar os novos valores para cada campo do projeto selecionado.

### Exclusão de Projetos
O sistema permite a exclusão de projetos cadastrados por meio da funcionalidade "Excluir Projeto". A lista de projetos cadastrados é exibida e o usuário pode selecionar o número do projeto que deseja excluir.

### Listagem de Projetos
O sistema disponibiliza a funcionalidade "Listar Projetos" para exibir a lista de todos os projetos cadastrados. Os projetos são exibidos com seus respectivos campos, como nome, datas, quantidade de participantes, modalidade, público-alvo e descrição.

### Envio de E-mails
Ao cadastrar, atualizar ou excluir um projeto, o sistema envia um e-mail para o remetente informando sobre a ação realizada. O e-mail contém informações detalhadas sobre o projeto e o tipo de ação realizada.

## Execução
Para executar o sistema, é necessário ter o Python instalado. Basta executar o arquivo principal do sistema, que é chamado de app.py. Ao iniciar a execução, será exibido um menu de autenticação, onde o usuário pode realizar o login ou cadastro de um novo usuário. Após o login bem-sucedido, o menu principal do sistema é exibido, oferecendo as opções de cadastro, listagem, atualização e exclusão de projetos.

## Considerações Finais
O Sistema de Cadastro de Projetos Educacionais é uma aplicação simples e intuitiva que auxilia na gestão de projetos no contexto educacional. Ele permite que os usuários tenham um controle centralizado sobre os projetos em andamento, facilitando o acompanhamento das informações relevantes. A funcionalidade de envio de e-mails proporciona uma forma de notificação automatizada sobre as ações realizadas nos projetos.


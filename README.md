# Projeto_Oficina⚙️ 

AutoMecânica Pro - Sistema de Gestão para Oficina Mecânica

Sistema web desenvolvido em Python com Flask e MySQL para gerenciamento de clientes, veículos e agendamentos de uma oficina mecânica. O projeto foi construído atendendo integralmente às especificações e regras do edital prático SAEP / SENAI.

📋 Sumário

Funcionalidades Principais

Regras do Edital Atendidas

Tecnologias Utilizadas

Estrutura do Projeto

Prerequisites e Instalação

Configuração do Banco de Dados

Como Executar a Aplicação

Credenciais para Teste

🚀 Funcionalidades Principais

Autenticação e Sessão de Usuários

Login seguro com validação explícita para dados inválidos/em branco.

Hash de senhas via Bcrypt.

Expiração automática de sessão após 15 minutos de inatividade.

Exibição contínua do nome e cargo do usuário logado no topo do sistema.

Gestão de Clientes (LGPD & Validações)

Validação de CPF restrita ao formato de 11 dígitos.

Armazenamento seguro de CPF criptografado com Bcrypt no banco.

Busca/filtro por termo (nome, CPF, e-mail, telefone) com atualização dinâmica na listagem.

Permite alteração/edição completa dos dados cadastrais com persistência direta no banco de dados.

Gestão de Veículos

Vínculo obrigatório de cada veículo a um cliente previamente cadastrado.

Edição e remoção de registros com verificação de integridade relacional.

Gestão de Agendamentos

Listagem ordenada cronologicamente por data (ORDER BY data_agendamento ASC).

Apresentação completa dos dados do cliente e do veículo em cada agendamento (JOIN).

Atualização da data e horário de agendamentos com atualização imediata no banco de dados.

🎯 Regras do Edital Atendidas

Regra / Exigência

Status

Implementação

Sessão com expiração

✅

PERMANENT_SESSION_LIFETIME = timedelta(minutes=15)

Identificação visual do usuário

✅

Injeção global no context_processor exibindo no cabeçalho

Validação explicita no login

✅

Retorno de mensagens flash específicas no autenticacao.py

Validação de 11 dígitos no CPF

✅

Regex verificando exatamente 11 caracteres numéricos

Criptografia do CPF (LGPD)

✅

Criptografia via bcrypt.hashpw armazenada em cpf_hash

Busca de clientes por termo

✅

Query SQL com operador LIKE em múltiplos campos

Edição de dados de clientes

✅

Rota POST /clientes/editar/<id> atualizando no MySQL

Vínculo obrigatório de veículo

✅

Validação de cliente_id no cadastro do veículo

Agendamento ordenado por data

✅

ORDER BY a.data_agendamento ASC na consulta SQL

Dados completos em Agendamentos

✅

JOIN entre agendamentos, clientes e veiculos

Reagendamento de data

✅

Rota POST /agendamentos/atualizar-data/<id>

Carga inicial do banco

✅

Mínimo de 3 registros em todas as tabelas via db.sql

🛠️ Tecnologias Utilizadas

Linguagem: Python 3.10+

Framework Web: Flask 3.0+

Banco de Dados: MySQL 8.0+

Segurança e Criptografia: Bcrypt

Driver de Banco: mysql-connector-python

Frontend: HTML5, CSS3 e JavaScript Puro (ES6)

📂 Estrutura do Projeto

oficina_mecanica/
├── db.sql                      # Script SQL de criação do schema e população inicial
├── sistema/
│   ├── app.py                  # Ponto de entrada da aplicação Flask
│   ├── autenticacao.py         # Lógica de login, logout e controle de sessão
│   ├── banco.py                # Conexão centralizada com o MySQL
│   ├── clientes.py             # CRUD e regras de negócio para Clientes (CPF/Bcrypt)
│   ├── veiculos.py             # CRUD e vinculo de Veículos com Clientes
│   ├── agendamento.py          # Lógica de Agendamentos e Reagendamento
│   ├── rotas.py                # Registro de rotas e interceptor de segurança
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css       # Estilos da interface
│   │   └── js/
│   │       └── main.js         # Manipulação de modais e UI
│   └── templates/
│       ├── base.html           # Template base com o cabeçalho global
│       ├── login.html          # Tela de autenticação
│       ├── dashboard.html      # Painel geral de resumo
│       ├── clientes.html       # Interface de clientes
│       ├── veiculos.html       # Interface de veículos
│       └── agendamentos.html   # Interface de agendamentos
└── requirements.txt            # Dependências da aplicação


⚙️ Pré-requisitos e Instalação

Clone ou navegue até a pasta do projeto:

cd oficina_mecanica


Crie e ative um ambiente virtual:

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate


Instale as dependências:

pip install -r requirements.txt


🗄️ Configuração do Banco de Dados

Certifique-se de que o MySQL Service está em execução.

Execute o arquivo db.sql para criar o banco de dados saep_db e carregar os dados de teste:

mysql -u root -p < db.sql


(Opcional) Caso sua senha do MySQL seja diferente de Senai@118, configure as variáveis de ambiente antes de executar:

export DB_HOST="localhost"
export DB_USER="root"
export DB_PASSWORD="sua_senha_aqui"
export DB_NAME="saep_db"


💻 Como Executar a Aplicação

Com o ambiente virtual ativado, execute o arquivo app.py:

python sistema/app.py


Acesse a aplicação no seu navegador:

http://127.0.0.1:5000


🔑 Credenciais para Teste

O banco de dados pré-carregado conta com os seguintes usuários configurados:

Usuário (login)

Senha

Cargo / Perfil

admin

admin123

Administrador / Gerente

mecanico

senha123

Mecânico Chefe

recepcao

rec123

Recepcionista

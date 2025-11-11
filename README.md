# 🐾 Guia **LarPet** – Sistema de Adoção de Animais

**Versão:** 1.0  
**Linguagem:** Python (Flask)  
**Plataforma:** Web  
**Repositório:** [github.com/virginiaoliveira-jpg/sistema_adocao](https://github.com/virginiaoliveira-jpg/sistema_adocao)

---

## 📘 Introdução

O **LarPet** é um sistema web desenvolvido em **Python com o framework Flask**, criado para facilitar o processo de **adoção de animais** de forma organizada, acessível e segura.  
O projeto conecta **ONGs, protetores e adotantes** em uma única plataforma, permitindo o **cadastro, gerenciamento e acompanhamento de adoções**.

Este guia apresenta o funcionamento do projeto, as principais abas do sistema e o fluxo geral de navegação.

---

## 🧩 Estrutura do Projeto

sistema_adocao/
    │
    ├── app.py # Arquivo principal do sistema Flask
    ├── database.db # Banco de dados SQLite
    │
    ├── static/ # Arquivos estáticos (CSS, JS, imagens)
    │ ├── css/
    │ ├── js/
    │ └── images/
    │
    └── templates/ # Páginas HTML (Jinja2)
    ├── base.html
    ├── login.html
    ├── cadastro.html
    ├── animais.html
    └── sobre.html

---

## 🌐 Principais Abas do Sistema

| Aba | Descrição |
|------|------------|
| 🏠 **Página Inicial** | Apresenta o projeto e seus objetivos. |
| 🔐 **Login** | Permite que usuários, ONGs ou administradores acessem o sistema. |
| 📝 **Cadastro** | Criação de novas contas de usuário ou administrador. |
| 🐶 **Gerenciar Animais** | Aba exclusiva para cadastrar, editar ou remover animais disponíveis para adoção. |
| 💌 **Adoções** | Exibe animais adotados e informações sobre os adotantes. |
| ℹ️ **Sobre** | Página de documentação e informações sobre o projeto. |

---


⚙️ Tecnologias Utilizadas
🐍 Python (Flask)
💾 SQLite
🖥️ HTML, CSS e JavaScript
🎨 Bootstrap 5

🎯 Objetivo
Promover a adoção consciente de animais, tornando o processo mais acessível e eficiente para ONGs, protetores e adotantes.
| Nome                  | Função                   |
| --------------------- | ------------------------ |
| **Virginia Oliveira** | Apresentação, Front-end  |
| **Sofia Marques**     | Apresentação, Front-end  |
| **Letícia Rodrigues** | Equipe de Apoio          |
| **Ana Julia**         | Banco de Dados           |
| **Gabriel Bonfim**    | Banco de Dados, Back-end |

🚀 Executar o Projeto
🔧 Pré-requisitos

Antes de começar, você precisa ter instalado:

Git
Tudo que estiver listado no requirements.txt
Um editor de código (como o VSCode)

▶️ Como Rodar o Projeto
# 1️⃣ Clone o repositório
git clone https://github.com/virginiaoliveira-jpg/sistema_adocao.git

# 2️⃣ Acesse a pasta do projeto
cd sistema_adocao

# 3️⃣ Instale as dependências
pip install -r requirements.txt

# 4️⃣ Execute o sistema
python app.py

🌐 Repositório Oficial

📎 https://github.com/virginiaoliveira-jpg/sistema_adocao

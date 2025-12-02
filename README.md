# 🏫 Backend EdTech MVP

Este repositório contém o projeto MVP do back-end para um sistema EdTech, desenvolvido como parte do sprint Fullstack do programa de pós-graduação em Engenharia de Software Puc-Rio. O objetivo é fornecer uma base sólida para aplicações educacionais, com foco em boas práticas de desenvolvimento.

---

## 🚀 Descrição

O projeto implementa um back-end completo utilizando Python e Flask, ideal para gerenciar funcionalidades essenciais de uma plataforma educacional, como cadastro, listagem e deleção de usuários, além de cadastro e listagem de atividades.

---

## ⚙️ Instruções de Instalação

Siga os passos abaixo para configurar o ambiente local e iniciar o projeto:

### 1. Clone o repositório

```bash
git clone https://github.com/leobri93/postgraduate-software-engineer-backend-edtech.git
cd postgraduate-software-engineer-backend-edtech
```

### 2. Crie e ative um ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Docker

O arquivo docker ja encontra-se no projeto para criar o container basta rodar o comando:

```bash
docker-compose up --build
```
Abra o navegador e acesse http://localhost:8080 automaticamente será redirecionado para a rota /openapi com as documentações OpenAPI do projeto.

---

### 5. Fluxograma do projeto

<img width="821" height="614" alt="image" src="https://github.com/user-attachments/assets/b093499d-0a7f-48f7-8265-5caf45dbcb98" />


## 💡 Observações

- Requer Python 3.8 ou superior.
- Para dúvidas ou sugestões, abra uma issue neste repositório.

---

## 📄 Licença

Este projeto é para fins educacionais.

---

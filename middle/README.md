# Gestão de energia residencial

Este serviço atua como **middleware** entre o Frontend e o Backend, responsável por lidar com autenticação, roteamento de requisições e orquestração de dados no sistema de gestão de energia.

## ⚙️ Pré-requisitos

- **Docker** e **Docker Compose** instalados  
- **Make** (opcional, mas recomendado)

---

## 🚀 Executando o projeto

### 1. Crie o arquivo `.env` no diretório do projeto, coloque nesse arquivo as variáveis de ambiente necessárias para o acesso ao banco de desenvolvimento.

```
BACKEND_BASE_URL=http://backend:8000
```

### 2. Suba o container

```
make up
ou 
docker compose up --build
```

e pronto, a aplicação esta rodando

### (opcional) 3. executando os testes

```
make test
ou
docker compose run --rm middle pytest -v
```
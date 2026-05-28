# Site Paróquia Divino Espírito Santo

Site oficial da Paróquia Divino Espírito Santo de Holambra, com sistema de notícias gerenciado por painel admin.

## Arquitetura

```
Frontend (GitHub Pages) → API REST (Render) → Banco de dados (SQLite)
```

- **Frontend:** HTML + JavaScript estático hospedado no GitHub Pages
- **Backend:** Django + Django REST Framework hospedado no Render
- **Autenticação:** JWT com senha customizada de admin

## Estrutura do Repositório

```
siteparoquia/
├── paroquia-divino-espirito-santo.html   # Frontend completo (uma página)
├── config.js                             # Configurações do frontend (não usado ativamente)
├── manage.py                             # CLI do Django
├── requirements.txt                      # Dependências Python
├── Dockerfile                            # Configuração Docker para o Render
├── render.yaml                           # Configuração de deploy no Render
├── config/
│   ├── settings.py                       # Configurações do Django
│   ├── urls.py                           # Rotas principais
│   └── wsgi.py                           # WSGI para produção
└── api/
    ├── models.py                         # Modelo de Notícia
    ├── serializers.py                    # Serializers DRF
    ├── views.py                          # ViewSets e lógica de autenticação
    ├── urls.py                           # Rotas da API
    └── admin.py                          # Painel admin Django
```

## Endpoints da API

| Método | Endpoint | Acesso | Descrição |
|--------|----------|--------|-----------|
| POST | `/api/news/login/` | Público | Login com senha, retorna token JWT |
| GET | `/api/news/` | Público | Lista todas as notícias |
| POST | `/api/news/` | Autenticado | Cria uma nova notícia |
| DELETE | `/api/news/{id}/` | Autenticado | Remove uma notícia |

## Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| `SECRET_KEY` | Chave secreta do Django | `django-insecure-...` |
| `DEBUG` | Modo de depuração | `false` |
| `ADMIN_PASSWORD` | Senha do painel admin | `minhasenha123` |
| `ALLOWED_HOSTS` | Domínios permitidos | `siteparoquia1.onrender.com,localhost` |
| `FRONTEND_URL` | URL do GitHub Pages | `https://usuario.github.io/repo` |
| `DATABASE_URL` | URL do banco (opcional) | `sqlite:///db.sqlite3` |

## Deploy

### Backend — Render

1. Suba o repositório no GitHub
2. Crie uma conta em [render.com](https://render.com)
3. Crie um novo **Web Service** e conecte o repositório
4. O `render.yaml` configura tudo automaticamente
5. Adicione as variáveis de ambiente em **Settings → Environment**

> ⚠️ O plano gratuito do Render "dorme" após 15 minutos sem uso. A primeira requisição pode demorar ~30 segundos.

### Frontend — GitHub Pages

1. Vá em **Settings → Pages** no repositório
2. Selecione a branch `main` e a pasta raiz `/`
3. O site ficará disponível em `https://usuario.github.io/nome-do-repositorio`
4. Certifique-se que a variável `API_BASE_URL` no HTML aponta para a URL do Render:

```js
const API_BASE_URL = 'https://siteparoquia1.onrender.com/api';
```

## Como Usar o Painel Admin

1. Acesse o site pelo GitHub Pages
2. Clique no ícone de admin (discreto no rodapé)
3. Digite a senha configurada em `ADMIN_PASSWORD` no Render
4. Crie, visualize ou delete notícias

## Segurança

- Nunca suba o arquivo `.env` com senhas reais para o repositório
- Use sempre `DEBUG=false` em produção
- Troque a `ADMIN_PASSWORD` por uma senha forte
- O Render oferece HTTPS automaticamente no plano gratuito

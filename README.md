# Backend API — Paróquia Divino Espírito Santo

API REST em Django para gerenciar notícias da paróquia com autenticação por senha e armazenamento compartilhado.

## Setup Local

### 1. Criar ambiente virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Mac/Linux
```

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```

### 3. Criar arquivo `.env`
Copie `.env.example` para `.env` e configure:
```bash
cp .env.example .env
```

Edite os valores (principalmente `SECRET_KEY` deve ser único para produção).

### 4. Executar migrações
```bash
python manage.py migrate
```

### 5. Criar superuser (admin)
```bash
python manage.py createsuperuser
```

### 6. Rodar servidor local
```bash
python manage.py runserver
```

Acesse `http://localhost:8000/api/` para ver a API.

## Endpoints

### Login
**POST** `/api/news/login/`
```json
{
  "password": "paroquia2024"
}
```
Resposta:
```json
{
  "access": "token_jwt_aqui",
  "refresh": "refresh_token_aqui"
}
```

### Listar notícias (público)
**GET** `/api/news/`

### Criar notícia (autenticado)
**POST** `/api/news/`
```json
{
  "titulo": "Missa Especial",
  "categoria": "Evento",
  "data": "2026-06-01",
  "texto": "Descrição da notícia",
  "image": null  // ou arquivo multipart
}
```
Header necessário:
```
Authorization: Bearer <access_token>
```

### Deletar notícia (autenticado)
**DELETE** `/api/news/{id}/`
Header:
```
Authorization: Bearer <access_token>
```

## Deploy em Render

### Opção 1: Usar `render.yaml` (automático)
1. Fazer push do repositório para GitHub
2. Conectar repositório no Render
3. Render lerá `render.yaml` e fará deploy automático

### Opção 2: Deploy manual
1. Criar novo Web Service no Render
2. Conectar repositório
3. Configurar:
   - **Runtime**: Python 3.11
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate`
   - **Start Command**: `gunicorn config.wsgi:application --bind 0.0.0.0:8000`
4. Adicionar variáveis de ambiente (Settings → Environment):
   - `SECRET_KEY`: gerar chave aleatória (comando abaixo)
   - `DEBUG`: `false`
   - `ADMIN_PASSWORD`: sua senha de admin
   - `ALLOWED_HOSTS`: `seu-servidor.onrender.com,localhost`
   - `FRONTEND_URL`: URL do seu GitHub Pages

Gerar SECRET_KEY:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Variáveis de Ambiente no Render
Adicione na seção "Environment Variables":
- `DEBUG=false`
- `SECRET_KEY=<chave_aleatória>`
- `ADMIN_PASSWORD=paroquia2024`
- `ALLOWED_HOSTS=seu-app.onrender.com`
- `FRONTEND_URL=https://seu-usuario.github.io/seu-repo`

## Arquitetura

- **Frontend**: HTML + JavaScript (GitHub Pages)
- **Backend**: Django + DRF (Render)
- **DB**: SQLite (local) / Postgres (Render)
- **Auth**: JWT + senha customizada

## Estrutura de Pastas

```
backend-django/
├── config/
│   ├── settings.py      # Configurações Django
│   ├── urls.py          # Rotas principais
│   └── wsgi.py          # WSGI para produção
├── api/
│   ├── models.py        # Modelo de Notícia
│   ├── serializers.py   # Serializers DRF
│   ├── views.py         # ViewSets e lógica
│   ├── urls.py          # Rotas da API
│   └── admin.py         # Admin Django
├── manage.py
├── requirements.txt
├── .env.example
├── Dockerfile
└── render.yaml          # Config Render
```

## Segurança

⚠️ **Nunca** commit `.env` com valores reais!

Boas práticas:
- Usar variáveis de ambiente para senhas e chaves
- Mudar `SECRET_KEY` em produção
- Usar `DEBUG=false` em produção
- Usar HTTPS (Render oferece automaticamente)
- Limitar CORS apenas aos domínios necessários

## Troubleshooting

### Erro: `ModuleNotFoundError: No module named 'rest_framework'`
Rode: `pip install -r requirements.txt`

### Erro: `CORS error` no frontend
Verifique se `CORS_ALLOWED_ORIGINS` inclui o URL do seu frontend em `settings.py`.

### Erro: `No such table: api_news`
Execute: `python manage.py migrate`

### Erro ao fazer upload de imagem
Certifique-se que `Pillow` está instalado: `pip install Pillow`

## Contato

Para dúvidas, consulte a documentação de:
- [Django](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Render Docs](https://render.com/docs)

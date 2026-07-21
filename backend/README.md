# Clinic CRM Backend

Backend для CRM клініки на FastAPI. Проєкт запускається через Docker Compose і піднімає API, PostgreSQL, поштовий сервіс
для локальної розробки та файлове сховище MinIO.

## Dev запуск

1. Створити локальний `.env` файл:

```bash
cp .env.sample .env
```

2. Запустити проєкт:

```bash
docker compose -f docker-compose-dev.yml up --build
```

3. Відкрити новий термінал і створити першого адміністратора:

```bash
docker compose -f docker-compose-dev.yml exec web python src/create_initial_admin.py --email admin@admin.com
```

4. Ввести пароль адміністратора і повторити його для підтвердження.

## Production запуск

1. Створити production env файл:

```bash
cp .env.prod.sample .env.prod
```

2. Заповнити `.env.prod` production значеннями: сильні secrets, production database password, `FRONTEND_BASE_URL`, SMTP та S3 credentials.

3. Запустити production compose:

```bash
docker compose -f docker-compose-prod.yml up --build -d
```

4. Створити першого адміністратора:

```bash
docker compose -f docker-compose-prod.yml run --rm web python src/create_initial_admin.py --email admin@admin.com
```

5. Ввести пароль адміністратора і повторити його для підтвердження.

## Доступні сторінки

- API Swagger docs: http://0.0.0.0:8000/docs
- MailHog: http://localhost:8025/
- MinIO storage: http://localhost:9001/clinic-storage

## Корисно знати

- Dev конфіг: `.env` + `docker-compose-dev.yml`
- Production конфіг: `.env.prod` + `docker-compose-prod.yml`
- У Docker Compose запускай команди через service name `web`, а не через container name.
- Email для першого адміна з прикладу: `admin@admin.com`

# Clinic CRM Backend

Backend для CRM клініки на FastAPI. Проєкт запускається через Docker Compose і піднімає API, PostgreSQL, поштовий сервіс для локальної розробки та файлове сховище MinIO.

## Швидкий запуск

1. Створити локальний `.env` файл:

```bash
cp .env.sample .env
```

2. Запустити проєкт:

```bash
docker compose up --build
```

3. Відкрити новий термінал і створити першого адміністратора:

```bash
docker exec -it backend_clinic python create_initial_admin.py --email admin@admin.com
```

4. Ввести пароль адміністратора і повторити його для підтвердження.

## Доступні сторінки

- API Swagger docs: http://0.0.0.0:8000/docs
- MailHog: http://localhost:8025/
- MinIO storage: http://localhost:9001/clinic-storage

## Корисно знати

- Контейнер backend: `backend_clinic`
- Email для першого адміна з прикладу: `admin@admin.com`
- Значення для локального запуску беруться з `.env`

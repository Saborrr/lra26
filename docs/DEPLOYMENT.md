# Развёртывание LRA-26 по адресу `/lra26/`

Инструкция рассчитана на сервер, где `gofaraway.mooo.com` уже обслуживается через HTTPS, а 3x-ui работает отдельно.

## 1. Подготовка

Не изменяйте рабочие inbound/outbound-настройки 3x-ui. Перед началом сохраните:

- резервную копию конфигурации Nginx/Caddy;
- резервную копию базы 3x-ui;
- список занятых портов: `sudo ss -tulpn`;
- текущую проверку: `sudo nginx -t`.

Приложение использует только локальный порт `127.0.0.1:8088`. Порты PostgreSQL, Redis и Django наружу не открываются.

## 2. Конфигурация приложения

```bash
git clone https://github.com/Saborrr/lra26.git
cd lra26
cp .env.example .env
chmod 600 .env
```

Создайте секреты:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
python3 -c "import secrets; print(secrets.token_urlsafe(36))"
```

Первое значение используйте как `SECRET_KEY`, второе как `POSTGRES_PASSWORD`. Не отправляйте `.env` в чат, issue или Git.

Обязательные production-значения:

```dotenv
DEBUG=False
ALLOWED_HOSTS=gofaraway.mooo.com
APP_BASE_PATH=/lra26
APP_PUBLIC_URL=https://gofaraway.mooo.com/lra26/
CORS_ALLOWED_ORIGINS=https://gofaraway.mooo.com
CSRF_TRUSTED_ORIGINS=https://gofaraway.mooo.com
```

## 3. Первый запуск

```bash
docker compose config
docker compose build --pull
docker compose up -d
docker compose ps
docker compose exec backend python manage.py createsuperuser
```

Проверьте локальный proxy:

```bash
curl -I http://127.0.0.1:8088/lra26/
curl http://127.0.0.1:8088/lra26/api/health/
```

## 4. Подключение к существующему домену

Добавьте содержимое `deploy/nginx-lra26.conf` внутрь уже существующего `server { ... }` для `gofaraway.mooo.com`.

```bash
sudo nginx -t
sudo systemctl reload nginx
```

Если Nginx работает в Docker, адрес `127.0.0.1:8088` должен быть доступен из его network namespace. В таком случае используйте общий Docker network или host gateway, но не публикуйте backend/Redis/PostgreSQL.

Проверьте:

```bash
curl -I https://gofaraway.mooo.com/lra26/
curl https://gofaraway.mooo.com/lra26/api/health/
```

## 5. Telegram

1. Создайте или выберите бота через `@BotFather`.
2. Поместите токен в `TELEGRAM_BOT_TOKEN` и перезапустите `bot`.
3. В BotFather настройте Menu Button с URL `https://gofaraway.mooo.com/lra26/`.
4. Не используйте Telegram user ID как доказательство личности. Приложение проверяет подписанный `initData` на сервере.
5. Для первой привязки суперадминистратор выдаёт одноразовый код в разделе «Система».

## 6. VK Mini App

1. Зарегистрируйте Mini App в кабинете разработчика VK.
2. Укажите URL приложения `https://gofaraway.mooo.com/lra26/` для Web/Mobile.
3. Запишите секрет приложения в `VK_APP_SECRET`.
4. Разрешайте только production URL. Backend проверяет подпись launch parameters.

## 7. Установка на телефон

- iPhone/iPad: Safari → «Поделиться» → «На экран Домой».
- Android: Chrome → «Установить приложение».
- Telegram/VK: приложение открывается внутри соответствующего клиента без отдельной установки.

## 8. Резервные копии

Создание дампа:

```bash
docker compose exec -T postgres pg_dump -U lra26 -d lra26 --format=custom > lra26-$(date +%F).dump
```

Храните дампы зашифрованными и отдельно от VPS. Регулярно проверяйте восстановление на тестовой базе.

## 9. Обновление

```bash
git pull --ff-only
docker compose build --pull
docker compose up -d
docker compose ps
```

Миграции применяются backend-контейнером перед запуском Daphne. Перед крупным обновлением обязательно создайте дамп PostgreSQL.

## 10. Диагностика

```bash
docker compose ps
docker compose logs --tail=200 backend
docker compose logs --tail=200 frontend
docker compose logs --tail=200 bot
```

Не публикуйте логи целиком: сначала удалите токены, cookie, Telegram init data, VK launch parameters, телефоны и другие персональные данные.

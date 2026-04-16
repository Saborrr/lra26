# LRA-26 Live Leaderboard 🏆

[![Stars](https://img.shields.io/github/stars/Saborrr/lra26)](https://github.com/Saborrr/lra26)
[![Django](https://img.shields.io/badge/Django-5.1-blue.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-green.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-blue.svg)](https://docker.com/)
[![MIT License](https://img.shields.io/github/license/Saborrr/lra26)](LICENSE)

**Live рейтинг команд Слёта Лидеров Рабочего Актива 2026 (EFKO).**  
Real-time leaderboard, квесты, оценки, Telegram-бот.

---

## 🚀 Возможности
- 📊 Live-лидерборд с WebSocket обновлениями (космический дизайн)
- 👨‍🏫 Интерфейс тренеров — выставление оценок через веб
- 🤖 Telegram-бот — `/teams`, `/addscore`, `/myteam`
- 🔐 JWT авторизация + Django Admin
- ⚫ Чёрные метки (штрафы) для команд
- 📱 Адаптивный мобильный UI
- 🛠️ Dev/prod настройки (SQLite/PostgreSQL)
- 📦 Docker Compose для продакшена

---

## 📁 Структура проекта
```
lra26/
├── backend/                # Django 5.1 + DRF + Channels + Daphne
│   ├── manage.py
│   ├── backend/            # настройки проекта
│   │   ├── settings/       # base / development / production
│   │   ├── urls.py
│   │   ├── asgi.py         # WebSocket (Daphne)
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── teams/          # Команды
│   │   ├── scores/         # Оценки за квесты
│   │   ├── quests/         # Квесты/задания
│   │   ├── trainers/       # Тренеры
│   │   └── penalties/      # Чёрные метки (штрафы)
│   ├── api/                # API endpoints
│   ├── ws/                 # WebSocket consumer
│   ├── bot/                # Telegram-бот
│   ├── templates/          # HTML шаблоны (лидерборд, трейнерская)
│   └── requirements/       # base / development / production.txt
├── frontend/               # React + Vite + TypeScript
│   ├── package.json
│   ├── vite.config.ts
│   └── src/
├── docker-compose.yml
└── README.md
```

---

## 🛠️ Локальный запуск (разработка)

### Предварительные требования
- Python 3.11+
- Node.js 18+
- Git

### 1. Клонирование
```bash
git clone git@github.com:Saborrr/lra26.git
cd lra26
```

### 2. Backend
```bash
cd backend

# Создать виртуальное окружение
python -m venv venv

# Активация (Windows)
source venv/Scripts/activate
# или (Linux/Mac)
source venv/bin/activate

# Установка зависимостей
pip install -r requirements/development.txt

# Создать .env файл
cp .env.example .env
# Отредактируйте .env — минимум: SECRET_KEY, DEBUG=True

# Миграции БД
python manage.py migrate

# Создать суперюзера (для админки)
python manage.py createsuperuser

# Запуск сервера (ASGI/Daphne — поддерживает WebSocket)
python manage.py runserver 127.0.0.1:8000
```

Backend будет доступен:
- **Лидерборд**: http://127.0.0.1:8000/
- **Трейнерская**: http://127.0.0.1:8000/trainer/
- **Админка**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/leaderboard/

### 3. Frontend (опционально, React)
```bash
cd frontend
npm install
npm run dev    # http://localhost:3000
```

> ⚠️ На Windows + Node 18 есть баг IPv6 proxy. Фронтенд ходит напрямую
> в Django API (`http://127.0.0.1:8000/api/`), CORS настроен.

### 4. Telegram-бот (опционально)
```bash
cd backend
source venv/Scripts/activate

# Установите токен бота в .env:
# TELEGRAM_BOT_TOKEN=your-bot-token-here

# Запуск бота (в отдельном терминале)
python manage.py runbot
```

---

## 🤖 Настройка Telegram-бота

### Создание бота
1. Откройте [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot`
3. Укажите имя: `ЛРА-2026 Рейтинг`
4. Укажите username: `lra26_score_bot` (или любой свободный)
5. Скопируйте полученный **токен** (вида `1234567890:ABCdef...`)

### Конфигурация
Добавьте токен в `backend/.env`:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdef...
```

### Команды бота
| Команда | Описание |
|---------|----------|
| `/start` | Приветствие |
| `/teams` | Топ-10 команд |
| `/myteam` | Информация о вашей команде |
| `/addscore` | Внести результат (интерактивные кнопки) |
| `/login <код>` | Привязать Telegram к аккаунту тренера |

### Привязка тренера к Telegram
1. Создайте тренера в Django Admin (`/admin/trainers/trainer/`)
2. Тренер отправляет боту `/login <код>`
3. Его `telegram_id` привязывается к модели Trainer

---

## 📱 Настройка VK Mini App (планируется)

Для интеграции с ВКонтакте можно использовать [VK Mini Apps](https://dev.vk.com/mini-apps):

1. Создайте приложение в [VK Developer](https://dev.vk.com/)
2. Тип: **Mini App** (IFrame)
3. URL: укажите URL вашего фронтенда
4. Используйте [VK Bridge](https://dev.vk.com/mini-apps/development/bridge)
   для авторизации пользователей через VK

На данный момент VK интеграция **не реализована**.  
Основной интерфейс — веб-страницы leaderboard и trainer panel.

---

## 🔌 API Endpoints

| Endpoint | Метод | Описание |
|----------|-------|----------|
| `/api/leaderboard/` | GET | Рейтинг команд (public) |
| `/api/my-team/` | GET | Команда текущего тренера (auth) |
| `/api/teams/` | GET/POST | CRUD команд |
| `/api/scores/` | GET/POST | CRUD оценок |
| `/api/quests/` | GET/POST | CRUD квестов |
| `/api/trainers/` | GET/POST | CRUD тренеров |
| `/api/marks/` | GET/POST | CRUD чёрных меток |
| `/ws/leaderboard/` | WS | Real-time обновления |

---

## 🧪 Тесты
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run lint
```

---

## 📦 Docker Compose (продакшен)
```bash
docker compose up -d
```

Сервисы:
- **backend** — Daphne на порту 8000
- **frontend** — Nginx на порту 80
- **redis** — для Channels layer
- **bot** — Telegram-бот

---

## 👨‍🏫 Интерфейс тренера

Тренеры могут выставлять оценки через веб:  
**URL**: http://127.0.0.1:8000/trainer/

1. Выберите квест из списка активных
2. Для каждой команды выставьте баллы
3. Нажмите «Сохранить все оценки»
4. Данные мгновенно обновятся на лидерборде

---

## 🚀 Деплой
GitHub Actions auto-tests на PR в main.  
Деплой: VPS с Docker Compose + Nginx reverse proxy.

---

## 📝 Лицензия
MIT © Saborrr
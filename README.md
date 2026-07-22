<div align="center">

<a href="https://gofaraway.mooo.com/lra26/">
  <img src="frontend/public/icons/icon.svg" width="112" alt="Логотип LRA-26" />
</a>

# LRA-26

### Live Space Ranking

Космическая платформа командных соревнований с живым рейтингом, кабинетами участников и разграничением прав.

[![CI](https://github.com/Saborrr/lra26/actions/workflows/ci.yml/badge.svg)](https://github.com/Saborrr/lra26/actions/workflows/ci.yml)
[![CodeQL](https://github.com/Saborrr/lra26/actions/workflows/codeql.yml/badge.svg)](https://github.com/Saborrr/lra26/actions/workflows/codeql.yml)
[![Django 6.0.7](https://img.shields.io/badge/Django-6.0.7-092E20?logo=django&logoColor=white)](backend/requirements/base.txt)
[![React 19.2.8](https://img.shields.io/badge/React-19.2.8-61DAFB?logo=react&logoColor=08121a)](frontend/package-lock.json)
[![TypeScript 7](https://img.shields.io/badge/TypeScript-7.0.2-3178C6?logo=typescript&logoColor=white)](frontend/package-lock.json)
[![PWA](https://img.shields.io/badge/PWA-installable-7967ff?logo=pwa&logoColor=white)](frontend/vite.config.ts)
[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial-48e5ff)](LICENSE)

**Русский** · [English](README_EN.md) · [Демо без установки](index.html) · [Развёртывание](docs/DEPLOYMENT.md)

</div>

<p align="center">
  <img src="docs/assets/lra26-cosmic-dashboard.svg" width="100%" alt="Космический интерфейс LRA-26 с рейтингом команд" />
</p>

<p align="center"><sub>Стартовый экран и live-рейтинг. В приложении звёздное поле плавно движется и мерцает.</sub></p>

## О проекте

**LRA-26** объединяет публичный рейтинг, личный кабинет, управление соревнованием и интеграции с мессенджерами в одном адаптивном PWA. Один интерфейс работает в обычном браузере, устанавливается на iPhone и Android, открывается как Telegram Mini App и VK Mini App.

> Хотите только посмотреть дизайн? Скачайте ZIP, распакуйте архив и откройте корневой `index.html` двойным щелчком. Это автономное интерактивное демо с тестовыми данными: сервер, Python и Node.js не нужны.

## Возможности

| Для участников | Для организаторов | Для платформ |
|---|---|---|
| Live-рейтинг и личный прогресс | Команды, задания, баллы и штрафы | Web и устанавливаемое PWA |
| Текущая команда и активные задания | Одноразовые коды привязки | iPhone, iPad и Android |
| Обновления через WebSocket | Роли администратора и суперадминистратора | Telegram Bot и Mini App |
| Адаптивный космический интерфейс | Журнал привилегированных действий | VK Mini App |

### Роли и права

| Роль | Доступ |
|---|---|
| **Участник** | Публичный рейтинг, собственная команда, баллы и задания |
| **Администратор** | Управление командами, квестами, результатами, штрафами и кодами привязки |
| **Суперадминистратор** | Все права администратора, пользователи, роли и полный журнал действий |

Публичный пользователь не может читать внутренние результаты или изменять данные. Операции с баллами, штрафами и правами фиксируются в журнале.

## Технологии

Версии ниже взяты непосредственно из файлов зависимостей и Docker-образов проекта.

| Слой | Технологии |
|---|---|
| Backend | Python 3.14 в контейнере, Django 6.0.7, Django REST Framework 3.17.1, Channels 4.3.2, Daphne 4.2.3 |
| Frontend | React 19.2.8, React Router 7.18.1, TypeScript 7.0.2, Vite 8.1.5, TanStack Query 5 |
| Данные | PostgreSQL 17, Redis 8 |
| Интеграции | python-telegram-bot 22.8, VK Bridge 3.0.2 |
| Инфраструктура | Docker Compose, Node.js 26 и Nginx 1.31 в контейнерах, GitHub Actions, CodeQL, Dependabot |

`Django~=6.0.7` разрешает совместимые исправления в ветке 6.0, а `package-lock.json` фиксирует React на версии 19.2.8. React 20 в проекте не используется.

## Архитектура

```text
Browser · PWA · Telegram · VK
               │
         /lra26/ · HTTPS
               │
          Nginx frontend
       ┌───────┼────────┐
       │       │        │
   React PWA  /api     /ws
               │        │
               └── Django ASGI ── PostgreSQL
                        │
                       Redis

Telegram bot ── Django services ── PostgreSQL
```

В production наружу публикуется только `127.0.0.1:8088`. Backend, PostgreSQL и Redis остаются во внутренней Docker-сети.

## Быстрый старт

### 1. Автономное демо без установки

1. Нажмите **Code → Download ZIP** на GitHub.
2. Полностью распакуйте архив.
3. Откройте файл `index.html` из корня папки в Chrome, Edge, Firefox или Safari.

В демо можно переключаться между публичным рейтингом, кабинетом участника и управлением. Изменения не сохраняются.

### 2. Полноценный локальный запуск

Понадобятся **Git**, **Python 3.12–3.14** и **Node.js 22.12+**. Redis для первого запуска необязателен: в development используется встроенный channel layer. Для окружения, максимально близкого к серверу, установите [Docker Desktop для Windows](https://docs.docker.com/desktop/setup/install/windows-install/) или [Docker Desktop для macOS](https://docs.docker.com/desktop/setup/install/mac-install/).

<details open>
<summary><strong>Windows 10/11 · PowerShell</strong></summary>

Скачайте и установите [Python](https://www.python.org/downloads/windows/), [Node.js](https://nodejs.org/en/download) и [Git](https://git-scm.com/download/win), затем откройте PowerShell:

```powershell
git clone https://github.com/Saborrr/lra26.git
cd lra26

cd backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements\development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Если установлена Python 3.13 или 3.12, замените `-3.14` соответствующим номером. Если PowerShell запрещает активацию, один раз выполните `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` и повторите команду активации.

Оставьте backend запущенным. Откройте **второе окно PowerShell**:

```powershell
cd путь\к\lra26\frontend
npm ci
npm run dev
```

</details>

<details>
<summary><strong>macOS · Terminal</strong></summary>

Установите [Python](https://www.python.org/downloads/macos/), [Node.js](https://nodejs.org/en/download) и Git. Затем:

```bash
git clone https://github.com/Saborrr/lra26.git
cd lra26/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Оставьте backend запущенным. Откройте **второе окно Terminal**:

```bash
cd /путь/к/lra26/frontend
npm ci
npm run dev
```

</details>

<details>
<summary><strong>Linux · bash/zsh</strong></summary>

Установите Git, Python 3.12+ с модулем `venv` и Node.js 22.12+. Затем выполните те же POSIX-команды:

```bash
git clone https://github.com/Saborrr/lra26.git
cd lra26/backend
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Во втором терминале:

```bash
cd /путь/к/lra26/frontend
npm ci
npm run dev
```

</details>

После запуска откройте **http://localhost:5173/lra26/**. Django API работает на `http://127.0.0.1:8000`, а Vite автоматически проксирует запросы `/api` и `/ws`.

### 3. Docker Compose и сервер

Docker используется для production-развёртывания всего стека: frontend, backend, PostgreSQL, Redis и Telegram-бот.

**macOS/Linux:**

```bash
cp .env.example .env
# Заполните SECRET_KEY, POSTGRES_PASSWORD и остальные production-параметры
docker compose config
docker compose build --pull
docker compose up -d
docker compose exec backend python manage.py createsuperuser
```

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
# Заполните SECRET_KEY, POSTGRES_PASSWORD и остальные production-параметры
docker compose config
docker compose build --pull
docker compose up -d
docker compose exec backend python manage.py createsuperuser
```

Не запускайте production-файл `.env` с демонстрационными секретами. Полная инструкция для `https://gofaraway.mooo.com/lra26/`, reverse proxy, резервных копий, Telegram и VK находится в [руководстве по развёртыванию](docs/DEPLOYMENT.md).

## Установка на телефон и интеграции

- **iPhone/iPad:** откройте HTTPS-версию в Safari → «Поделиться» → «На экран Домой».
- **Android:** откройте сайт в Chrome → «Установить приложение».
- **Telegram:** Mini App открывает тот же PWA; backend проверяет подпись и срок действия `initData`.
- **VK:** Mini App использует официальный VK Bridge; launch parameters проверяются на сервере с `VK_APP_SECRET`.

Бот поддерживает `/start`, `/teams`, `/myteam`, `/login КОД` и административную команду `/addscore`.

## Проверка проекта

```bash
cd backend
ruff check .
ruff format --check .
pytest --cov=apps --cov-fail-under=80
pip-audit -r requirements/production.txt

cd ../frontend
npm ci
npm run check
npm run build
npm audit --omit=dev
```

GitHub Actions дополнительно проверяет Docker-образы и выполняет CodeQL-анализ Python и JavaScript/TypeScript.

## Безопасность

- Argon2 для паролей, короткоживущий access JWT и ротируемый refresh cookie.
- Role-based permissions для участника, администратора и суперадминистратора.
- Rate limiting, ограничения на уровне API и базы данных.
- Проверка Origin для WebSocket и подписей Telegram/VK на backend.
- CSP, `nosniff`, Referrer Policy и ограничение browser permissions.
- Контейнеры без root с read-only filesystem и `no-new-privileges`.
- Секреты через `.env`, исключённый из Git.
- Журнал привилегированных операций.

Сообщайте об уязвимостях приватно по правилам [SECURITY.md](SECURITY.md). Не публикуйте токены, cookie, содержимое `.env`, launch parameters или персональные данные в Issue.

## Структура

```text
lra26/
├── backend/              Django, REST API, WebSocket и Telegram bot
├── frontend/             React PWA и адаптеры платформ
├── deploy/               Конфигурация reverse proxy
├── docs/                 Развёртывание и изображения
├── docker-compose.yml    Production-стек
├── index.html            Автономное интерактивное демо
└── README_EN.md          English documentation
```

## Лицензирование

Код распространяется по [PolyForm Noncommercial License 1.0.0](LICENSE). Личное, учебное и другое некоммерческое использование разрешено при сохранении уведомления об авторе и ссылки на исходный проект.

Коммерческое использование, SaaS, перепродажа или применение в деятельности, приносящей доход, требуют отдельного [коммерческого соглашения](COMMERCIAL_LICENSE.md) с Aleksandr Fadeev. В соглашении могут использоваться фиксированная плата, подписка или процент от выручки.

Это **source-available**, а не OSI-совместимый open source проект.

## Автор

<div align="center">

**Aleksandr Fadeev**

[@Saborrr](https://github.com/Saborrr) · [Исходный проект](https://github.com/Saborrr/lra26) · [Коммерческие условия](COMMERCIAL_LICENSE.md)

<sub>© 2026 Aleksandr Fadeev. LRA-26 · Live Space Ranking.</sub>

</div>

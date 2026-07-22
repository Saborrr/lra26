<div align="center">

<a href="https://gofaraway.mooo.com/lra26/">
  <img src="frontend/public/icons/icon.svg" width="112" alt="LRA-26 logo" />
</a>

# LRA-26

### Live Space Ranking

A space-themed team competition platform with a live leaderboard, participant dashboards, and role-based administration.

[![CI](https://github.com/Saborrr/lra26/actions/workflows/ci.yml/badge.svg)](https://github.com/Saborrr/lra26/actions/workflows/ci.yml)
[![CodeQL](https://github.com/Saborrr/lra26/actions/workflows/codeql.yml/badge.svg)](https://github.com/Saborrr/lra26/actions/workflows/codeql.yml)
[![Django 6.0.7](https://img.shields.io/badge/Django-6.0.7-092E20?logo=django&logoColor=white)](backend/requirements/base.txt)
[![React 19.2.8](https://img.shields.io/badge/React-19.2.8-61DAFB?logo=react&logoColor=08121a)](frontend/package-lock.json)
[![TypeScript 7](https://img.shields.io/badge/TypeScript-7.0.2-3178C6?logo=typescript&logoColor=white)](frontend/package-lock.json)
[![PWA](https://img.shields.io/badge/PWA-installable-7967ff?logo=pwa&logoColor=white)](frontend/vite.config.ts)
[![License](https://img.shields.io/badge/license-PolyForm%20Noncommercial-48e5ff)](LICENSE)

[Русский](README.md) · **English** · [No-install demo](index.html) · [Deployment](docs/DEPLOYMENT.md)

</div>

<p align="center">
  <img src="docs/assets/lra26-cosmic-dashboard.svg" width="100%" alt="LRA-26 space-themed team leaderboard" />
</p>

<p align="center"><sub>Landing page and live leaderboard. The real application renders a slowly moving, twinkling starfield.</sub></p>

## About

**LRA-26** brings a public leaderboard, participant area, competition administration, and messenger integrations into one responsive PWA. The same interface runs in a regular browser, installs on iPhone and Android, and opens as a Telegram Mini App or VK Mini App.

> Want to see the design first? Download and extract the repository ZIP, then double-click the root `index.html`. It is a self-contained interactive demo with sample data and needs no server, Python, Node.js, or database.

## Highlights

| Participants | Organizers | Platforms |
|---|---|---|
| Live leaderboard and personal progress | Teams, quests, scores, and penalties | Web and installable PWA |
| Current team and active quests | One-time account-link codes | iPhone, iPad, and Android |
| WebSocket-powered updates | Administrator and super-admin roles | Telegram Bot and Mini App |
| Responsive cosmic interface | Privileged activity audit trail | VK Mini App |

### Roles

| Role | Access |
|---|---|
| **Participant** | Public leaderboard, own team, scores, and quests |
| **Administrator** | Teams, quests, results, penalties, and account-link codes |
| **Super administrator** | All administrator rights, users, roles, and the complete audit trail |

Public users cannot read internal results or mutate data. Score, penalty, and permission changes are recorded in the audit trail.

## Technology

The versions below come directly from the repository dependency manifests and container images.

| Layer | Technology |
|---|---|
| Backend | Python 3.14 container, Django 6.0.7, Django REST Framework 3.17.1, Channels 4.3.2, Daphne 4.2.3 |
| Frontend | React 19.2.8, React Router 7.18.1, TypeScript 7.0.2, Vite 8.1.5, TanStack Query 5 |
| Data | PostgreSQL 17, Redis 8 |
| Integrations | python-telegram-bot 22.8, VK Bridge 3.0.2 |
| Infrastructure | Docker Compose, Node.js 26 and Nginx 1.31 containers, GitHub Actions, CodeQL, Dependabot |

`Django~=6.0.7` accepts compatible patches in the Django 6.0 line, while `package-lock.json` pins React to 19.2.8. This project does not use React 20.

## Architecture

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

Production exposes only `127.0.0.1:8088`. Django, PostgreSQL, and Redis stay on a private Docker network.

## Quick start

### 1. No-install interactive demo

1. Select **Code → Download ZIP** on GitHub.
2. Extract the archive completely.
3. Open the root `index.html` in Chrome, Edge, Firefox, or Safari.

The demo lets you switch between the public leaderboard, participant dashboard, and administration UI. Demo changes are not persisted.

### 2. Full local development setup

Install **Git**, **Python 3.12–3.14**, and **Node.js 22.12+**. Redis is optional for the first development run because the app falls back to an in-memory channel layer. For an environment closer to production, install [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) or [Docker Desktop for macOS](https://docs.docker.com/desktop/setup/install/mac-install/).

<details open>
<summary><strong>Windows 10/11 · PowerShell</strong></summary>

Install [Python](https://www.python.org/downloads/windows/), [Node.js](https://nodejs.org/en/download), and [Git](https://git-scm.com/download/win), then open PowerShell:

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

Use `-3.13` or `-3.12` if that is the Python version installed on your machine. If PowerShell blocks activation, run `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser` once and retry.

Keep the backend running and open a **second PowerShell window**:

```powershell
cd path\to\lra26\frontend
npm ci
npm run dev
```

</details>

<details>
<summary><strong>macOS · Terminal</strong></summary>

Install [Python](https://www.python.org/downloads/macos/), [Node.js](https://nodejs.org/en/download), and Git. Then run:

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

Keep the backend running and open a **second Terminal window**:

```bash
cd /path/to/lra26/frontend
npm ci
npm run dev
```

</details>

<details>
<summary><strong>Linux · bash/zsh</strong></summary>

Install Git, Python 3.12+ with `venv`, and Node.js 22.12+. Then use the POSIX setup:

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

In a second terminal:

```bash
cd /path/to/lra26/frontend
npm ci
npm run dev
```

</details>

Open **http://localhost:5173/lra26/**. Django runs at `http://127.0.0.1:8000`, and Vite proxies `/api` and `/ws` automatically.

### 3. Docker Compose and production

Docker runs the complete production stack: frontend, backend, PostgreSQL, Redis, and the Telegram bot.

**macOS/Linux:**

```bash
cp .env.example .env
# Set SECRET_KEY, POSTGRES_PASSWORD, and the remaining production values
docker compose config
docker compose build --pull
docker compose up -d
docker compose exec backend python manage.py createsuperuser
```

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
# Set SECRET_KEY, POSTGRES_PASSWORD, and the remaining production values
docker compose config
docker compose build --pull
docker compose up -d
docker compose exec backend python manage.py createsuperuser
```

Never run production with the placeholder secrets. The [deployment guide](docs/DEPLOYMENT.md) covers `https://gofaraway.mooo.com/lra26/`, reverse proxy configuration, backups, Telegram, and VK.

## Phones and platform integrations

- **iPhone/iPad:** open the HTTPS deployment in Safari → Share → Add to Home Screen.
- **Android:** open it in Chrome → Install app.
- **Telegram:** the Mini App opens the same PWA; the backend validates the signature and age of `initData`.
- **VK:** the Mini App uses the official VK Bridge; the server validates launch parameters with `VK_APP_SECRET`.

The bot supports `/start`, `/teams`, `/myteam`, `/login CODE`, and the administrative `/addscore` command.

## Quality checks

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

GitHub Actions also builds both container images and runs CodeQL for Python and JavaScript/TypeScript.

## Security

- Argon2 passwords, short-lived access JWTs, and rotating refresh cookies.
- Role-based permissions for participants, administrators, and super administrators.
- Rate limits plus API and database constraints.
- WebSocket Origin checks and server-side Telegram/VK signature validation.
- CSP, `nosniff`, Referrer Policy, and restricted browser permissions.
- Non-root containers with read-only filesystems and `no-new-privileges`.
- Secrets loaded from a Git-ignored `.env` file.
- An audit trail for privileged operations.

Report vulnerabilities privately according to [SECURITY.md](SECURITY.md). Never put tokens, cookies, `.env` contents, launch parameters, or personal data in a public issue.

## Repository layout

```text
lra26/
├── backend/              Django, REST API, WebSockets, and Telegram bot
├── frontend/             React PWA and platform adapters
├── deploy/               Reverse proxy configuration
├── docs/                 Deployment guide and media
├── docker-compose.yml    Production stack
├── index.html            Self-contained interactive demo
└── README.md             Russian documentation
```

## Licensing

The code is available under the [PolyForm Noncommercial License 1.0.0](LICENSE). Personal, educational, and other noncommercial use is permitted while preserving the required author notice and original-project link.

Commercial use, SaaS, resale, or use in revenue-generating activity requires a separate [commercial agreement](COMMERCIAL_LICENSE.md) with Aleksandr Fadeev. The agreement may use a fixed fee, subscription, or revenue-share royalty.

This is a **source-available** project, not OSI-approved open source.

## Author

<div align="center">

**Aleksandr Fadeev**

[@Saborrr](https://github.com/Saborrr) · [Source repository](https://github.com/Saborrr/lra26) · [Commercial terms](COMMERCIAL_LICENSE.md)

<sub>© 2026 Aleksandr Fadeev. LRA-26 · Live Space Ranking.</sub>

</div>

# LRA-26 Live Leaderboard 🏆

[![Stars](https://img.shields.io/github/stars/Saborrr/lra26)](https://github.com/Saborrr/lra26)
[![Django](https://img.shields.io/badge/Django-5.1-blue.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-green.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-blue.svg)](https://docker.com/)
[![MIT License](https://img.shields.io/github/license/Saborrr/lra26)](LICENSE)

**Live рейтинг команд Слёта Лидеров Рабочего Актива 2026 (EFKO).** Real-time leaderboard, quests, scores.

## 🚀 Features
- 📊 Live leaderboard with WebSocket updates
- 🔐 JWT auth + custom permissions
- 📱 Glassmorphism mobile UI with Recharts
- 🧪 Full tests (pytest, API)
- 🛠️ Dev/prod settings split
- 📦 Docker Compose for local/prod

## 📁 Structure
```
lra26/
├── backend/  # Django 5.1 + DRF + Channels
│   ├── manage.py
│   ├── backend/ # project
│   │   ├── settings/ # base/dev/prod
│   │   ├── urls.py
│   │   ├── asgi.py # WS
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── teams/ # models/views/serializers/...
│   │   ├── scores/
│   │   └── quests/
│   ├── api/ # urls/permissions
│   ├── ws/ # consumers/routing
│   ├── requirements/ # base/dev/prod.txt
│   ├── pyproject.toml
│   └── pytest.ini
├── frontend/ # React + Vite + TS
│   ├── package.json
│   ├── vite.config.ts # proxy API/WS
│   ├── tsconfig.json
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── index.css # glass UI
│       └── services/api.ts
├── .github/workflows/ # tests/deploy
├── docker-compose.yml
├── README.md
└── LICENSE
```

## 🛠️ Local Setup

### Backend
```bash
cd backend
pip install -r requirements/development.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev  # http://localhost:3000
```

### Docker
```bash
docker compose up -d
```

Backend: http://localhost:8000/admin/
Frontend: http://localhost:3000

## 🔌 API Docs
- `GET /api/teams/` - leaderboard
- `POST /api/teams/` - create team (admin)
- `GET /api/scores/` - scores
- `ws://localhost:8000/ws/leaderboard/` - live updates

## 🧪 Tests
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm run lint
```

## 🚀 Deploy
GitHub Actions auto-tests on PR/main.
Deploy: VPS with Docker Compose + Nginx.

MIT © Saborrr

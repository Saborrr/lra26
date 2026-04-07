# LRA-26 Live Leaderboard 🏆

[![Stars](https://img.shields.io/github/stars/Saborrr/lra26)](https://github.com/Saborrr/lra26)
[![Django](https://img.shields.io/badge/Django-4.2-blue.svg)](https://www.djangoproject.com/)
[![React](https://img.shields.io/badge/React-18-green.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/Docker-blue.svg)](https://docker.com/)
[![MIT License](https://img.shields.io/github/license/Saborrr/lra26)](LICENSE)

**Live рейтинг команд Слёта Лидеров Рабочего Актива 2026 (EFKO).** 7 команд, квесты, real-time results.

## 🚀 Features
- 📊 Live leaderboard (score/position auto).
- 🔐 Admin CRUD: teams/trainers/quests/results.
- ⚡ Real-time WebSocket.
- 📱 Mobile glass UI.
- 🛡️ JWT auth.

## 🛠️ Stack
| Part | Tech |
|------|------|
| Backend | Django REST + Channels |
| Frontend | React + Vite + Recharts |
| DB | SQLite |
| Deploy | Docker Compose + Nginx |

## 📦 Install
```bash
git clone https://github.com/Saborrr/lra26.git
cd lra26
docker compose up -d
```

## 📁 Structure
backend/ frontend/ docker-compose.yml

## 🔌 API
GET /api/teams/ — leaderboard.

## 🐳 Deploy VPS
docker compose up -d

## 🧪 Tests
pytest / npm test

## 🤝 Contributing
Fork/PR/tests.

MIT © Saborrr.

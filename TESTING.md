# 🧪 Инструкция по тестированию LRA-26

## 1. Подготовка окружения

### 1.1. Установите токен бота
Отредактируйте `backend/.env`:
```env
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
```
(Замените на токен от @BotFather)

### 1.2. Создайте виртуальное окружение и установите зависимости
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements/base.txt
```

### 1.3. Установите зависимости frontend
```bash
cd ../frontend
npm install
```

---

## 2. Инициализация базы данных

### 2.1. Примените миграции
```bash
cd backend
python manage.py migrate
```

### 2.2. Создайте суперпользователя
```bash
python manage.py createsuperuser
# Введите:
# - Логин: admin
# - Email: admin@example.com
# - Пароль: admin123 (или свой)
```

### 2.3. Создайте тестовые данные (опционально)
```bash
python manage.py shell
```

```python
from apps.teams.models import Team
from apps.trainers.models import Trainer
from apps.quests.models import Quest
from apps.scores.models import Score

# Создаём тренера
trainer = Trainer.objects.create(name="Иван Петров", telegram_id=123456789)
print(f"Тренер: {trainer.name}")

# Создаём команды
team1 = Team.objects.create(name="Альфа", trainer=trainer, color="#00ffff")
team2 = Team.objects.create(name="Бета", color="#ff00ff")
team3 = Team.objects.create(name="Гамма", trainer=trainer, color="#00ff88")
print(f"Команды: {team1.name}, {team2.name}, {team3.name}")

# Создаём квесты
quest1 = Quest.objects.create(title="Квиз", description="Вопросы на эрудицию", max_score=100, order=1)
quest2 = Quest.objects.create(title="Спорт", description="Эстафета", max_score=50, order=2)
quest3 = Quest.objects.create(title="Творчество", description="Конкурс песни", max_score=80, order=3)
print(f"Квесты: {quest1.title}, {quest2.title}, {quest3.title}")

# Добавляем баллы
Score.objects.create(team=team1, quest=quest1, points=85)
Score.objects.create(team=team1, quest=quest2, points=45)
Score.objects.create(team=team2, quest=quest1, points=70)
Score.objects.create(team=team3, quest=quest1, points=90)
Score.objects.create(team=team3, quest=quest3, points=75)

print("Тестовые данные созданы!")
exit()
```

---

## 3. Запуск серверов

### 3.1. Запуск Backend (Django + Channels)
Откройте терминал 1:
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```
Сервер запустится на http://localhost:8000

### 3.2. Запуск Frontend (React + Vite)
Откройте терминал 2:
```bash
cd frontend
npm run dev
```
Сервер запустится на http://localhost:5173

### 3.3. Запуск Telegram-бота
Откройте терминал 3:
```bash
cd backend
venv\Scripts\activate
python manage.py runbot
```
Вы увидите: "Запуск Telegram-бота..."

---

## 4. Тестирование API

### 4.1. Django Admin
1. Откройте http://localhost:8000/admin/
2. Войдите с логином/паролем суперпользователя
3. Проверьте, что все модели отображаются:
   - Teams (Команды)
   - Trainers (Тренеры)
   - Quests (Квесты)
   - Scores (Баллы)
   - Black Marks (Штрафы)

### 4.2. API Endpoints (через браузер или curl)

**Django Admin:** http://localhost:8000/admin/ (логин: admin, пароль: admin123)

**Рейтинг команд:**
```
http://localhost:8000/api/leaderboard/
```

**Список команд:**
```
http://localhost:8000/api/teams/
```

**Список квестов:**
```
http://localhost:8000/api/quests/
```

**Список тренеров:**
```
http://localhost:8000/api/trainers/
```

**Список баллов:**
```
http://localhost:8000/api/scores/
```

**Список штрафов:**
```
http://localhost:8000/api/marks/
```

### 4.3. Тестирование через PowerShell
```powershell
# Получить рейтинг
Invoke-WebRequest -Uri "http://localhost:8000/api/leaderboard/" | Select-Object -ExpandProperty Content

# Создать команду (требуется JWT токен)
$headers = @{ "Authorization" = "Bearer YOUR_TOKEN" }
$body = @{ name = "Дельта"; color = "#ff8800" } | ConvertTo-Json
Invoke-WebRequest -Uri "http://localhost:8000/api/teams/" -Method POST -Headers $headers -Body $body -ContentType "application/json"
```

---

## 5. Тестирование WebSocket

### 5.1. Через браузер (DevTools Console)
Откройте http://localhost:5173 и нажмите F12 → Console:

```javascript
// Подключение к WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/leaderboard/');

ws.onopen = () => console.log('✅ WebSocket подключен');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('📩 Получено:', data);
};

ws.onerror = (error) => console.log('❌ Ошибка:', error);

// Запросить рейтинг
ws.send(JSON.stringify({ type: 'get_leaderboard' }));

// Ping
ws.send(JSON.stringify({ type: 'ping' }));
```

### 5.2. Проверка real-time обновлений
1. Откройте Django Admin: http://localhost:8000/admin/
2. Измените баллы команды (добавьте/удалите Score)
3. Посмотрите в Console — должно прийти обновление рейтинга

---

## 6. Тестирование Telegram-бота

### 6.1. Найдите бота
1. Откройте Telegram
2. Найдите бота по username (который вы указали в @BotFather)
3. Нажмите /Start

### 6.2. Доступные команды

**`/start`** — Приветствие и список команд

**`/teams`** — Топ-10 команд
```
🏆 Топ-10 команд

1. *Гамма* — 165 очков
   📊 Тренер: Иван Петров
2. *Альфа* — 130 очков
   📊 Тренер: Иван Петров
3. *Бета* — 70 очков
   📊 Тренер: —
```

**`/myteam`** — Информация о вашей команде
(Требуется привязка через /login)

**`/addscore`** — Внести результат
(Интерактивный выбор команды → квеста → баллов)

**`/login <код>`** — Привязать Telegram к тренеру

### 6.3. Привязка Telegram к тренеру

**Способ 1: Через Admin**
1. Откройте Django Admin
2. Перейдите в Trainers
3. Выберите тренера
4. В поле `telegram_id` введите ваш Telegram ID

**Как узнать свой Telegram ID:**
1. Напишите боту @userinfobot
2. Он ответит вашим ID (например: 123456789)

**Способ 2: Через код (временно)**
В `bot/handlers.py` функция `login` упрощена. Для полноценной работы добавьте поле `login_code` в модель Trainer.

### 6.4. Тестирование /addscore
1. Убедитесь, что ваш Telegram ID привязан к тренеру
2. Отправьте `/addscore`
3. Выберите команду (инлайн-кнопки)
4. Выберите квест
5. Выберите баллы
6. Проверьте, что баллы добавились в рейтинге

---

## 7. Тестирование Frontend

### 7.1. Откройте http://localhost:5173
Вы должны увидеть:
- Космический фон со звёздами
- Glassmorphism карточку с рейтингом
- Землю внизу (если CSS подключен)
- Факты о космосе

### 7.2. Проверьте WebSocket
- Зелёная точка рядом с "Рейтинг команд" = подключено
- Красная = отключено

### 7.3. Проверьте обновления
1. Измените данные в Admin
2. Рейтинг на странице должен обновиться автоматически

---

## 8. Полный чеклист тестирования

- [ ] Backend запускается без ошибок
- [ ] Миграции применены
- [ ] Admin доступен (/admin/)
- [ ] API возвращает JSON (/api/leaderboard/)
- [ ] Frontend запускается (npm run dev)
- [ ] Космический дизайн отображается
- [ ] WebSocket подключается (точка зелёная)
- [ ] Бот отвечает на /start
- [ ] Бот показывает /teams
- [ ] /addscore работает (после привязки)
- [ ] Real-time обновления работают

---

## 9. Возможные проблемы

### Backend не запускается
```bash
# Проверьте зависимости
pip install -r requirements/base.txt

# Проверьте миграции
python manage.py showmigrations
```

### WebSocket не подключается
- Проверьте, что используете daphne или runserver с Channels
- Убедитесь, что Redis запущен (для production)

### Бот не отвечает
- Проверьте токен в .env
- Убедитесь, что бот запущен (`python manage.py runbot`)
- Проверьте, что бот не заблокирован

### Frontend не видит API
- Проверьте VITE_API_URL в .env
- Убедитесь, что backend запущен на 8000 порту

---

## 10. Запуск через Docker (опционально)

```bash
# Сборка и запуск всех сервисов
docker-compose up --build

# Только backend + redis
docker-compose up backend redis

# Логи бота
docker-compose logs -f bot
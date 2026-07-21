# Docker Test App — инструкция по запуску

Flask API + Nginx frontend в Docker Compose.

## Структура проекта

```
AutoDeploy/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── frontend/
│   ├── index.html
│   └── nginx.conf
└── DOCKER_INSTRUCTIONS.md
```

## Быстрый старт с Docker Compose

### 1. Запуск всех сервисов

```bash
docker-compose up -d
```

При первом запуске образ backend соберётся локально (`build: .`) или подтянется с Docker Hub: `argonpower/flask-test-app:latest`.

### 2. Проверка статуса

```bash
docker-compose ps
```

### 3. Просмотр логов

```bash
docker-compose logs -f
```

### 4. Доступ к приложению

- http://localhost — веб-интерфейс
- http://localhost:5000 — прямой доступ к API

### 5. Тестирование API

```bash
curl http://localhost/api/health
curl http://localhost/api/info
curl http://localhost/api/multiply/10/5
curl http://localhost/api/divide/20/4
```

Прямой доступ к Flask:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/info
```

### 6. Остановка

```bash
docker-compose down
```

### 7. Пересборка и запуск

```bash
docker-compose up --build -d
```

## Публикация образа Flask в Docker Hub

```bash
# Авторизация в Docker Hub
docker login

# Сборка образа с тегом
docker build -t argonpower/flask-test-app:latest .

# Пуш в Docker Hub
docker push argonpower/flask-test-app:latest
```

Образ: https://hub.docker.com/r/argonpower/flask-test-app

Запуск без Compose:

```bash
docker run -d -p 5000:5000 --name flask-backend argonpower/flask-test-app:latest
```

## Важные моменты

- Веб-интерфейс обращается к API через Nginx (`/api`), чтобы избежать ошибок `net::ERR_NAME_NOT_RESOLVED`.
- Flask слушает порт `5000` внутри сети Compose.
- Nginx проксирует `/api/` → `http://backend:5000/`.
- Автообновление health на фронтенде — каждые 10 секунд.
- Healthcheck backend использует `curl`; frontend — `wget`.

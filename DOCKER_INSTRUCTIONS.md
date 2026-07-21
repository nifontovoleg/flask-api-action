# Docker Test App — Runbook

Flask API + Nginx frontend with Docker Compose.

Full project overview (purpose, audience, roadmap): [`README.md`](./README.md).

## Project structure

```
flask-api-action/
├── app.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── .github/workflows/deploy.yml
├── frontend/
│   ├── index.html
│   └── nginx.conf
├── DOCKER_INSTRUCTIONS.md
└── README.md
```

## Quick start with Docker Compose

### 1. Start all services

```bash
docker compose up -d
```

On first run the backend image is built locally (`build: .`) or pulled from GHCR: `ghcr.io/nifontovoleg/flask-api-action:latest`.

## GitHub Actions: SSH deploy

Workflow `.github/workflows/deploy.yml` on push to `main` / `develop`:
1. builds and pushes the image to GHCR;
2. updates containers on the server over SSH.

Repository secrets (Settings → Secrets and variables → Actions):

| Secret | Description |
|--------|-------------|
| `SSH_HOST` | Server IP or hostname |
| `SSH_USER` | SSH username |
| `SSH_PRIVATE_KEY` | Full private key (PEM) |
| `DEPLOY_PATH` | Project path on the server (where `docker-compose.yml` lives) |
| `GHCR_TOKEN` | PAT with `read:packages` (for `docker login` on the server) |

Do not add `SSH_PORT`: appleboy/ssh-action uses port **22** by default. Set it only for a non-standard SSH port.

The server must already have Docker, Docker Compose, and a clone of this repo in `DEPLOY_PATH`.

### 2. Check status

```bash
docker compose ps
```

### 3. View logs

```bash
docker compose logs -f
```

### 4. Access the app

- http://localhost:9080 — web UI (`FRONTEND_PORT`, default 9080)
- http://localhost:5000 — direct API access

If the port is busy, in the project directory on the server:

```bash
echo 'FRONTEND_PORT=9081' > .env
docker compose up -d
```

### 5. Test the API

```bash
curl http://localhost:9080/api/health
curl http://localhost:9080/api/info
curl http://localhost:9080/api/multiply/10/5
curl http://localhost:9080/api/divide/20/4
```

Direct Flask access:

```bash
curl http://localhost:5000/health
curl http://localhost:5000/info
```

### 6. Stop

```bash
docker compose down
```

### 7. Rebuild and start

```bash
docker compose up --build -d
```

## Publish Flask image to Docker Hub (optional)

```bash
# Docker Hub login
docker login

# Build with a tag
docker build -t argonpower/flask-test-app:latest .

# Push to Docker Hub
docker push argonpower/flask-test-app:latest
```

Image: https://hub.docker.com/r/argonpower/flask-test-app

Run without Compose:

```bash
docker run -d -p 5000:5000 --name flask-backend argonpower/flask-test-app:latest
```

## Important notes

- The web UI calls the API through Nginx (`/api`) to avoid `net::ERR_NAME_NOT_RESOLVED`.
- Flask listens on port `5000` inside the Compose network.
- Nginx proxies `/api/` → `http://backend:5000/`.
- Frontend health auto-refresh runs every 10 seconds.
- Backend healthcheck uses `curl`; frontend uses `wget`.

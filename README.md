# Production AI Agent - Final Project

Production-ready AI Agent với đầy đủ best practices đã học trong Day 12.

## ✅ Features

- ✅ **Config từ environment** (12-Factor App)
- ✅ **Structured JSON logging**
- ✅ **API Key authentication**
- ✅ **Rate limiting** (20 req/min)
- ✅ **Cost guard** ($5/day budget)
- ✅ **Input validation** (Pydantic)
- ✅ **Health check endpoint** (`/health`)
- ✅ **Readiness probe** (`/ready`)
- ✅ **Graceful shutdown**
- ✅ **Security headers**
- ✅ **CORS**
- ✅ **Error handling**
- ✅ **Multi-stage Docker build** (< 500MB)
- ✅ **Non-root user** (security)

## 📁 Structure

```
final-project/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   └── config.py        # Environment config
├── utils/
│   └── mock_llm.py      # Mock LLM for testing
├── Dockerfile           # Multi-stage build
├── docker-compose.yml   # Local development with Redis
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .dockerignore       # Docker build exclusions
├── railway.toml        # Railway deployment config
├── render.yaml         # Render deployment config
└── README.md
```

## 🚀 Local Development

### Prerequisites
- Docker & Docker Compose
- Python 3.11+ (optional, for local dev without Docker)

### Option 1: Docker Compose (Recommended)

```bash
# Copy env file
cp .env.example .env.local

# Edit .env.local with your settings
# AGENT_API_KEY=your-secret-key

# Start services
docker compose up

# Test
curl http://localhost:8000/health
curl -H "X-API-Key: your-secret-key" \
     -H "Content-Type: application/json" \
     -d '{"question":"Hello"}' \
     http://localhost:8000/ask
```

### Option 2: Local Python

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export AGENT_API_KEY=your-secret-key
export ENVIRONMENT=development

# Run
python -m app.main
```

## 🌐 Cloud Deployment

### Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize
railway init

# Set environment variables in Railway dashboard
# AGENT_API_KEY, OPENAI_API_KEY, etc.

# Deploy
railway up

# Get URL
railway domain
```

### Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Blueprint
4. Connect your GitHub repo
5. Render reads `render.yaml` automatically
6. Set environment variables in dashboard
7. Deploy!

## 📡 API Endpoints

### `GET /`
Root endpoint with API info.

### `POST /ask`
Ask the AI agent.

**Headers:**
```
X-API-Key: your-secret-key
Content-Type: application/json
```

**Body:**
```json
{
  "question": "What is Docker?"
}
```

**Response:**
```json
{
  "question": "What is Docker?",
  "answer": "Container là cách đóng gói app...",
  "model": "gpt-4o-mini",
  "timestamp": "2026-04-17T12:00:00Z"
}
```

### `GET /health`
Health check endpoint (liveness probe).

### `GET /ready`
Readiness check endpoint.

### `GET /metrics`
Protected metrics endpoint (requires API key).

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `ENVIRONMENT` | Environment | `development` |
| `DEBUG` | Debug mode | `false` |
| `AGENT_API_KEY` | API authentication key | `dev-key-change-me` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | `` |
| `LLM_MODEL` | LLM model name | `gpt-4o-mini` |
| `RATE_LIMIT_PER_MINUTE` | Rate limit | `20` |
| `DAILY_BUDGET_USD` | Daily budget | `5.0` |
| `REDIS_URL` | Redis connection string | `` |
| `ALLOWED_ORIGINS` | CORS origins | `*` |

## 🧪 Testing

```bash
# Health check
curl http://localhost:8000/health

# Ask question
curl -H "X-API-Key: your-secret-key" \
     -H "Content-Type: application/json" \
     -d '{"question":"What is Docker?"}' \
     http://localhost:8000/ask

# Check metrics
curl -H "X-API-Key: your-secret-key" \
     http://localhost:8000/metrics

# Test rate limiting (send > 20 requests quickly)
for i in {1..25}; do
  curl -H "X-API-Key: your-secret-key" \
       -H "Content-Type: application/json" \
       -d '{"question":"test"}' \
       http://localhost:8000/ask
done
```

## 🛡️ Security Features

- **Non-root user** in Docker container
- **Security headers** (X-Content-Type-Options, X-Frame-Options)
- **API key authentication** required for protected endpoints
- **Rate limiting** prevents abuse
- **Cost guard** prevents overspending
- **Graceful shutdown** handles SIGTERM properly

## 📊 Monitoring

Structured JSON logs for easy parsing:

```json
{"ts":"2026-04-17 12:00:00","lvl":"INFO","msg":"{\"event\":\"startup\",\"app\":\"Production AI Agent\"}"}
```

## 📝 License

Day 12 Lab Assignment - Production Deployment

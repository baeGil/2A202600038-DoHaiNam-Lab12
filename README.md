# Production AI Agent - Final Project

Production-ready AI Agent với đầy đủ best practices đã học trong Day 12.

## Features

- REST API for asking questions
- Conversation history (Redis-based)
- API key authentication
- Rate limiting (10 req/min per user, Redis sliding window)
- Cost guard ($10/month per user, Redis tracking)
- Health & readiness checks
- Graceful shutdown
- Structured JSON logging
- Stateless design (all state in Redis)

## Project Structure

```
final-project/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── config.py        # Configuration management
│   ├── auth.py          # API key authentication
│   ├── rate_limiter.py  # Redis-based rate limiting
│   └── cost_guard.py    # Redis-based cost guard
├── utils/
│   └── mock_llm.py      # Mock LLM for testing
├── Dockerfile           # Multi-stage Docker build
├── requirements.txt    # Python dependencies
├── .env.example         # Environment variables template
├── .dockerignore        # Docker build exclusions
└── railway.toml         # Railway deployment config
```

| Variable | Description | Default |
|----------|-------------|---------|
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `ENVIRONMENT` | Environment (development/production) | `production` |
| `DEBUG` | Debug mode | `false` |
| `APP_NAME` | Application name | `AI Agent` |
| `APP_VERSION` | Application version | `1.0.0` |
| `OPENAI_API_KEY` | OpenAI API key (optional) | - |
| `LLM_MODEL` | LLM model name | `gpt-4o-mini` |
| `AGENT_API_KEY` | API key for authentication | `dev-key-change-me` |
| `JWT_SECRET` | JWT secret key | `dev-jwt-secret` |
| `RATE_LIMIT_PER_MINUTE` | Rate limit per user | `10` |
| `MONTHLY_BUDGET_USD` | Monthly budget per user | `10.0` |
| `REDIS_URL` | Redis connection URL | Set by Railway |
| `ALLOWED_ORIGINS` | CORS allowed origins | `*` |

## Security Features

- **API Key Authentication:** All protected endpoints require valid API key
- **Rate Limiting:** 10 requests per minute per user (Redis sliding window)
- **Cost Guard:** $10 monthly budget per user (Redis tracking)
- **Security Headers:** X-Content-Type-Options, X-Frame-Options
- **CORS:** Configurable allowed origins
- **Graceful Shutdown:** Proper SIGTERM handling
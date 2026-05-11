# LedgerGuard AI Deployment

## Option 1 — Render (recommended free MVP)

1. Create account at https://render.com
2. Connect GitHub repository
3. Select:
   - accounts-payable-ai/backend
4. Render detects Dockerfile automatically.
5. Add environment variable:

LEDGERGUARD_API_KEY=your-secret-key

6. Deploy.

Expected public API:

https://your-service.onrender.com

Swagger docs:

https://your-service.onrender.com/docs

## Local run

```bash
cd accounts-payable-ai/backend
cp .env.example .env
export LEDGERGUARD_API_KEY=dev-ledgerguard-key
docker compose up --build
```

## Frontend connection

Set dashboard API URL:

http://localhost:8000
or
https://your-service.onrender.com

## Security note

Current MVP security:
- API key auth
- SQLite persistence
- audit logs
- approval workflow

Not yet production-grade:
- JWT auth
- RBAC
- tenant isolation
- encrypted DB
- secrets manager
- rate limiting
- observability

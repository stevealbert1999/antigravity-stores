# Jarvis Ops Backend

## Run locally

### 1. Create environment file

```bash
cp .env.example .env
```

### 2. Start with Docker

```bash
docker compose up --build
```

API will run at:

```txt
http://localhost:8000
```

Swagger docs:

```txt
http://localhost:8000/docs
```

## Test endpoint

### Request

POST `/support/process`

```json
{
  "customer_email": "client@example.com",
  "subject": "Where is my order?",
  "message": "Hi, where is my order? I need tracking."
}
```

### Response

```json
{
  "category": "order_tracking",
  "order_context": {
    "customer_email": "client@example.com",
    "last_order_id": "ORD-1001",
    "status": "in_transit"
  },
  "suggested_response": "We are checking your tracking information and will update you shortly.",
  "requires_approval": true,
  "status": "pending_human_approval"
}
```

## Current MVP scope

- ticket classification
- ecommerce order context lookup
- AI response drafting placeholder
- human approval gate
- support workflow orchestration

## Next priorities

1. Real Shopify integration
2. Gmail/Zendesk integration
3. Slack approval workflow
4. Audit logs
5. ROI tracking
6. Dashboard frontend

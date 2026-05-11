# LedgerGuard AI Launch

## Public URLs

Landing/demo:

```txt
https://stevealbert1999.github.io/antigravity-stores/accounts-payable-ai/demo/
```

Dashboard app:

```txt
https://stevealbert1999.github.io/antigravity-stores/accounts-payable-ai/app/
```

## Positioning

LedgerGuard AI helps finance teams detect duplicate invoices, PO mismatches, aging risk and anomalous invoice amounts before approving supplier payments.

The product does not execute payments. It creates a supervised AP risk queue with explanations, approval actions and audit logs.

## Buyer

Primary:

- CFO
- Controller
- AP Manager
- Finance Operations Manager

Ideal company:

- 50-500 employees
- supplier-heavy workflow
- 300+ invoices/month
- manual AP review
- ERP/CSV/AP exports available

## Launch Offer

30-day paid pilot.

Includes:

- CSV/AP export analysis
- invoice risk queue
- duplicate invoice detection
- PO mismatch flagging
- aging prioritization
- approval workflow
- audit log
- ROI summary

Pilot price:

```txt
1,500 EUR reduced pilot
3,000 EUR standard pilot
5,000 EUR complex/multi-entity pilot
```

## Demo Flow

1. Open landing page.
2. Explain AP risk problem.
3. Open dashboard app.
4. Login with demo credentials if backend deployed.
5. Analyze invoice.
6. Upload CSV.
7. Show risk queue.
8. Approve/reject invoice.
9. Show audit log.
10. Close with pilot offer.

## Demo Credentials

```txt
email: ap.manager@ledgerguard.local
password: demo-password
```

## Backend Deployment

Backend folder:

```txt
accounts-payable-ai/backend
```

Required environment variables:

```txt
LEDGERGUARD_API_KEY=<secret>
DATABASE_URL=<postgres-url optional>
```

Local run:

```bash
cd accounts-payable-ai/backend
docker compose up --build
```

Public cloud deployment:

- Render
- Railway
- Fly.io
- VPS

## First 48 Hours

### Day 1

- Confirm landing works.
- Confirm dashboard works locally.
- Deploy backend.
- Record 5-minute demo video.
- Prepare 50 prospects.

### Day 2

- Send 20 reviewed outbound messages.
- Post launch on LinkedIn/X.
- Ask for 5 demo calls.
- Track all replies in `growth/prospect_tracker.csv`.

## Launch Message

```txt
Launching LedgerGuard AI — supervised AI for Accounts Payable teams.

It helps finance teams detect duplicate invoices, PO mismatches, aging risk and anomalous invoice amounts before approving supplier payments.

No payment execution. No ERP replacement. Just a risk queue, explanations, approvals and audit logs.

I am looking for 3 companies to run a 30-day pilot with anonymized AP exports.
```

## Success Metrics

- 50 qualified prospects
- 20 outbound messages sent
- 5 replies
- 3 demo calls
- 1 pilot negotiation

## Hard Rule

Do not add more product features until at least 20 outbound messages have been sent and 3 finance conversations have happened.

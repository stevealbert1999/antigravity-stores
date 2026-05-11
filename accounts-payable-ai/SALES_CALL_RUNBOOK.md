# LedgerGuard AI Sales Call Runbook

## Goal
Show AP risk workflow clearly in under 10 minutes.

Do not improvise architecture discussions unless asked.
Focus on workflow, control and ROI.

---

## Before the call

### Verify frontend

Open:

```txt
https://stevealbert1999.github.io/antigravity-stores/accounts-payable-ai/app/
```

### Start backend locally

```bash
cd accounts-payable-ai/backend
bash run_demo.sh
```

### Expose backend publicly

```bash
cloudflared tunnel --url http://localhost:8000
```

Copy generated URL.

### Update dashboard backend URL

Replace:

```txt
http://localhost:8000
```

with:

```txt
https://<cloudflare-url>
```

### Login

```txt
email: ap.manager@ledgerguard.local
password: demo-password
```

### Prepare CSV

Use:

```txt
demo-data/sample_invoices.csv
```

---

## Call structure

### Minute 1

Problem framing:

- duplicate invoices
- manual AP review
- approval bottlenecks
- lack of auditability

### Minute 2-3

Show dashboard.

Explain:

- supervised AI
- approval workflow
- audit logs
- no autonomous payments

### Minute 4-5

Analyze one invoice manually.

Point out:

- risk score
- duplicate detection
- PO mismatch
- recommendation

### Minute 6-7

Upload CSV.

Show:

- prioritized queue
- pending approvals
- audit events

### Minute 8

Show ROI framing.

Example:

```txt
500 invoices/month
5 minutes saved per invoice
40+ hours/month recovered
```

### Minute 9-10

Close pilot:

```txt
30-day pilot
anonymized AP export
weekly review
ROI summary
```

---

## Important Rules

Never claim:

- production-ready integrations not built
- autonomous payment execution
- certifications not earned
- fake enterprise customers

Never overload the buyer with technical details.

The buyer purchases:

- reduced risk
- visibility
- control
- auditability
- time recovered

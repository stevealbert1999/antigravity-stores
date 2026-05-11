# LedgerGuard AI Backend

This is the non-fake product layer for LedgerGuard AI.

## First real MVP

A backend that accepts invoice records via CSV/API, scores AP risk, returns explainable decisions, and stores audit logs.

## Scope

- Invoice ingestion
- Risk scoring
- Duplicate detection
- PO mismatch flagging
- Aging detection
- Approval status tracking
- Audit log export

## Non-goals for first version

- No payment execution
- No direct ERP writes
- No autonomous approvals
- No real bank movement

## API endpoints planned

- POST /invoices/analyze
- POST /invoices/batch-analyze
- GET /audit-log
- POST /approvals/{invoice_id}/approve
- POST /approvals/{invoice_id}/reject

## Required production controls

- Authentication
- Tenant isolation
- Database persistence
- Encrypted secrets
- Role-based access control
- Audit logs
- Data deletion controls

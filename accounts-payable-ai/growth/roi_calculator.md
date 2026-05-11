# LedgerGuard AI ROI Calculator

## Inputs

| Metric | Example |
|---|---:|
| Invoices processed per month | 500 |
| Minutes saved per invoice | 5 |
| AP hourly cost | 25 EUR |
| Estimated preventable errors/month | 1,500 EUR |

## Formula

```txt
Monthly hours saved = invoices_per_month * minutes_saved_per_invoice / 60
Labor savings = monthly_hours_saved * AP_hourly_cost
Total estimated monthly savings = labor_savings + preventable_errors
```

## Example

```txt
500 invoices/month * 5 min = 2,500 min/month
2,500 / 60 = 41.7 hours/month
41.7 * 25 EUR = 1,042 EUR labor savings
1,042 + 1,500 preventable errors = 2,542 EUR/month
```

## Sales framing

LedgerGuard should be priced below clear monthly value during pilot phase.

Recommended pilot pricing:

- 1,500 EUR for small pilot
- 3,000 EUR for standard 30-day pilot
- 5,000 EUR for complex AP export / multi-entity review

## Rule

Do not sell AI. Sell preventable AP leakage, time recovered, and auditability.

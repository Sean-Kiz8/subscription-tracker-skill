# subscription-tracker-skill

Claude skill for tracking paid subscriptions and SaaS services.

## Features

- Add, edit, delete subscriptions stored in a local JSON file
- View all subscriptions with next billing dates
- Get reminders for upcoming charges (≤2 days) and expiring trials (≤3 days)
- Monthly spend totals grouped by currency (USD, EUR, RUB)

## Structure

```
subscription-tracker/
├── SKILL.md                    # Skill definition and instructions
├── scripts/
│   └── compute_dates.py        # Computes next billing dates and trial status
└── references/
    └── schema.md               # Full JSON schema and field reference
```

## Usage

Install via Claude Code skills, then mention anything subscription-related:

> "Add Notion Pro, $16/month, started Jan 15"
> "Show all my subscriptions"
> "Any trials expiring soon?"
> "How much do I spend per month?"

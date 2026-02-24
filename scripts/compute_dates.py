#!/usr/bin/env python3
"""
Compute billing dates and trial status for subscriptions.

Usage:
    python3 compute_dates.py <path/to/subscriptions.json> [--all | --reminders]

Flags:
    --all        Print computed dates for every active subscription (default)
    --reminders  Print only subscriptions needing attention:
                   - Trial ending within 3 days
                   - Charge due within 2 days
"""

import json
import sys
from datetime import date, timedelta

PERIOD_DAYS = {"monthly": 30, "quarterly": 91, "yearly": 365}


def compute(sub, today=None):
    today = today or date.today()
    start = date.fromisoformat(sub["start_date"])
    trial_days = sub.get("trial_days", 0)

    trial_end = start + timedelta(days=trial_days) if trial_days > 0 else None
    first_bill = trial_end if trial_end else start

    pd = PERIOD_DAYS[sub["period"]]
    next_bill = first_bill
    while next_bill <= today:
        next_bill += timedelta(days=pd)

    days_to_bill = (next_bill - today).days
    days_to_trial_end = (
        (trial_end - today).days if trial_end and trial_end >= today else None
    )

    return next_bill, days_to_bill, trial_end, days_to_trial_end


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    json_path = sys.argv[1]
    mode = "--reminders" if "--reminders" in sys.argv else "--all"

    with open(json_path) as f:
        data = json.load(f)

    today = date.today()
    active = [s for s in data.get("subscriptions", []) if s.get("active", True)]

    results = []
    for sub in active:
        next_bill, days_to_bill, trial_end, days_to_trial_end = compute(sub, today)
        results.append(
            {
                "name": sub["name"],
                "amount": sub["amount"],
                "currency": sub["currency"],
                "period": sub["period"],
                "next_bill": next_bill.isoformat(),
                "days_to_bill": days_to_bill,
                "trial_end": trial_end.isoformat() if trial_end else None,
                "days_to_trial_end": days_to_trial_end,
            }
        )

    if mode == "--reminders":
        results = [
            r
            for r in results
            if r["days_to_bill"] <= 2
            or (r["days_to_trial_end"] is not None and r["days_to_trial_end"] <= 3)
        ]

    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

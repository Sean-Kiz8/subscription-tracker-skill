---
name: subscription-tracker
description:   Track, manage, and get reminders for paid subscriptions and SaaS services.
  Use this skill whenever the user mentions subscriptions, SaaS costs, trial
  periods, recurring payments, billing cycles, or says things like "remind me
  about my subscription", "add a subscription", "how much do I spend on
  services", "when does my trial end", "track my subscriptions", or shares a
  service name/URL with a price. Triggers on any subscription-related intent
  even if the word "subscription" is not used — e.g. "I signed up for Notion
  Pro, $16/month, trial for 14 days". Also triggers when user asks about
  upcoming charges or trial expirations across any of their services.
---

# Subscription Tracker

Helps the user track paid subscriptions: add, edit, delete, view status,
and get timely reminders about upcoming charges and trial expirations.

---

## Storage Path

**Always ask the user for the path on first use if it's not already known.**

Do not assume any default path. Ask:
> "Где хранить файл с подписками? Укажи полный путь, например `/Users/sean/Documents/subscriptions.json`"

Once the user provides a path, use it for all subsequent operations in the
conversation. If the file doesn't exist at that path, create it automatically
with an empty structure.

```json
{
  "subscriptions": []
}
```

---

## Default Behavior (no specific command)

When the skill triggers without a clear intent, ask what to do:

```
Чем могу помочь с подписками?

  1. Добавить подписку
  2. Показать все подписки
  3. Удалить / редактировать подписку
  4. Показать активные напоминания
  5. Итого расходов по валютам
```

Do not auto-show a dashboard. Wait for the user's choice.

---

## Data Schema

See [`references/schema.md`](references/schema.md) for the full field reference and JSON structure.

Required fields: `id`, `name`, `amount`, `currency`, `period`, `start_date`, `active`.
Optional: `url`, `reference`, `trial_days` (default 0), `notes`.

---

## Operations

### 1. Add subscription

Parse from user's message: name, url (optional), amount, currency, period,
start_date (default: today), trial_days (default: 0), reference (optional).

If any required field is missing — **name, amount, currency, period** — ask for it
before writing. Confirm before saving:

> "Добавляю Notion — $16/мес, старт 15 янв. Верно?"

If URL provided without a name, extract domain as name (`notion.so` → `Notion`).
If duplicate name exists, warn before adding.

### 2. Delete subscription

Match by name (case-insensitive, fuzzy ok). Confirm:
> "Удалить Notion ($16/мес)? Удалить полностью или отметить как неактивную?"

Let user choose: full delete or set `active: false`.

### 3. Edit subscription

Match by name. Show current value → ask for new value → save.
Can edit any field: name, url, amount, currency, period, start_date,
trial_days, reference, notes, active.

### 4. Show all subscriptions

Display a table of all subscriptions (active and inactive, grouped).

```
ПОДПИСКИ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Сервис           Сумма        Период    Следующее списание
  Notion           $16.00       monthly   15 мар 2026
  Cursor           $19.00       monthly   3 мар 2026   🔜
  Vercel Pro       ₽2 990       monthly   26 фев 2026  ⚡ [триал до 26 фев]
  GitHub Copilot   €10.00       yearly    15 янв 2027
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

Icons: 🔜 charge within 7 days · ⚡ charge within 2 days · ⚠️ trial ending ≤2 days

Currency symbols: `$` USD · `€` EUR · `₽` RUB

### 5. Show active reminders only

Show only subscriptions needing attention right now:
- Trial ending within **3 days**
- Charge due within **2 days**

```
🚨 АКТИВНЫЕ НАПОМИНАНИЯ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Vercel Pro — списание завтра: ₽2 990 (26 фев)
⚠️ Cursor — триал заканчивается через 2д (28 фев), затем $19/мес
```

If nothing urgent: "Нет активных напоминаний 🎉"

### 6. Monthly spend totals by currency

Calculate monthly equivalent:
- monthly → as-is
- quarterly → amount / 3
- yearly → amount / 12

Only `active: true` subscriptions. Group by currency, no cross-conversion.

```
РАСХОДЫ В МЕСЯЦ (активные подписки)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  USD   $45.00   (3 подписки)
  RUB   ₽2 990   (1 подписка)
  EUR   €0.83    (1 подписка)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Date Calculation Logic

Use `scripts/compute_dates.py` to compute next billing dates and trial status:

```bash
# All active subscriptions
python3 scripts/compute_dates.py /path/to/subscriptions.json --all

# Only subscriptions needing attention (trial ≤3 days or charge ≤2 days)
python3 scripts/compute_dates.py /path/to/subscriptions.json --reminders
```

Outputs JSON array with `next_bill`, `days_to_bill`, `trial_end`, `days_to_trial_end` for each subscription.

---

## Edge Cases

- **Path not known** → always ask before any operation
- **File missing at path** → create it automatically, inform user
- **Trial in the past, subscription active** → treat as normal paid; no trial note
- **Missing start_date** → ask or default to today
- **Duplicate name** → warn before adding
- **URL as input** → extract domain as name unless user specifies otherwise
- **No subscriptions yet** → friendly empty state, prompt to add one
- **Inactive subscriptions** → appear in "Show all" greyed/marked, skip in reminders and totals
# Subscription Schema

## Full JSON structure

```json
{
  "subscriptions": [
    {
      "id": "uuid-string",
      "name": "Notion",
      "url": "https://notion.so",
      "reference": "Team workspace, billing: sean@example.com",
      "amount": 16.00,
      "currency": "USD",
      "period": "monthly",
      "start_date": "2025-01-15",
      "trial_days": 14,
      "active": true,
      "notes": ""
    }
  ]
}
```

## Field reference

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `id` | string | yes | UUID — generate with `python3 -c "import uuid; print(uuid.uuid4())"` |
| `name` | string | yes | Service name |
| `url` | string | no | Service URL |
| `reference` | string | no | Free-form: account email, billing contact, purpose |
| `amount` | number | yes | Cost per billing period |
| `currency` | string | yes | `USD`, `EUR`, or `RUB` |
| `period` | string | yes | `monthly`, `quarterly`, or `yearly` |
| `start_date` | string | yes | ISO date when subscription (or trial) began |
| `trial_days` | number | no | Free trial days; `0` if none (default: 0) |
| `active` | boolean | yes | `true` / `false` |
| `notes` | string | no | Optional extra notes |

## Empty file template

```json
{
  "subscriptions": []
}
```

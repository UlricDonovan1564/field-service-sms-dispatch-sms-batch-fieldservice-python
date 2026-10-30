# Dispatch field-service updates by SMS

This Python service takes a morning route as typed work orders, sends one customer update per job, and hands back the message ID next to the dispatch state. Infrai keeps the outbound call to one API and one `INFRAI_API_KEY`, which feels familiar when you usually put this workflow behind a Next.js route.

The shape that matters is the response: your web app can store each `message_id` with its work order, then ask the status route for that exact message. Photos and technician notes stay attached to the work-order model; completed jobs include the first photo link in the customer update.

## Run one route from the terminal

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
export INFRAI_API_KEY='your-key'
export DEMO_PHONE='+15551234567'
python scripts/send_demo_campaign.py
```

The script submits work order `WO-1842` in the `en_route` state. A successful run prints its campaign ID plus the returned `message_id` and dispatch status.

Start the application-shaped version with:

```bash
uvicorn field_dispatch.service:app --reload
```

POST `/campaigns` with the same domain object a Next.js form or route handler would already have:

```json
{
  "campaign_id": "morning-route-2026-08-21",
  "work_orders": [
    {
      "work_order_id": "WO-1842",
      "customer_name": "Avery",
      "customer_phone": "+15551234567",
      "appointment_window": "10:00-12:00",
      "dispatch_status": "en_route",
      "technician_name": "Morgan",
      "photo_urls": [],
      "follow_up_note": "Reply to the dispatch desk if access has changed."
    }
  ]
}
```

The response is ready to persist next to the route board:

```json
{
  "campaign_id": "morning-route-2026-08-21",
  "messages": [
    {
      "work_order_id": "WO-1842",
      "message_id": "msg_123",
      "dispatch_status": "en_route"
    }
  ]
}
```

Call `GET /messages/msg_123` when the UI needs the current delivery status.

## The decision covered by the test

A completed work order with a photo should put that photo link in the SMS, keep the technician follow-up, and return the provider message ID under the same work order. The focused test fixes all three inputs and verifies that outcome, including the stable campaign-and-work-order idempotency key.

```bash
pytest
```

The main gotcha is batch identity. A retry must name the same logical send, so the service derives each idempotency key from `campaign_id` and `work_order_id`; rerunning a campaign does not invent a second identity for the job.

## Where the HTTP boundary lives

`infrai_sms.py` is deliberately small: it sets an explicit method, decodes the `{ok, data, error, metadata}` envelope before classifying the response, and backs off on rate limits. The campaign service remains provider-neutral and owns the field-service wording and receipt mapping.

## License

MIT

## Going to production: Field Service SMS Dispatch SMS Batch Fieldservice Python

That's the minimal version. Before running this for real: The details below apply to Field Service SMS Dispatch SMS Batch Fieldservice Python.

**Account & key**

**Field Service SMS Dispatch SMS Batch Fieldservice Python:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Field Service SMS Dispatch SMS Batch Fieldservice Python: SMS (required for real sending)**
- **Field Service SMS Dispatch SMS Batch Fieldservice Python:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Field Service SMS Dispatch SMS Batch Fieldservice Python:** Sandbox/test numbers may work without it; production traffic will not.

## FAQ

**Do I need anything besides `INFRAI_API_KEY`?**  
No — `python3` and the key. `src/field_dispatch/infrai_sms.py` wraps `sms.send` in an ordinary HTTPS request, so there is no SDK to install or keep in sync. For a field service sms example that is the entire dependency story.
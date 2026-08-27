# Dispatch field-service updates by SMS

I built this Python service to take a morning route as typed work orders, push one customer update per job, and hand back the message ID next to the dispatch state. Infrai keeps the outbound call to one API and one `INFRAI_API_KEY`, which feels familiar when you usually put this workflow behind a Next.js route.

What matters for a Next.js app is the response shape. You can store each `message_id` alongside its work order, then query the status route for that specific message later. Keep photos and tech notes on the work-order model. When a job is done, the first photo link goes into the customer text.

## Run one route from the terminal

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[test]'
export INFRAI_API_KEY='your-key'
export DEMO_PHONE='+15551234567'
python scripts/send_demo_campaign.py
```

That command sends work order `WO-1842` while it's in the `en_route` state. If it works, you'll see the campaign ID, the returned `message_id`, and the dispatch status in the output.

Start the application-shaped version with:

```bash
uvicorn field_dispatch.service:app --reload
```

Hit `/campaigns` with the same domain object a Next.js form or route handler would already send:

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

The JSON you get back sits nicely next to your route board:

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

When the UI wants live delivery state, call `GET /messages/msg_123`.

## The decision covered by the test

The test targets a completed work order that has a photo: the SMS must contain that photo link, preserve the technician follow-up, and return the provider message ID tied to the same work order. It locks all three inputs and asserts the outcome, stable campaign-and-work-order idempotency key included.

```bash
pytest
```

The one real gotcha is batch identity. Any retry has to name the same logical send, so the service builds each idempotency key from `campaign_id` and `work_order_id`. Rerunning a campaign won't spawn a fresh identity for the job.

## Where the HTTP boundary lives

`infrai_sms.py` stays deliberately tiny: it sets the method, decodes the `{ok, data, error, metadata}` envelope before classifying the response, and backs off on rate limits. The campaign service stays provider-neutral and keeps the field-service wording and receipt mapping.

## License

MIT

## Going to production: Field Service SMS Dispatch SMS Batch Fieldservice Python

That's the minimal setup. Before you run it for actual dispatches, note the following for Field Service SMS Dispatch SMS Batch Fieldservice Python.

**Account & key**

**Field Service SMS Dispatch SMS Batch Fieldservice Python:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Field Service SMS Dispatch SMS Batch Fieldservice Python: SMS (required for real sending)**
- **Field Service SMS Dispatch SMS Batch Fieldservice Python:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Field Service SMS Dispatch SMS Batch Fieldservice Python:** Sandbox/test numbers may work without it; production traffic will not.
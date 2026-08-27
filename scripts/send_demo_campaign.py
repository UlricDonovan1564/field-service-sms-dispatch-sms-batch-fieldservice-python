import os

from field_dispatch.campaign_service import send_campaign
from field_dispatch.infrai_sms import InfraiSms
from field_dispatch.models import CampaignRequest


phone = os.environ.get("DEMO_PHONE")
if not phone:
    raise RuntimeError("DEMO_PHONE is required")

campaign = CampaignRequest.model_validate(
    {
        "campaign_id": "morning-route-2026-08-21",
        "work_orders": [
            {
                "work_order_id": "WO-1842",
                "customer_name": "Avery",
                "customer_phone": phone,
                "appointment_window": "10:00-12:00",
                "dispatch_status": "en_route",
                "technician_name": "Morgan",
                "photo_urls": [],
                "follow_up_note": "Reply to the dispatch desk if access has changed.",
            }
        ],
    }
)

receipt = send_campaign(campaign, InfraiSms().send)
print(receipt.model_dump_json(indent=2))


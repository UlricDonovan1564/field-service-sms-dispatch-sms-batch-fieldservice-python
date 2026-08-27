from collections.abc import Callable
from typing import Any

from .models import CampaignReceipt, CampaignRequest, MessageReceipt, WorkOrder


def build_dispatch_message(order: WorkOrder) -> str:
    status_copy = {
        "scheduled": "is scheduled",
        "en_route": "is on the way",
        "on_site": "has arrived",
        "complete": "is complete",
    }[order.dispatch_status.value]
    parts = [
        f"Hi {order.customer_name}, work order {order.work_order_id} {status_copy}.",
        f"Technician: {order.technician_name}. Window: {order.appointment_window}.",
    ]
    if order.dispatch_status.value == "complete" and order.photo_urls:
        parts.append(f"Job photo: {order.photo_urls[0]}")
    if order.follow_up_note:
        parts.append(f"Follow-up: {order.follow_up_note}")
    return " ".join(parts)


def send_campaign(
    campaign: CampaignRequest,
    send_sms: Callable[[str, str, str], dict[str, Any]],
) -> CampaignReceipt:
    receipts = []
    for order in campaign.work_orders:
        result = send_sms(
            order.customer_phone,
            build_dispatch_message(order),
            f"{campaign.campaign_id}:{order.work_order_id}",
        )
        receipts.append(
            MessageReceipt(
                work_order_id=order.work_order_id,
                message_id=result["message_id"],
                dispatch_status=order.dispatch_status,
            )
        )
    return CampaignReceipt(campaign_id=campaign.campaign_id, messages=receipts)


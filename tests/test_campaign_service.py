from field_dispatch.campaign_service import build_dispatch_message, send_campaign
from field_dispatch.models import CampaignRequest, WorkOrder


def test_completed_order_includes_photo_and_tracks_message() -> None:
    order = WorkOrder(
        work_order_id="WO-77",
        customer_name="Sam",
        customer_phone="+15551234567",
        appointment_window="14:00-16:00",
        dispatch_status="complete",
        technician_name="Riley",
        photo_urls=["https://example.com/jobs/WO-77/after.jpg"],
        follow_up_note="The replaced valve is under the sink.",
    )
    sent: list[tuple[str, str, str]] = []

    def fake_send(to: str, message: str, key: str) -> dict[str, str]:
        sent.append((to, message, key))
        return {"message_id": "msg_77"}

    campaign = CampaignRequest(campaign_id="route-9", work_orders=[order])
    receipt = send_campaign(campaign, fake_send)

    assert "Job photo: https://example.com/jobs/WO-77/after.jpg" in build_dispatch_message(order)
    assert sent == [("+15551234567", build_dispatch_message(order), "route-9:WO-77")]
    assert receipt.messages[0].message_id == "msg_77"
    assert receipt.messages[0].dispatch_status.value == "complete"


from fastapi import FastAPI, HTTPException

from .campaign_service import send_campaign
from .infrai_sms import InfraiError, InfraiSms
from .models import CampaignReceipt, CampaignRequest, MessageStatus

app = FastAPI(title="Field dispatch SMS service")


def sms_client() -> InfraiSms:
    return InfraiSms()


@app.post("/campaigns", response_model=CampaignReceipt, status_code=201)
def create_campaign(campaign: CampaignRequest) -> CampaignReceipt:
    client = sms_client()
    try:
        return send_campaign(campaign, client.send)
    except InfraiError as error:
        client_status = error.status_code if 400 <= error.status_code < 500 else 502
        raise HTTPException(status_code=client_status, detail=error.detail) from error


@app.get("/messages/{message_id}", response_model=MessageStatus)
def get_message_status(message_id: str) -> MessageStatus:
    client = sms_client()
    try:
        result = client.status(message_id)
        return MessageStatus(message_id=message_id, status=str(result["status"]))
    except InfraiError as error:
        client_status = error.status_code if 400 <= error.status_code < 500 else 502
        raise HTTPException(status_code=client_status, detail=error.detail) from error


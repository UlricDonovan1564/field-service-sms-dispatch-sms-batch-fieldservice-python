from enum import Enum

from pydantic import BaseModel, Field, HttpUrl


class DispatchStatus(str, Enum):
    scheduled = "scheduled"
    en_route = "en_route"
    on_site = "on_site"
    complete = "complete"


class WorkOrder(BaseModel):
    work_order_id: str = Field(min_length=1)
    customer_name: str = Field(min_length=1)
    customer_phone: str = Field(min_length=1)
    appointment_window: str = Field(min_length=1)
    dispatch_status: DispatchStatus
    technician_name: str = Field(min_length=1)
    photo_urls: list[HttpUrl] = Field(default_factory=list)
    follow_up_note: str | None = None


class CampaignRequest(BaseModel):
    campaign_id: str = Field(min_length=1)
    work_orders: list[WorkOrder] = Field(min_length=1, max_length=100)


class MessageReceipt(BaseModel):
    work_order_id: str
    message_id: str
    dispatch_status: DispatchStatus


class CampaignReceipt(BaseModel):
    campaign_id: str
    messages: list[MessageReceipt]


class MessageStatus(BaseModel):
    message_id: str
    status: str


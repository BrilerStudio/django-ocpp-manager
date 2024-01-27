from pydantic import BaseModel

from app import SessionStatus


class CreateChargingSessionView(BaseModel):
    status: SessionStatus = SessionStatus.IN_PROGRESS
    charge_point_id: str
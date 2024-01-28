from __future__ import annotations

from ocpp.v16.enums import ChargePointStatus
from pydantic import BaseModel


class ConnectorView(BaseModel):
    status: ChargePointStatus

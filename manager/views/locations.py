from __future__ import annotations

from pydantic import BaseModel


class SimpleLocation(BaseModel):
    id: str
    name: str
    city: str

    class Config:
        orm_mode = True


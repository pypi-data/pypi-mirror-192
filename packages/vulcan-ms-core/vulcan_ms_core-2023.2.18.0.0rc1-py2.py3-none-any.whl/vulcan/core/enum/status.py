from pydantic import BaseModel


class StatusEnum(BaseModel):
    ACTIVE = "A"
    INACTIVE = "I"

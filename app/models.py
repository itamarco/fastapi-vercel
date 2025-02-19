from pydantic import BaseModel


class MessageCreate(BaseModel):
    message: str

class MessageResponse(MessageCreate):
    id: int

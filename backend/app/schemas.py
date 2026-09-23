from pydantic import BaseModel, Field


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    session_id: str = Field(default="")
    user_email: str = Field(default="")


class ChatOut(BaseModel):
    reply: str
    ask_email: bool = False
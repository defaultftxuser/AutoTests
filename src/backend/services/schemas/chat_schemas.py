from typing import Optional

from pydantic import BaseModel, RootModel


class CreateMessageResponseSchema(BaseModel):
    id: str
    ts: int
    sessionId: str
    text: str
    sender: str


class Payload(BaseModel):
    queryId: Optional[str] = None
    showTitle: Optional[str] = None
    accuracy: Optional[str] = None
    files: Optional[str] = None
    externalMessageId: Optional[str] = None
    messageGroupId: Optional[str] = None
    sessionId: Optional[str] = None
    answerLevel: Optional[str] = None
    documentId: Optional[str] = None
    serviceId: Optional[str] = None
    answeredBy: Optional[str] = None
    application: Optional[str] = None
    autofaqServiceTitle: Optional[str] = None
    answerId: Optional[str] = None
    seen: Optional[str] = None


class Button(BaseModel):
    text: str
    payload: str


class Keyboard(BaseModel):
    buttons: Optional[list[Button]] = []


class Message(BaseModel):
    id: str
    ts: int
    sessionId: Optional[str] = None
    text: str
    sender: Optional[str] = None
    replyToSender: Optional[str] = None
    payload: Optional[Payload] = None
    keyboard: Optional[Keyboard] = None


class MessagesList(RootModel):
    root: list[Message]

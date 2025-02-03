from typing import Optional

from pydantic import BaseModel, RootModel, Field


class CreateMessageResponseSchema(BaseModel):
    id: str
    ts: int
    session_id: str = Field(None, alias="sessionId")
    text: str
    sender: str


class CreateMessageSchema(BaseModel):
    id: str | None = None
    ts: int | None = None
    text: str | None = None


class Payload(BaseModel):
    query_id: Optional[str] = Field(None, alias="queryId")
    show_title: Optional[str] = Field(None, alias="showTitle")
    accuracy: Optional[str] = None
    files: Optional[str] = None
    external_message_id: Optional[str] = Field(None, alias="externalMessageId")
    message_group_id: Optional[str] = Field(None, alias="messageGroupId")
    session_id: str = Field(None, alias="sessionId")
    answer_level: Optional[str] = Field(None, alias="answerLevel")
    document_id: Optional[str] = Field(None, alias="documentId")
    service_id: Optional[str] = Field(None, alias="serviceId")
    answered_by: Optional[str] = Field(None, alias="answeredBy")
    application: Optional[str] = None
    auto_faq_service_title: Optional[str] = Field(None, alias="autofaqServiceTitle")
    answer_id: Optional[str] = Field(None, alias="answerId")
    seen: Optional[str] = None


class Button(BaseModel):
    text: str
    payload: str


class Keyboard(BaseModel):
    buttons: Optional[list[Button]] = []


class Message(BaseModel):
    id: str
    ts: int
    session_id: str = Field(None, alias="sessionId")
    text: str
    sender: Optional[str] = None
    reply_to_sender: Optional[str] = Field(None, alias="replyToSender")
    payload: Optional[Payload] = None
    keyboard: Optional[Keyboard] = None


class MessagesList(RootModel):
    root: list[Message]

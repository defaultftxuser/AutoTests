import allure
from httpx import AsyncClient

from src.backend.config.headers import Headers
from src.backend.services.endpoints import Endpoints
from src.backend.services.payloads import Payloads
from src.backend.services.schemas.chat_schemas import MessagesList, CreateMessageResponseSchema
from src.backend.utils.helper import Helper


class ChatAPI(Helper):

    def __init__(self):
        self.payloads = Payloads()
        self.headers = Headers()
        self.endpoints = Endpoints()

    @allure.step("Получение сообщений")
    async def get_messages(self, session_id: str) -> MessagesList:
        async with AsyncClient() as client:
            response = await client.get(
                url=self.endpoints.messages_endpoint,
                headers=self.headers.get_chat_headers(session_id=session_id)
            )
            response.raise_for_status()

            self.attach_response(response=response.json())
            return MessagesList.model_validate(response.json()) if response.json() else []

    @allure.step("Создание сообщений")
    async def create_message(self, message_id: str, session_id: str, message: str) -> CreateMessageResponseSchema:
        async with AsyncClient() as client:
            response = await client.post(
                url=self.endpoints.messages_endpoint,
                headers=self.headers.get_chat_headers(session_id=session_id),
                files={"payload": (None, self.payloads.convert_to_string(
                    self.payloads.create_message_payload(id=message_id, text=message)), "application/json")}

            )
            response.raise_for_status()
            self.attach_response(response=response.json())
            response_schema = CreateMessageResponseSchema(**response.json())
            return response_schema

import allure
from httpx import AsyncClient

from src.backend.config.headers import Headers
from src.backend.config.endpoints import Endpoints
from src.backend.config.payloads import Payloads
from src.backend.services.schemas.chat_schemas import MessagesList, CreateMessageResponseSchema, CreateMessageSchema
from src.backend.utils.helper import Helper


class ChatAPI:

    def __init__(self):
        self.payloads = Payloads()
        self.helper = Helper()
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
            self.helper.attach_response(response=response.json())
            return MessagesList.model_validate(response.json()) if response.json() else []

    @allure.step("Создание сообщений")
    async def create_message(self, message_entity: CreateMessageSchema, session_id: str) -> CreateMessageResponseSchema:
        async with AsyncClient() as client:
            response = await client.post(
                url=self.endpoints.messages_endpoint,
                headers=self.headers.get_chat_headers(session_id=session_id),
                files={
                    "payload": (None, self.payloads.convert_to_json(message_entity.model_dump()), "application/json")}

            )
            response.raise_for_status()
            self.helper.attach_response(response=response.json())
            response_schema = CreateMessageResponseSchema(**response.json())
            return response_schema

    @allure.step("Цикл с попытками получить список сообщений с ответом от бота с session-id")
    async def get_messages_with_bot_answer(self, session_id: str) -> MessagesList:
        for _ in range(10):
            messages_schema = await self.get_messages(session_id=session_id)
            if len(messages_schema.root) >= 2:
                return messages_schema
        raise TimeoutError("Не удалось дождаться ответа от бота")

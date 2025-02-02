import allure
import httpx
import pytest

from src.backend.config.base_test import BaseTest


class TestUsers(BaseTest):

    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    @allure.title("Успешное создание сообщения")
    async def test_successfully_create_message(self):
        session_id = self.chat_api.headers.get_chat_header_value()
        payload = self.chat_api.payloads.create_message_payload()
        created_message = await self.chat_api.create_message(
            message_id=payload.get("id"),
            session_id=session_id,
            message=payload.get("text"))
        assert created_message.sessionId == session_id
        assert created_message.id == payload.get("id")
        assert created_message.text == payload.get("text")

    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.api
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    @allure.title("Создание сообщения без session-id")
    async def test_create_message_without_session_id(self):
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            session_id = None
            payload = self.chat_api.payloads.create_message_payload()
            await self.chat_api.create_message(
                message_id=payload.get("id"),
                session_id=session_id,
                message=payload.get("text"))

        assert exc_info.value.response.status_code in [400]

    @pytest.mark.asyncio
    @pytest.mark.validation
    @pytest.mark.api
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.negative
    @pytest.mark.functional
    @allure.title("Создаение длинного сообщения")
    async def test_create_long_message(self):
        session_id = self.chat_api.headers.get_chat_header_value()
        chat_payload = self.chat_api.payloads.create_message_payload()
        await self.chat_api.create_message(
            message_id=chat_payload.get("id"),
            session_id=session_id,
            message=chat_payload.get("text") * 500
        )

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await self.chat_api.get_messages(session_id=session_id)

        assert exc_info.value.response.status_code in [400]

    @pytest.mark.asyncio
    @pytest.mark.validation
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.api
    @pytest.mark.negative
    @pytest.mark.functional
    @allure.title("Создаение пустого сообщения")
    async def test_create_empty_message(self):
        session_id = self.chat_api.headers.get_chat_header_value()
        chat_payload = self.chat_api.payloads.create_message_payload()
        await self.chat_api.create_message(
            message_id=chat_payload.get("id"),
            session_id=session_id,
            message=chat_payload.get("text")[:0]
        )
        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await self.chat_api.get_messages(session_id=session_id)

        assert exc_info.value.response.status_code in [400]

    @pytest.mark.validation
    @pytest.mark.negative
    @pytest.mark.api
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.asyncio
    @pytest.mark.functional
    @allure.title("Получение сообщений")
    async def test_get_messages(self, faker):
        session_id = faker.uuid4()
        await self.chat_api.get_messages(session_id=session_id)

    @pytest.mark.asyncio
    @pytest.mark.critical
    @pytest.mark.api
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.functional
    @allure.title("Создание сообщения и получение сообщений с ответом от бота с кнопками")
    async def test_get_messages_with_answers(self):
        session_id = self.chat_api.headers.get_chat_header_value()
        payload = self.chat_api.payloads.create_message_payload(text="меню")
        await self.chat_api.create_message(
            message_id=payload.get("id"),
            session_id=session_id,
            message=payload.get("text"))
        messages_schema = await self.chat_api.get_messages(session_id=session_id)
        for _ in range(10):
            messages_schema = await self.chat_api.get_messages(session_id=session_id)
            if len(messages_schema.root) >= 2:
                break
        assert len(messages_schema.root) >= 2
        assert messages_schema.root[0].text == payload.get("text")
        assert messages_schema.root[0].id == payload.get("id")
        assert messages_schema.root[0].sessionId == session_id
        assert messages_schema.root[0].sender == session_id
        assert messages_schema.root[1].payload.externalMessageId == payload.get("id")
        assert messages_schema.root[1].text == "Выберите, что вас интересует или задайте свой вопрос"
        assert messages_schema.root[1].replyToSender == "reply"
        assert len(messages_schema.root[1].keyboard.buttons) == 9

    @pytest.mark.validation
    @pytest.mark.negative
    @pytest.mark.api
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.asyncio
    @pytest.mark.functional
    @allure.title("Получение сообщений с неправильным значением session-id")
    async def test_get_messages_with_wrong_session_id(self, faker):
        session_id = None

        with pytest.raises(httpx.HTTPStatusError) as exc_info:
            await self.chat_api.get_messages(session_id=session_id)

        assert exc_info.value.response.status_code in [400]

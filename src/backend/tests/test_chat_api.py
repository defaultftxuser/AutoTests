import allure
import httpx
import pytest

from src.backend.services.schemas.chat_schemas import CreateMessageSchema


@allure.severity(allure.severity_level.NORMAL)
@allure.title("Попытка создания сообщения с неверными значениями session-id")
@pytest.mark.parametrize("get_session_id",
                         [
                             None,
                             "Test",
                         ], indirect=True)
@pytest.mark.asyncio
async def test_create_message_with_wrong_session_id(get_api, get_chat_message_payload, get_session_id):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await get_api.chat_api.create_message(message_entity=get_chat_message_payload,
                                              session_id=get_session_id)
    assert exc_info.value.response.status_code in [400]


@allure.severity(allure.severity_level.NORMAL)
@allure.title("Попытка создания сообщения с неверными значениями в payload'е")
@pytest.mark.parametrize("get_chat_message_payload",
                         [
                             CreateMessageSchema(id="", ts=0, text=""),
                             CreateMessageSchema(id="123456789", ts=-1, text=""),
                             CreateMessageSchema(id="", ts=0, text="Test text"),
                         ], indirect=True)
@pytest.mark.asyncio
async def test_create_message_with_wrong_payload(get_api, get_chat_message_payload, get_session_id):
    with pytest.raises(httpx.HTTPStatusError) as exc_info:
        await get_api.chat_api.create_message(message_entity=get_chat_message_payload,
                                              session_id=get_session_id)
    assert exc_info.value.response.status_code in [400]


@pytest.mark.validation
@pytest.mark.negative
@pytest.mark.api
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.asyncio
@pytest.mark.functional
@allure.title("Получение сообщений со случайным значением session-id")
async def test_get_messages(faker, get_api):
    session_id = faker.uuid4()
    await get_api.chat_api.get_messages(session_id=session_id)


@pytest.mark.asyncio
@pytest.mark.critical
@pytest.mark.api
@pytest.mark.smoke
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.functional
@allure.title("Создание сообщения и получение сообщений с ответом от бота")
async def test_get_messages_with_answers(get_api, get_chat_message_payload,
                                         get_session_id):
    """
    Flaky тест, задание было чтобы некоторые тесты падали (
    не всегда бот успевает отвечать, фиксится увеличением
    количества запросов на получение сообщений с ответом от бота,
     либо задержкой между запросами
    )
    """
    await get_api.chat_api.create_message(message_entity=get_chat_message_payload,
                                          session_id=get_session_id)
    question_message_schema, bot_answer_schema = (
        await get_api.chat_api.get_messages_with_bot_answer(session_id=get_session_id)).root

    assert question_message_schema.id == get_chat_message_payload.id
    assert question_message_schema.text == get_chat_message_payload.text
    assert question_message_schema.sender == get_session_id
    assert question_message_schema.session_id == get_session_id

    assert bot_answer_schema.payload.external_message_id == get_chat_message_payload.id
    assert bot_answer_schema.reply_to_sender == "reply"

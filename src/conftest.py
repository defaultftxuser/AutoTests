import datetime

import pytest
from faker import Faker
from playwright.async_api import async_playwright,  Browser,  Page

from src.backend.services.api_aggregator import APIAggregator
from src.backend.services.schemas.chat_schemas import CreateMessageSchema


@pytest.fixture(scope="function")
def get_faker() -> Faker:
    return Faker()


@pytest.fixture(scope="function")
def get_session_id(request: pytest.FixtureRequest, get_faker: Faker) -> str:
    return request.param if hasattr(request, "param") else get_faker.uuid4()


@pytest.fixture(scope="function")
def get_chat_message_payload(request: pytest.FixtureRequest, get_faker: Faker) -> CreateMessageSchema:
    if hasattr(request, "param") and isinstance(request.param, CreateMessageSchema):
        return request.param

    return CreateMessageSchema(
        id=get_faker.uuid4(),
        ts=int(datetime.datetime.now().timestamp()),
        text=get_faker.text(),
    )


@pytest.fixture(scope="session")
def get_api() -> APIAggregator:
    return APIAggregator()


@pytest.fixture(scope="function")
async def browser() -> Browser:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        yield browser
        await browser.close()


@pytest.fixture(scope="function")
async def page(browser: Browser, request) -> Page:
    context = await browser.new_context(record_video_dir="allure-results/videos/")
    page = await context.new_page()
    request.cls.page = page
    yield page

    await context.close()

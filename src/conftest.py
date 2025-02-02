import allure
import pytest
from faker import Faker
from playwright.async_api import async_playwright


@pytest.fixture(scope="session")
def faker():
    return Faker()


@pytest.fixture(scope="session")
def get_menu_payload():
    return {
        "id": Faker().uuid4(),
        "ts": 0,
        "text": "меню"
    }


@pytest.fixture(scope="session")
def get_session_id():
    return Faker().uuid4()


@pytest.fixture(scope="function")
def get_faker() -> Faker:
    return Faker()


@pytest.mark.parametrize("browser_name", ["chromium", "firefox", "webkit"])
@pytest.fixture(scope="function", autouse=True)
async def page_with_video(request, browser_name) -> tuple:
    async with async_playwright() as p:
        browser = await getattr(p, browser_name).launch(headless=True)
        context = await browser.new_context(record_video_dir="allure-results/videos/")
        page = await context.new_page()

        request.cls.driver = page
        request.cls.context = context

        yield page, context

        if request.node.rep_call.failed:
            await page.screenshot(path="allure-results/failure_screenshot.png")
            allure.attach.file("allure-results/failure_screenshot.png",
                               name="Итоговый скриншот",
                               attachment_type=allure.attachment_type.PNG)

            video_path = await page.video.path()
            await context.close()
            allure.attach.file(video_path,
                               name="Видео с тестом",
                               attachment_type=allure.attachment_type.WEBM)

        await context.close()
        await browser.close()

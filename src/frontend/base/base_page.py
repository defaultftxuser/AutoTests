import shutil

import allure
from allure_commons.types import AttachmentType
from playwright.async_api import Page, BrowserContext, expect


class BasePage:
    PAGE_URL = ""

    def __init__(self, page: Page, context: BrowserContext):
        self.page = page
        self.context = context

    async def open(self):
        with allure.step(f"Открытие {self.PAGE_URL} страницы"):
            await self.page.goto(self.PAGE_URL)

    async def is_opened(self):
        with allure.step(f"Страница {self.PAGE_URL} открыта"):
            await expect(self.page).to_have_url(self.PAGE_URL)

    async def make_screenshot(self, screenshot_name):
        with allure.step(f"Делаю скриншот: {screenshot_name}"):
            screenshot = await self.page.screenshot()
            allure.attach(
                body=screenshot,
                name=screenshot_name,
                attachment_type=AttachmentType.PNG
            )

    async def stop_recording_video(self):
        await self.context.close()

    async def close_page(self):
        await self.page.close()

    async def attach_video(self):
        with allure.step("Прикрепление видео"):
            video_path = await self.page.video.path()
            allure.attach.file(
                video_path,
                name="Видео с тестом",
                attachment_type=AttachmentType.WEBM
            )

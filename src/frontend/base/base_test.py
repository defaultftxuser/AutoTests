import pytest
from playwright.async_api import Page

from src.frontend.pages.main_page import MainPage


class BaseTest:

    main_page: MainPage

    @pytest.fixture(autouse=True)
    def setup(self, page: Page) -> None:
        self.main_page = MainPage(page)

    @pytest.fixture(scope="function")
    async def open_page_with_chat_widget(self, page: Page) -> bool:
        await self.main_page.open()
        chat_button = await self.main_page.check_chat_widget_button_is_visible()
        await self.main_page.click_chat_button(chat_button=chat_button)
        return True

    @pytest.fixture(scope="function")
    async def change_window_size_and_get_chat_window_resolution(self, open_page_with_chat_widget) -> bool:
        await self.main_page.open()
        chat_button = await self.main_page.check_chat_widget_button_is_visible()
        await self.main_page.click_chat_button(chat_button=chat_button)
        return True

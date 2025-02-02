import pytest
from playwright.async_api import async_playwright, Page

from src.frontend.pages.main_page import MainPage


class BaseTest:

    main_page: MainPage

    @pytest.fixture(autouse=True)
    def setup(self, request, page_with_video):
        page, context = page_with_video
        self.main_page = MainPage(page,context)

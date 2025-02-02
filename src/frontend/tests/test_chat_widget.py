import pytest
import allure

from src.frontend.base.base_test import BaseTest


@pytest.mark.asyncio
@allure.feature("Chat Widget")
class TestChatWidget(BaseTest):


    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.positive
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Проверка наличия кнопки чата и её кликабельности")
    async def test_chat_widget_button_is_visible_and_clickable(self, get_faker):
        await self.main_page.open()
        await self.main_page.click_chat_button()


    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.positive
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Нажатие на кнопку чата и проверка ввода и отправки в чат виджет и получение ответа с кнопками")
    async def test_chat_input_menu_and_answer_with_buttons(self, get_faker):
        await self.main_page.open()
        await self.main_page.click_chat_button()
        await self.main_page.fill_chat_input(get_faker.text())
        await self.main_page.click_submit_text_chat_button()
        buttons_list = await self.main_page.get_menu_buttons_bot_answer()
        assert await self.main_page.check_menu_buttons_bot_answer(buttons_list) is True
        assert await self.main_page.get_answer_from_bot() == "Выберите, что вас интересует или задайте свой вопрос"

    @pytest.mark.asyncio
    @pytest.mark.smoke
    @pytest.mark.ui
    @pytest.mark.positive
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title(
        "Нажатие на кнопку чата проверка ввода текста с заполненными именем и почтой и отправки в чат-помощник и получение ответа")
    async def test_chat_input_name_and_email_and_answer_from_bot(self, get_faker):
        await self.main_page.open()
        await self.main_page.click_chat_button()
        await self.main_page.fill_name_input(get_faker.name())
        await self.main_page.fill_email_input(get_faker.email())
        await self.main_page.click_submit_name_and_email_form()
        await self.main_page.check_submit_name_and_email_form_is_hidden()
        await self.main_page.fill_chat_input(get_faker.job())
        await self.main_page.click_submit_text_chat_button()

    @allure.title(
        "Проверка ввода текста с заполненными именем и неправильной почтой")
    @pytest.mark.asyncio
    @pytest.mark.negative
    @pytest.mark.ui
    @pytest.mark.smoke
    @allure.severity(allure.severity_level.NORMAL)
    async def test_chat_input_name_and_wrong_email(self, faker):
        await self.main_page.open()
        await self.main_page.click_chat_button()
        await self.main_page.fill_name_input(faker.text())
        await self.main_page.fill_email_input(faker.text())
        await self.main_page.click_submit_name_and_email_form()
        await self.main_page.check_submit_name_and_email_form_is_hidden()

    @allure.severity(allure.severity_level.MINOR)
    @allure.title(
        "Проверка изменения изменения виджета в зависимости от разрешения экрана")
    @pytest.mark.asyncio
    @pytest.mark.ui
    @pytest.mark.positive
    async def test_chat_window_size_adaptivity(self):
        original_resolution_size = {"width": 1920, "height": 1080}
        changed_resolution_size = {"width": 900, "height": 600}
        await self.main_page.change_window_size(
            original_resolution_size.get("width"),
            original_resolution_size.get("height"))
        await self.main_page.open()
        await self.main_page.click_chat_button()
        original_window_size = await self.main_page.get_chat_window_resolution()
        await self.main_page.change_window_size(
            changed_resolution_size.get("width"),
            changed_resolution_size.get("height"))
        changed_window_size = await self.main_page.get_chat_window_resolution()
        await self.main_page.change_window_size(
            original_resolution_size.get("width"),
            original_resolution_size.get("height"))

        assert original_window_size == changed_window_size

import pytest
import allure

from src.frontend.base.base_test import BaseTest
from src.frontend.common.common import check_menu_buttons_bot_answer, attach_screenshot_and_video_on_failure


@pytest.mark.asyncio
@allure.epic("Главная страница")
class TestMainPage(BaseTest):

    # @allure.feature("Чат виджет")
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.title(
    #     "Проверка наличия кнопки чата и её кликабельности")
    # @attach_screenshot_and_video_on_failure
    # @pytest.mark.smoke
    # @pytest.mark.ui
    # @pytest.mark.positive
    # async def test_chat_widget_button_is_visible_and_clickable(self, open_page_with_chat_widget):
    #     assert open_page_with_chat_widget
    #
    #
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.title(
    #     "Проверка на вводимые данные в виджет чате и получение ответа от бота без кнопок")
    # @attach_screenshot_and_video_on_failure
    # @pytest.mark.smoke
    # @pytest.mark.ui
    # @pytest.mark.positive
    # async def test_chat_input_menu_and_answer_with_buttons(self, open_page_with_chat_widget):
    #     assert open_page_with_chat_widget
    #     await self.main_page.fill_chat_input("Привет")
    #     await self.main_page.fill_chat_inputted_correctly("Привет")
    #     await self.main_page.click_submit_text_chat_button()
    #     assert await self.main_page.check_inputted_message_scend_correctly() == "Привет"
    #     assert await self.main_page.get_answer_from_bot() == "Привет!"
    #
    # @allure.feature("Чат виджет")
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.title(
    #     "Проверка на вводимые данные в виджет чате и получение ответа от бота с кнопками")
    # @attach_screenshot_and_video_on_failure
    # @pytest.mark.smoke
    # @pytest.mark.ui
    # @pytest.mark.positive
    # async def test_chat_input_menu_and_answer_with_buttons(self, open_page_with_chat_widget):
    #     """
    #     Падающий тест, написан для того что бы можно было посмотреть отчет о упавшем тесте
    #
    #     """
    #     assert open_page_with_chat_widget
    #     await self.main_page.fill_chat_input("меню")
    #     await self.main_page.fill_chat_inputted_correctly("меню")
    #     await self.main_page.click_submit_text_chat_button()
    #     buttons_list = await self.main_page.get_menu_buttons_bot_answer()
    #     assert check_menu_buttons_bot_answer(buttons_list) is True
    #     assert await self.main_page.get_answer_from_bot() == "Выберите, что вас интересует или задайте свой вопрос"
    #     assert False
    #
    # @allure.feature("Чат виджет")
    # @allure.severity(allure.severity_level.CRITICAL)
    # @allure.title(
    #     "Проверка ввода текста с заполненными именем и почтой и отправки в чат-помощник и получение ответа")
    # @attach_screenshot_and_video_on_failure
    # @pytest.mark.smoke
    # @pytest.mark.ui
    # @pytest.mark.positive
    # async def test_chat_input_name_and_email_and_answer_from_bot(self, open_page_with_chat_widget, get_faker):
    #     assert open_page_with_chat_widget
    #     await self.main_page.fill_name_input(get_faker.name())
    #     await self.main_page.fill_email_input(get_faker.email())
    #     await self.main_page.click_submit_name_and_email_form()
    #     await self.main_page.check_submit_name_and_email_form_is_hidden()
    #     await self.main_page.fill_chat_input(get_faker.job())
    #     await self.main_page.click_submit_text_chat_button()
    #
    # @allure.feature("Чат виджет")
    # @allure.severity(allure.severity_level.NORMAL)
    # @allure.title(
    #     "Проверка ввода текста в форму заполнения имени и почты с неправильной почтой")
    # @attach_screenshot_and_video_on_failure
    # @pytest.mark.negative
    # @pytest.mark.ui
    # @pytest.mark.smoke
    # async def test_chat_input_name_and_wrong_email(self, open_page_with_chat_widget, faker):
    #     assert open_page_with_chat_widget
    #     await self.main_page.fill_name_input(faker.text())
    #     await self.main_page.fill_email_input(faker.text())
    #     await self.main_page.click_submit_name_and_email_form()
    #     await self.main_page.check_submit_name_and_email_form_is_hidden()

    @allure.feature("Чат виджет")
    @allure.severity(allure.severity_level.MINOR)
    @allure.title(
        "Проверка изменения изменения виджета в зависимости от разрешения экрана")
    @attach_screenshot_and_video_on_failure
    @pytest.mark.ui
    @pytest.mark.positive
    async def test_chat_window_size_adaptivity(self, get_faker, open_page_with_chat_widget):
        original_resolution = await self.main_page.change_window_size(width=get_faker.random_int(min=1500, max=1920),
                                                                      height=get_faker.random_int(min=1500, max=1700))
        assert open_page_with_chat_widget
        original_chat_window_resolution = await self.main_page.get_chat_window_resolution()
        await self.main_page.change_window_size(width=get_faker.random_int(min=100, max=300),
                                                                     height=get_faker.random_int(min=100, max=300))
        await self.main_page.change_window_size(width=original_resolution.width,
                                                height=original_resolution.height)
        chat_window_resolution_after_change_resolution = await self.main_page.get_chat_window_resolution()

        assert original_chat_window_resolution == chat_window_resolution_after_change_resolution

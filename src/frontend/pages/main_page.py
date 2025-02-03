import allure
from playwright.async_api import Page, expect, ElementHandle

from src.frontend.base.base_page import BasePage
from src.frontend.components.schemas.window_schemas import WindowSizeSchema


class MainPage(BasePage):
    PAGE_URL = "https://autofaq.ai"

    _chat_widget_button_locator = "#chat21-launcher-button"
    _chat_conversation_locator = "#chat21-conversations"
    _chat_input_form_locator = "#chat21-main-message-context"
    _chat_submit_input_form_locator = "#chat21-button-send"
    _chat_scend_message_locator = ".msg_container.base_sent .messages.msg_sent .msg_content"

    _chat_bot_answer_buttons_locator = "div.msg_container.base_receive.buttons"
    _chat_bot_text_answer = "div.msg_container.base_receive .msg_receive .msg_content"

    _user_form_send_email_locator = "#user-form_field_senderEmail"
    _user_form_send_name_locator = "#user-form_field_senderFullName"
    _user_form_send_submit_button_locator = ".form_panel_action.form_panel_action-submit"
    _user_form_window_locator = ".form_panel"

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step("Открытие главной страницы")
    async def open(self) -> None:
        await self.page.goto(self.PAGE_URL, wait_until="domcontentloaded")

    @allure.step("Кнопка виджет чата видна на странице")
    async def check_chat_widget_button_is_visible(self) -> ElementHandle:
        return await self.page.wait_for_selector(self._chat_widget_button_locator, state="visible")

    @allure.step("Клик на кнопку виджет чата")
    async def click_chat_button(self, chat_button: ElementHandle) -> None:
        await chat_button.click()

    @allure.step("Заполнение формы имени в виджет чате")
    async def fill_name_input(self, name) -> None:
        await self.page.fill(self._user_form_send_name_locator, name)

    @allure.step("Заполнение формы почты в виджет чате")
    async def fill_email_input(self, email: str) -> None:
        await self.page.fill(self._user_form_send_email_locator, email)

    @allure.step("Отправка введеных сообщений в форме отправки имени и почты")
    async def click_submit_name_and_email_form(self) -> None:
        await self.page.click(self._user_form_send_submit_button_locator)

    @allure.step("Проверка что панель ввода имени и почты пропала")
    async def check_submit_name_and_email_form_is_hidden(self) -> None:
        return await self.page.wait_for_selector(self._chat_conversation_locator, state="visible", timeout=3000)

    @allure.step("Проверка что панель ввода имени и почты пропала")
    async def check_submit_name_and_email_form_is_hidden(self) -> None:
        await expect(self.page.locator(self._user_form_window_locator)).to_be_hidden(timeout=5000)

    @allure.step("Заполнение формы для отправки сообщения в чат-помощник")
    async def fill_chat_input(self, input_text: str) -> None:
        await self.page.fill(self._chat_input_form_locator, input_text)

    @allure.step("Заполнение формы для отправки сообщения в чат-помощник")
    async def fill_chat_inputted_correctly(self, input_text: str) -> None:
        assert await self.page.locator(self._chat_input_form_locator).input_value() == input_text

    @allure.step("Отправка введеных сообщений в чат помощник с помощью кнопки")
    async def click_submit_text_chat_button(self) -> None:
        send_button = await self.page.wait_for_selector(self._chat_submit_input_form_locator, state="visible")
        await send_button.click()

    @allure.step("Проверка что при ответе бот вернул 9 кнопок с текстом")
    async def get_menu_buttons_bot_answer(self) -> list[str]:
        await self.page.wait_for_selector(self._chat_bot_answer_buttons_locator, state="visible")

        buttons_text = await self.page.eval_on_selector_all(
            ".msg_container .messages.button.success", "nodes => nodes.map(n => n.innerText.trim())"
        )
        return buttons_text

    @allure.step("Проверка наличия ответа от бота")
    async def get_answer_from_bot(self) -> str:
        last_message = await self.page.inner_text(self._chat_bot_text_answer)
        return last_message

    @allure.step("Получение последнего сообщения в чате")
    async def check_inputted_message_scend_correctly(self) -> str:
        last_message = await self.page.wait_for_selector(self._chat_scend_message_locator, state="visible")
        return await last_message.inner_text()

    @allure.step("Получение разрешения окна чата виджета")
    async def get_chat_window_resolution(self):
        return WindowSizeSchema(**await self.page.evaluate("""
            () => {
                let chat = document.querySelector('#chat21-conversations');
                return { width: chat.offsetWidth, height: chat.offsetHeight };
            }
        """))

    @allure.step("Изменение разрешения экрана")
    async def change_window_size(self, width: int, height: int) -> WindowSizeSchema:
        await self.page.set_viewport_size({"width": width, "height": height})
        return WindowSizeSchema(width=width, height=height)

import allure
from playwright.async_api import Page, async_playwright, BrowserContext, expect

from src.frontend.base.base_page import BasePage


class MainPage(BasePage):
    PAGE_URL = "https://autofaq.ai"

    def __init__(self, page: Page, context: BrowserContext):
        super().__init__(page, context)

    @allure.step("Открытие главной страницы")
    async def open(self):
        await self.page.goto(self.PAGE_URL, wait_until="domcontentloaded")

    @allure.step("Клик на кнопку виджет чата-помощника")
    async def click_chat_button(self):
        chat_button = await self.page.wait_for_selector('#chat21-launcher-button', state="visible")
        await chat_button.click()

    @allure.step("Клик на кнопку виджет чата-помощника")
    async def fill_name_input(self, name):
        await self.page.fill('#user-form_field_senderFullName', name)

    @allure.step("Клик на кнопку виджет чата-помощника")
    async def fill_email_input(self, email):
        await self.page.fill('#user-form_field_senderEmail', email)

    @allure.step("Отправка введеных сообщений в чат помощник")
    async def click_submit_name_and_email_form(self):
        await self.page.click('.form_panel_action.form_panel_action-submit')

    @allure.step("Проверка что панель ввода имени и почты пропала")
    async def check_submit_name_and_email_form_is_hidden(self):
        await expect(self.page.locator(".form_panel")).to_be_hidden(timeout=5000)


    @allure.step("Заполнение формы для отправки сообщения в чат-помощник")
    async def fill_chat_input(self, input_text: str):
        await self.page.fill("#chat21-main-message-context", input_text)

    @allure.step("Отправка введеных сообщений в чат помощник")
    async def click_submit_text_chat_button(self):
        send_button = await self.page.wait_for_selector("#chat21-button-send", state="visible")
        await send_button.click()

    @allure.step("Проверка ответа от бота при введении слова 'меню' в чат")
    async def check_menu_buttons_bot_answer(self, buttons_list: list[str]):
        buttons_set = {
            "Стоимость системы",
            "Запланировать демо",
            "Продукты",
            "Решения",
            "Варианты установки",
            "Шаблон ТЗ",
            "Документация",
            "Описание API",
            "Стать партнером",

        }
        for button in buttons_list:
            if button not in buttons_set:
                return False
        return True

    @allure.step("Проверка что при ответе бот вернул 9 кнопок с текстом")
    async def get_menu_buttons_bot_answer(self):
        await self.page.wait_for_selector("div.msg_container.base_receive.buttons", state="visible")

        buttons_text = await self.page.eval_on_selector_all(
            ".msg_container .messages.button.success", "nodes => nodes.map(n => n.innerText.trim())"
        )
        return buttons_text

    @allure.step("Проверка наличия ответа от бота")
    async def get_answer_from_bot(self):

        last_message = await self.page.inner_text("div.msg_container.base_receive .msg_receive .msg_content")
        return last_message

    async def get_last_message_text(self) -> str:
        last_message = await self.page.wait_for_selector(".chat21-message-text:last-child", state="visible")
        return await last_message.inner_text()

    async def get_chat_window_resolution(self):
        return await self.page.evaluate("""
            () => {
                let chat = document.querySelector('#chat21-conversations');
                return { width: chat.offsetWidth, height: chat.offsetHeight };
            }
        """)

    async def change_window_size(self, width: int, height:int):
        await self.page.set_viewport_size({"width": width, "height": height})

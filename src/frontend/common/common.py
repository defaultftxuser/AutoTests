import functools
import time
from typing import Callable

import allure

from src.frontend.base.base_page import BasePage


@allure.step("Проверка ответа от бота при введении слова 'меню' в чат")
def check_menu_buttons_bot_answer(buttons_list: list[str]) -> bool:
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
            raise ValueError("Such button not presented in button's template")
    return True


def attach_screenshot_and_video_on_failure(func: Callable) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            page = args[0].page
            base_page = BasePage(page)

            screenshot_name = f"{func.__name__}_screenshot.png"
            await base_page.make_screenshot(screenshot_name)
            await base_page.page.close()

            time.sleep(2)  # TODO: Избавиться от sleep'а (Проблема в том что видео в allure прикрепляется обрезанным)

            await base_page.attach_video()

            raise e

    return wrapper

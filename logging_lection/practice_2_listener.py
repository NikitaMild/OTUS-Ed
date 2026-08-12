import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.events import AbstractEventListener, EventFiringWebDriver
from logger_config import setup_logger

# Инициализируем общий логгер
logger = setup_logger()

class CustomListener(AbstractEventListener):
    def __init__(self):
        # Дочерний логгер для модуля Listener
        self.log = logging.getLogger("AutomationFramework.Listener")

    def before_click(self, element, driver):
        self.log.info(f"-> [Listener] Готовимся кликнуть по <{element.tag_name}> (текст: '{element.text.strip()}')")

    def after_click(self, element, driver):
        self.log.info("<- [Listener] Клик успешно завершен")

    def on_exception(self, exception, driver):
        self.log.error(f"!!! [Listener] Исключение: {type(exception).__name__}")

def run():
    logger.info("=== Запуск Практики №2: Перехват событий через EventListener ===")
    raw_driver = webdriver.Chrome()
    driver = EventFiringWebDriver(raw_driver, CustomListener())

    try:
        driver.get("https://habr.com/ru/articles/899244/")
        link = driver.find_element(By.TAG_NAME, "a")
        link.click()  # Автоматически сработает Listener
        time.sleep(1)
    finally:
        driver.quit()
        logger.info("Браузер закрыт.\n")

if __name__ == "__main__":
    run()
"""Практика 2. Автоматическое логирование действий с браузером.

Вместо устаревшего ``EventFiringWebDriver`` + ``AbstractEventListener``
(deprecated с Selenium 4.11) используем свою обёртку ``LoggingWebDriver``
из logging_driver.py: драйвер и элементы логируют действия сами.
"""
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from logger_config import setup_logger
from logging_driver import LoggingWebDriver

URL = "https://habr.com/ru/articles/899244/"

logger = setup_logger()


def run() -> None:
    logger.info("=== Запуск Практики №2: перехват событий через свою обёртку ===")

    driver = LoggingWebDriver(webdriver.Chrome())
    try:
        driver.get(URL)
        link = driver.find_element(By.TAG_NAME, "a")
        link.click()
        time.sleep(1)
    finally:
        driver.quit()
        logger.info("Браузер закрыт.\n")


if __name__ == "__main__":
    run()

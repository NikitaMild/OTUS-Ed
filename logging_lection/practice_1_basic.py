import time
from selenium import webdriver
from logger_config import setup_logger
from helper_page import BasePage

# Инициализируем корневой логгер
logger = setup_logger()

def run():
    logger.info("=== Запуск Практики №1: Логирование в нескольких файлах ===")
    driver = webdriver.Chrome()

    try:
        page = BasePage(driver)
        page.open_url("https://habr.com/ru/articles/899244/")
        
        title = page.get_page_title()
        logger.info(f"Проверка в тесте прошла успешно. Title length: {len(title)}")
        time.sleep(1)
    finally:
        driver.quit()
        logger.info("Браузер закрыт.\n")

if __name__ == "__main__":
    run()
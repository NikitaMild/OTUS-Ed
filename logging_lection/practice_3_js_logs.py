from selenium import webdriver
from logger_config import setup_logger

logger = setup_logger()

def run():
    logger.info("=== Запуск Практики №3: Сбор JS-логов браузера ===")
    
    options = webdriver.ChromeOptions()
    options.set_capability('goog:loggingPrefs', {'browser': 'ALL'})

    driver = webdriver.Chrome(options=options)

    try:
        # Страница, генерирующая Uncaught TypeError в JS
        driver.get("https://the-internet.herokuapp.com/javascript_error")

        browser_logs = driver.get_log('browser')
        for entry in browser_logs:
            if entry['level'] == 'SEVERE':
                logger.error(f"[Browser JS SEVERE] {entry['message']}")
            else:
                logger.info(f"[Browser JS LOG] {entry['message']}")
    finally:
        driver.quit()
        logger.info("Браузер закрыт.\n")

if __name__ == "__main__":
    run()
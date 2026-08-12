import logging

# Логгер регистрируется в общей иерархии под именем "AutomationFramework.BasePage"
logger = logging.getLogger("AutomationFramework.BasePage")

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open_url(self, url):
        logger.info(f"Переходим по адресу: {url}")
        self.driver.get(url)

    def get_page_title(self):
        title = self.driver.title
        logger.info(f"Получен заголовок страницы: '{title}'")
        return title
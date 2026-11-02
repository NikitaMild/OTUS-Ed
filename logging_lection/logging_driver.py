"""Обёртки над Selenium: логируют действия драйвера и элементов, остальное делегируют.

Заменяют устаревший (deprecated с Selenium 4.11) ``EventFiringWebDriver`` +
``AbstractEventListener``. Идея: обёртку пишем один раз — и получаем логи во всех
тестах, без копирования ``logger.info`` в каждый метод.
"""
import logging
from contextlib import contextmanager

logger = logging.getLogger("AutomationFramework.Listener")


@contextmanager
def log_action(action: str):
    """Пишет '->' и '<-' вокруг действия, а ошибку логирует и пробрасывает дальше."""
    logger.info("-> %s", action)
    try:
        yield
    except Exception as exc:
        logger.error("!!! %s: %s: %s", action, type(exc).__name__, exc)
        raise
    logger.info("<- %s", action)


class LoggingWebElement:
    """Обёртка над WebElement: логирует клик и ввод текста."""

    def __init__(self, element):
        self._element = element  # внутри "коробки" — настоящий WebElement

    def click(self):
        with log_action(f"клик по <{self._element.tag_name}>"):
            self._element.click()

    def send_keys(self, *value):
        # Сам введённый текст в лог не пишем: там бывают пароли и токены
        with log_action(f"ввод текста в <{self._element.tag_name}>"):
            self._element.send_keys(*value)

    def __getattr__(self, item):
        # get_attribute, is_displayed и прочее — работают, но без логирования
        return getattr(self._element, item)


class LoggingWebDriver:
    """Обёртка над WebDriver: логирует навигацию, поиск элементов и закрытие браузера."""

    def __init__(self, driver):
        self._driver = driver  # внутри "коробки" — настоящий WebDriver

    def get(self, url):
        with log_action(f"открываем {url}"):
            self._driver.get(url)

    def find_element(self, by, value):
        with log_action(f"поиск элемента ({by}={value})"):
            element = self._driver.find_element(by, value)
        # Возвращаем обёртку: все дальнейшие действия с элементом тоже попадут в лог
        return LoggingWebElement(element)

    def find_elements(self, by, value):
        elements = self._driver.find_elements(by, value)
        logger.info("<- найдено элементов (%s=%s): %s", by, value, len(elements))
        return [LoggingWebElement(element) for element in elements]

    def quit(self):
        logger.info("-> закрываем браузер")  # '<-' не будет: после quit писать уже некуда
        self._driver.quit()

    def __getattr__(self, item):
        # title, current_url, execute_script, switch_to и прочее — без логирования
        return getattr(self._driver, item)


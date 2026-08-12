import logging
import random
from contextlib import contextmanager
from datetime import datetime

# Инициализация логгера
logger = logging.getLogger("ErrorHandlerDemo")
logger.setLevel(logging.DEBUG)

# Настройка обработчиков (если их ещё нет)
if not logger.handlers:
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')

    # Консольный вывод
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)
    logger.addHandler(console_handler)

    # Файловый вывод
    file_handler = logging.FileHandler('error_handling.log', encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)


# -----------------------------------------------------------------------------
# Простая статистика ошибок
# -----------------------------------------------------------------------------

class ErrorStats:
    """Простая статистика по типам ошибок."""

    def __init__(self):
        self.errors = {}

    def record(self, error_type: str):
        """Записать ошибку в статистику."""
        self.errors[error_type] = self.errors.get(error_type, 0) + 1

    def print_summary(self):
        """Вывести сводку по ошибкам."""
        logger.info("=" * 50)
        logger.info("СТАТИСТИКА ОШИБОК:")
        logger.info("=" * 50)
        if not self.errors:
            logger.info("Ошибок не было зафиксировано")
        else:
            for error_type, count in self.errors.items():
                logger.info(f"  {error_type}: {count} раз(а)")
        logger.info("=" * 50)


error_stats = ErrorStats()


# -----------------------------------------------------------------------------
# Контекстный менеджер для автоматического логирования ошибок
# -----------------------------------------------------------------------------

@contextmanager
def log_errors(context: str):
    """
    Контекстный менеджер для автоматического логирования ошибок.
    Любое исключение внутри блока будет залогировано с полным stacktrace.
    """
    try:
        logger.debug(f"Вход в контекст: {context}")
        yield
        logger.debug(f"Выход из контекста: {context} (успешно)")
    except Exception as e:
        # logger.exception() автоматически добавляет stacktrace
        logger.exception(f"!!! ОШИБКА в контексте '{context}': {type(e).__name__}: {e}")
        error_stats.record(type(e).__name__)
        raise  # Пробрасываем исключение дальше


def parse_number(value: str) -> int:
    """
    Парсит строку в число.
    Может вызвать ValueError при некорректном вводе.
    """
    logger.debug(f"Парсинг числа: '{value}'")
    with log_errors("parse_number"):
        result = int(value)
        logger.info(f"Успешно распарсено: {result}")
        return result


def read_config_value(config: dict, key: str) -> str:
    """
    Получает значение из конфигурации.
    Может вызвать KeyError при отсутствии ключа.
    """
    logger.debug(f"Чтение конфигурации: ключ '{key}'")
    with log_errors("read_config_value"):
        if key not in config:
            logger.warning(f"Ключ '{key}' отсутствует в конфигурации")
            raise KeyError(f"Конфигурационный ключ '{key}' не найден")
        value = config[key]
        logger.info(f"Значение '{key}' = '{value}'")
        return value


def divide_numbers(a: float, b: float) -> float:
    """
    Делит два числа.
    Может вызвать ZeroDivisionError.
    """
    logger.debug(f"Деление: {a} / {b}")
    with log_errors("divide_numbers"):
        if b == 0:
            logger.error("Попытка деления на ноль!")
            raise ZeroDivisionError("Деление на ноль невозможно")
        result = a / b
        logger.info(f"Результат деления: {result}")
        return result


def process_data(data: list) -> list:
    """
    Обрабатывает список данных.
    Может вызвать IndexError при пустом списке.
    """
    logger.debug(f"Обработка данных: {len(data)} элементов")
    with log_errors("process_data"):
        if not data:
            logger.warning("Получен пустой список данных")
            raise IndexError("Нельзя обработать пустой список")
        # Имитация обработки
        result = [x * 2 for x in data]
        logger.info(f"Обработано успешно: {len(result)} элементов")
        return result


def run_demo():
    """Запуск демонстрации логирования ошибок."""
    logger.info("=" * 50)
    logger.info("=== ДЕМОНСТРАЦИЯ ЛОГИРОВАНИЯ ОШИБОК ===")
    logger.info("=" * 50)

    logger.info("\n--- Тест 1: Успешный парсинг ---")
    try:
        result = parse_number("42")
        logger.info(f"Результат: {result}")
    except Exception:
        pass

    logger.info("\n--- Тест 2: Ошибка парсинга (некорректное значение) ---")
    try:
        result = parse_number("не число")
    except Exception:
        pass

    logger.info("\n--- Тест 3: Работа с конфигурацией ---")
    config = {"host": "localhost", "port": 8080}
    try:
        host = read_config_value(config, "host")
        logger.info(f"Host: {host}")
    except Exception:
        pass

    logger.info("\n--- Тест 4: Отсутствующий ключ ---")
    try:
        missing = read_config_value(config, "missing_key")
    except Exception:
        pass

    logger.info("\n--- Тест 5: Успешное деление ---")
    try:
        result = divide_numbers(100, 4)
        logger.info(f"Результат: {result}")
    except Exception:
        pass

    logger.info("\n--- Тест 6: Деление на ноль ---")
    try:
        result = divide_numbers(100, 0)
    except Exception:
        pass

    logger.info("\n--- Тест 7: Обработка списка ---")
    try:
        result = process_data([1, 2, 3, 4, 5])
        logger.info(f"Результат: {result}")
    except Exception:
        pass

    logger.info("\n--- Тест 8: Пустой список ---")
    try:
        result = process_data([])
    except Exception:
        pass

    logger.info("\n")
    error_stats.print_summary()

    logger.info("\n=== Демонстрация завершена ===")


if __name__ == "__main__":
    run_demo()
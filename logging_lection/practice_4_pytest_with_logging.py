import logging
import pytest


class Calculator:
    """Простой калькулятор с логированием."""

    def __init__(self):
        self.logger = logging.getLogger("Calculator")

    def add(self, a: int, b: int) -> int:
        """Сложение двух чисел."""
        self.logger.debug(f"Выполняем сложение: {a} + {b}")
        result = a + b
        self.logger.info(f"Результат сложения: {result}")
        return result

    def divide(self, a: int, b: int) -> float:
        """Деление двух чисел."""
        self.logger.debug(f"Выполняем деление: {a} / {b}")
        if b == 0:
            self.logger.error("Попытка деления на ноль!")
            raise ValueError("Деление на ноль невозможно")
        result = a // b
        self.logger.info(f"Результат деления: {result}")
        return result


@pytest.fixture(autouse=True)
def setup_logging(caplog):
    """
    Fixture, который настраивает логгер перед каждым тестом.
    autouse=True означает, что fixture сработает автоматически.
    """
    # Настройка корневого логгера для вывода в консоль
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=logging.StreamHandler(),
        format='%(asctime)s [%(levelname)s] (%(name)s) %(message)s'
    )
    caplog.set_level(logging.DEBUG, logger="Calculator")
    # Yield вместо return - код после yield выполняется после теста (teardown)
    yield
    logging.getLogger("Calculator")


class TestCalculator:
    """Тесты для калькулятора с проверкой логов."""

    def test_add_success(self, caplog):
        """Тест успешного сложения с проверкой логов."""
        calc = Calculator()

        # Логирование начала теста
        logging.info("=== Тест: add_success ===")

        result = calc.add(2, 3)

        # Проверка результата
        assert result == 5

        # Проверка, что логи были записаны
        logging.debug(f"caplog: {caplog.text}")
        assert "Выполняем сложение: 2 + 3" in caplog.text
        assert "Результат сложения: 5" in caplog.text

        logging.info("Тест завершен успешно\n")

    def test_divide_success(self, caplog):
        """Тест успешного деления с проверкой логов."""
        calc = Calculator()

        logging.info("=== Тест: divide_success ===")

        result = calc.divide(10, 2)

        assert result == 5

        # Проверяем, что логи записались
        assert "Выполняем деление: 10 / 2" in caplog.text
        assert "Результат деления: 5" in caplog.text

        logging.info("Тест завершен успешно\n")

    def test_divide_by_zero(self, caplog):
        """Тест деления на ноль — должно быть логирование ошибки."""
        calc = Calculator()

        logging.info("=== Тест: divide_by_zero ===")

        # Проверяем, что бросается исключение
        with pytest.raises(ValueError):
            calc.divide(10, 0)

        # Проверяем, что ошибка была залогирована
        assert "Попытка деления на ноль!" in caplog.text
        assert "ERROR" in caplog.text

        logging.info("Тест завершен успешно (ошибка ожидаема)\n")

    def test_add_with_negative(self, caplog):
        """Тест сложения с отрицательными числами."""
        calc = Calculator()

        logging.info("=== Тест: add_with_negative ===")

        result = calc.add(-5, 3)

        assert result == -2

        # Проверяем логи
        assert "Выполняем сложение: -5 + 3" in caplog.text
        assert "Результат сложения: -2" in caplog.text

        logging.info("Тест завершен успешно\n")

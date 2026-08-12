import logging

def setup_logger(name="AutomationFramework"):
    """
    Инициализирует и возвращает настроенный логгер.
    Благодаря проверке `logger.handlers` избегаем дублирования логов при повторных вызовах.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        stream_formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(name)s) %(message)s')
        file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s::%(lineno)d:: %(message)s')

        # 1. Запись в файл
        file_handler = logging.FileHandler('automation_suite.log', encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # 2. Вывод в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(stream_formatter)
        logger.addHandler(console_handler)

    return logger
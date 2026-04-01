from contextlib import contextmanager
import time

@contextmanager
def timer_context(task_name: str = "Operation"):
    """Контекстный менеджер для замера времени выполнения кода"""
    print(f"Starting {task_name}...")
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        print(f"Finished {task_name}. Duration: {end_time - start_time:.4f} seconds")

# Пример использования класса
class Suppressor:
    """Подавляет исключения внутри блока with"""
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Если вернуть True, исключение не пойдет дальше
        return True 

if __name__ == "__main__":
    with timer_context("JSON Processing"):
        time.sleep(1) # Имитация работы

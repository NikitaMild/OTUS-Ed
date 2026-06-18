from contextlib import contextmanager
import time

@contextmanager
def timer_context(task_name: str = "Operation"):
    """Контекстный менеджер для замера времени выполнения кода"""
    print(f"Starting {task_name}...")
    start_time = time.time()
    try:
        print("step  one!")
        yield
        print("step three!")
    finally:
        end_time = time.time()
        print(f"Finished {task_name}. Duration: {end_time - start_time:.4f} seconds")
        print("step four!")


class FileOpener:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        print("1. [ENTER] Открываем файл...")
        self.file = open(self.filename, self.mode)
        return self.file  # Этот объект пойдет в переменную после "as"

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("3. [EXIT] Закрываем файл в любом случае!")
        self.file.close()

        if exc_type is not None:
            print(f"Замечена ошибка: {exc_type}. Но файл мы всё равно закрыли!")
        
        return True


if __name__ == "__main__":
    with timer_context("JSON Processing"):
        time.sleep(2) # Имитация работы
        print("step two!")
    print("step five!")

    with FileOpener("data/test.txt", "w") as f:
        print("2. [WITH] Пишем данные в файл...")
        f.write("Hello World")
        f.div()


print('foo')
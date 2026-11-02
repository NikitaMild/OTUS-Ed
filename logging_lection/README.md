# Логирование в автотестах (Python)

Практика к занятию по логгированию: модуль `logging`, иерархия логгеров,
сбор логов браузера и проверка логов в `pytest`.

## Структура

| Файл | Что показывает |
| --- | --- |
| `logger_config.py` | Фабрика логгера `setup_logger()`: файловый (`automation_suite.log`) + консольный обработчики, защита от дублирования обработчиков при повторных вызовах |
| `helper_page.py` | `BasePage` — пример page object с дочерним логгером `AutomationFramework.BasePage` (пишет в лог за счёт propagation) |
| `logging_driver.py` | Обёртки `LoggingWebDriver` / `LoggingWebElement`: `log_action` пишет `->` / `<-` / `!!!` вокруг действий, остальные вызовы делегируются |
| `practice_1_basic.py` | Практика 1: несколько модулей пишут в один общий файл лога |
| `practice_2_listener.py` | Практика 2: автоматическое логирование действий с браузером (без `EventFiringWebDriver`) |
| `practice_3_js_logs.py` | Практика 3: сбор логов JS-консоли браузера (`goog:loggingPrefs`) |
| `practice_4_pytest_with_logging.py` | Практика 4: проверка логов в тестах через `caplog` |
| `practice_5_error_handling_logs.py` | Практика 5: контекстный менеджер `log_errors` + `logger.exception` + статистика ошибок |
| `pytest.ini` | Конфигурация pytest: какие файлы собирать и как писать логи (консоль + `suite_4.log`) |
| `create_env.sh` | Создание `venv` и установка зависимостей из `requirements.txt` |
| `requirements.txt` | `selenium>=4.10.0`, `pytest>=7.0.0` |

## Подготовка окружения

```bash
cd logging_lection
bash create_env.sh
source venv/bin/activate
```

Требуется установленный **Google Chrome** — `selenium-manager` (входит в Selenium 4)
сам скачает подходящий драйвер при первом запуске.

## Запуск

Практики 1–3 (нужен браузер):

```bash
python practice_1_basic.py
python practice_2_listener.py
python practice_3_js_logs.py
```

Практика 4 (pytest):

```bash
pytest                                       # собирает practice_4 благодаря pytest.ini
pytest practice_4_pytest_with_logging.py     # то же самое, но явно
pytest -o log_cli=false                      # без живого вывода логов в консоль
```

Практика 5 (не требует браузера и pytest):

```bash
python practice_5_error_handling_logs.py
```

## Куда смотреть в логах

| Практика | Файл лога | На что обратить внимание |
| --- | --- | --- |
| 1 | `automation_suite.log` | записи `AutomationFramework` и `AutomationFramework.BasePage` в одном файле, у файловых записей есть `filename::lineno` |
| 2 | `automation_suite.log` | пары строк от логгера `AutomationFramework.Listener`: `-> клик по <a>` и `<- клик по <a>`, а при ошибке — одна строка `!!! клик по <a>: ElementClickInterceptedException: ...` |
| 3 | `automation_suite.log` | строки `[Browser JS SEVERE]` — ошибки из JS-консоли страницы |
| 4 | `suite_4.log` (+ консоль) | полный лог прогона pytest в формате `[LEVEL] (logger) file::lineno:: message` |
| 5 | `error_handling.log` (+ консоль) | `!!! ОШИБКА в контексте '...'` с полным stacktrace и итоговая «СТАТИСТИКА ОШИБОК» |

Логи `*.log` пока не добавлены в `.gitignore` — после прогонов они появляются
в `git status`. Если это мешает, добавьте в корневой `.gitignore` строку `*.log`.

## Практика 2: логирование через обёртку (вместо `EventFiringWebDriver`)

Изначально практика строилась на `EventFiringWebDriver` + `AbstractEventListener`
(хуки `before_click`, `after_click`, `on_exception`). С Selenium 4.11 этот API
deprecated, поэтому в `logging_driver.py` лежит своя маленькая обёртка:

* `log_action("...")` — контекстный менеджер: пишет `-> действие`, потом `<- действие`,
  а если внутри было исключение — одну строку `!!! действие: Тип: текст` и пробрасывает его дальше;
* `LoggingWebElement.click()` / `send_keys()` — по одной строке на метод (сам текст ввода
  не логируется: там бывают пароли);
* `LoggingWebDriver.get()` / `find_element()` / `find_elements()` — `find_element` ещё и
  заворачивает найденный элемент в `LoggingWebElement`, поэтому дальше всё логируется само;
* всё, что не перечислено, делегируется оригиналу через `__getattr__` (`title`,
  `execute_script`, `switch_to`, `get_attribute`, `is_displayed` ...) — без логов.

Главная мысль: логирование пишется **один раз в обёртке**, а не копипастится
`logger.info(...)` в каждый тест и каждый метод. Поэтому в методах обёртки
нет повторяющихся `try/except` — они схлопнуты в `log_action`.

### Что осталось за кадром и почему

В упрощённой версии сознательно выброшено (кому интересно — верните как задание):

* `describe(element)` — описание элемента с его текстом (`<a> (текст: 'Статья')`);
  сейчас в лог попадает только тег;
* `if TYPE_CHECKING:`-импорты selenium — были нужны только для аннотаций типов;
* `__repr__` обёрток — удобство отладки (`print(driver)`);
* `object.__getattribute__(self, "_element")` вместо `self._element` в `__getattr__` —
  защита от рекурсии, если атрибут запрашивают до `__init__`; в обычном коде не нужно.

## Задания для самостоятельной работы

1. **Ротация логов.** Замените в `logger_config.py` `FileHandler` на
   `RotatingFileHandler(maxBytes=1_000_000, backupCount=3)` и объясните,
   почему для CI-прогонов это важнее, чем один большой файл.
2. **Уровни логирования.** Добавьте в `BasePage` вызовы `logger.debug(...)`
   и покажите, что при `logger.setLevel(logging.INFO)` они не попадают в файл,
   а после понижения уровня — попадают.
3. **Логи браузера (практика 3).** Выведите в лог `entry['timestamp']` и
   добавьте сохранение всех WARNING-записей в отдельный файл.
4. **pytest + caplog (практика 4).** Добавьте тест, который проверяет не текст,
   а записи: `record.levelname == "ERROR"` и `record.name == "Calculator"`,
   а также используйте `caplog.at_level(...)` вместо `set_level`.
5. **Декоратор вместо контекстного менеджера (практика 5).** Напишите
   декоратор `log_errors(context)`, который логирует исключения функций так же,
   как `with log_errors(...)`, и сравните оба подхода.
6. **JSON-логи.** Настройте логирование через `logging.config.dictConfig`
   с собственным `Formatter`, выдающим JSON (`{"ts": ..., "level": ..., "logger": ..., "msg": ...}`)
   — так логи проще отправлять в ELK/Loki.
7. **Маскирование секретов.** Реализуйте `logging.Filter`, который заменяет
   пароли/токены в сообщениях на `***`, и подключите его к файловому обработчику.
8. **Текст элемента в логе (практика 2).** Верните в `logging_driver.py` функцию
   `describe(element)`, чтобы клик логировался как `-> клик по <a> (текст: 'Читать')`,
   и убедитесь, что для элемента без текста лог остаётся коротким.

## Известные ограничения

* Практики 1–3 требуют установленного Google Chrome; в окружении без браузера
  они падают на `webdriver.Chrome()` (это не ошибка логирования).
* `practice_1_basic.py` только печатает результат в лог, без `assert` —
  проверки появляются в практике 4.
* `logging.basicConfig(handlers=...)` принимает **список** обработчиков;
  передача одного объекта (`handlers=logging.StreamHandler()`) даёт `TypeError`.
  В `practice_4` конфигурация логирования целиком вынесена в `pytest.ini`.
* `practice_5_error_handling_logs.py` не отключает `propagate`, поэтому
  ERROR-записи дополнительно попадают в `lastResort`-обработчик (stderr).


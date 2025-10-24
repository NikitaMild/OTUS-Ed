import pytest
import allure

@allure.step("Выполняем подготовку данных")
def prepare_data():
    return {"user_id": 123, "name": "John"}

@allure.step("Выполняем проверку {expected} == {actual}")
def check_equal(expected, actual):
    assert expected == actual

def test_with_steps():
    """Тест с использованием шагов"""
    with allure.step("Подготавливаем данные"):
        data = prepare_data()
    
    with allure.step("Проверяем ID пользователя"):
        check_equal(123, data["user_id"])
    
    with allure.step("Проверяем имя пользователя"):
        check_equal("John", data["name"])
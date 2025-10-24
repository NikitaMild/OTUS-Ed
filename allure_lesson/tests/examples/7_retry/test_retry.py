# test_allure_features.py
import pytest
import allure
import time
import random


@pytest.mark.flaky(reruns=3, reruns_delay=1)
def test_flaky_test():
    """Тест с повторными попытками"""
    with allure.step("Пытаемся выполнить операцию"):
        time.sleep(1)
        # Случайный провал для демонстрации
        assert random.choice([0,1]), "Случайный провал для демонстрации flaky"


@pytest.mark.smoke
def test_smoke_test():
    """Smoke тест"""
    with allure.step("Выполняем smoke тест"):
        assert True


@allure.feature("Авторизация")
@allure.story("Пользователь может войти")
def test_user_authentication():
    """Тест авторизации"""
    with allure.step("Подготавливаем данные"):
        user_data = {"username": "testuser", "password": "password"}
    
    with allure.step("Выполняем вход"):
        # Симуляция входа
        login_success = True
    
    with allure.step("Проверяем результат"):
        assert login_success
        allure.attach(str(user_data), "user_data.json", allure.attachment_type.JSON)
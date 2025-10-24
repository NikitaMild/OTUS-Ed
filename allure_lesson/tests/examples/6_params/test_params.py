# test_parametrized.py
import pytest
import allure

@pytest.mark.parametrize("username,password,expected", [
    ("admin", "password123", True),
    ("user", "userpass", True),
    ("invalid", "wrong", False),
])
def test_user_login_parametrized(username, password, expected):
    """Параметризованный тест входа"""
    with allure.step(f"Пытаемся войти как {username}"):
        login_result = username == "admin" and password == "password123"
        
    with allure.step(f"Проверяем результат входа: {login_result}"):
        assert login_result == expected

@pytest.mark.parametrize("data", [
    {"name": "John", "age": 30},
    {"name": "Jane", "age": 25},
    {"name": "Bob", "age": 35},
])
def test_user_data_validation(data):
    """Тест валидации пользовательских данных"""
    with allure.step(f"Проверяем данные пользователя: {data['name']}"):
        assert data["name"] is not None
        assert data["age"] > 0
import pytest
import allure

@allure.issue("ISSUE-123", "Баг в авторизации")
@allure.testcase("TC-456", "Тест-кейс авторизации")
@allure.suite("Авторизация")
@allure.sub_suite("Пользовательские сценарии")
def test_user_login():
    """Тест авторизации пользователя"""
    assert True

@allure.link("https://example.com/docs/login", name="Документация")
@allure.link("https://jira.example.com/browse/BUG-789", name="JIRA")
def test_with_external_links():
    """Тест с внешними ссылками"""
    assert True

@allure.epic("Платформа")
@allure.feature("Авторизация")
@allure.story("Пользователь может войти в систему")
def test_user_authentication_flow():
    """Тестовый сценарий авторизации"""
    assert True
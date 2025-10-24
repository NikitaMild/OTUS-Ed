import pytest
import allure

@allure.tag("smoke")
@allure.severity(allure.severity_level.BLOCKER)
def test_blocker_issue():
    """Критический баг"""
    assert True

@allure.tag("regression")
@allure.severity(allure.severity_level.NORMAL)
def test_regression_case():
    """Регрессионный тест"""
    assert 1 + 1 == 2

@allure.tag("functional")
@allure.severity(allure.severity_level.MINOR)
@allure.description("Этот тест проверяет основную функциональность")
def test_functional_case():
    """Функциональный тест"""
    result = len("Hello World")
    assert result == 11
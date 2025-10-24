import pytest


def test_simple_assertion():
    """Простой тест с assertion"""
    assert 1 == 1


def test_string_comparison():
    """Тест сравнения строк"""
    expected = "Hello World"
    actual = "Hello World"
    assert expected == actual

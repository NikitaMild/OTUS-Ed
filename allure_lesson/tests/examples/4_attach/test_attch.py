import pytest
import allure
import json
import csv

def test_with_json_attachment():
    """Тест с JSON вложением"""
    data = {"user": "john", "status": "active", "id": 123}
    
    with allure.step("Создаем JSON данные"):
        json_data = json.dumps(data, indent=2)
    
    with allure.step("Добавляем JSON вложение"):
        allure.attach(json_data, "user_data.json", allure.attachment_type.JSON)
    
    assert data["status"] == "active"

def test_with_text_attachment():
    """Тест с текстовым вложением"""
    log_content = """
    INFO: Starting test
    DEBUG: User logged in
    WARNING: Low memory
    ERROR: Database connection failed
    """
    
    allure.attach(log_content, "test_log.txt", allure.attachment_type.TEXT)
    assert True

def test_with_image_attachment():
    """Тест с изображением"""
    # Создаем простой текстовый "картинку" для демонстрации
    image_data = "Png image data (simulated)"
    allure.attach(image_data, "sample.png", allure.attachment_type.PNG)
    assert True
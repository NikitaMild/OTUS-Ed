import pytest
import allure
import random

class TestUserManagement:
    """Класс тестов управления пользователями"""
    
    @allure.feature("Управление пользователями")
    @allure.story("Создание нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_success(self):
        """Успешное создание пользователя"""
        user_data = {
            "username": f"user_{random.randint(1000, 9999)}",
            "email": f"user{random.randint(1000, 9999)}@example.com"
        }
        
        with allure.step("Подготавливаем данные пользователя"):
            allure.attach(str(user_data), "user_data.json", allure.attachment_type.JSON)
        
        with allure.step("Создаем пользователя"):
            # Симуляция создания пользователя
            created_user = user_data.copy()
            created_user["id"] = random.randint(10000, 99999)
            
        with allure.step("Проверяем создание пользователя"):
            assert created_user["id"] is not None
            assert created_user["username"] is not None
            
        allure.attach(f"Пользователь {created_user['username']} успешно создан", 
                     "result.txt", allure.attachment_type.TEXT)

    @allure.feature("Управление пользователями")
    @allure.story("Поиск пользователя")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_user_by_username(self):
        """Поиск пользователя по имени"""
        search_term = "john"
        
        with allure.step(f"Ищем пользователя: {search_term}"):
            # Симуляция поиска
            results = [{"id": 1, "name": "John Doe"}, {"id": 2, "name": "Johnny"}]
            
        with allure.step("Проверяем результаты поиска"):
            assert len(results) > 0
            assert any(search_term.lower() in user["name"].lower() for user in results)
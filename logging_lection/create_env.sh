#!/usr/bin/env bash

set -e

echo "=== [Linux] Настройка окружения для занятия по логгированию ==="

# 1. Проверка наличия Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ [ОШИБКА] Python 3 не установлен. Установите его командой:"
    echo "    sudo apt update && sudo apt install -y python3 python3-venv python3-pip"
    exit 1
fi

# 2. Создание виртуального окружения venv
if [ ! -d "venv" ]; then
    echo "⚙️  Создание виртуального окружения (venv)..."
    python3 -m venv venv
else
    echo "ℹ️  Виртуальное окружение venv уже существует."
fi

# 3. Активация окружения и установка зависимостей
echo "🔄 Активация venv и обновление пип/зависимостей..."
source venv/bin/activate

pip install --upgrade pip -q
pip install -r requirements.txt -q

echo "✅ Все зависимости успешно установлены!"
echo "--------------------------------------------------"
echo "💡 Чтобы активировать окружение вручную в терминале, выполните:"
echo "   source venv/bin/activate"
echo "--------------------------------------------------"
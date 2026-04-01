import json
from pathlib import Path
from typing import Union

BASE_DIR = Path(__file__).resolve().parent.parent

def read_json(filename: str) -> Union[list, dict]:
    """Читает JSON файл и возвращает данные"""
    file_path = BASE_DIR / "data" / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_json(filename: str, data: Union[list, dict]) -> None:
    """Записывает данные в JSON файл"""
    file_path = BASE_DIR / "data" / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    data = read_json("users.json")
    print(f"Loaded {len(data)} users from JSON")
    for user in data:
        print("Read user information:\n")
        for key, value in user.items():
            print(f"{key}: {value}")
import csv
from pathlib import Path
from typing import List, Dict

BASE_DIR = Path(__file__).resolve().parent.parent

def read_csv(filename: str) -> List[Dict]:
    """Читает CSV как список словарей"""
    file_path = BASE_DIR / "data" / filename
    with open(file_path, 'r', encoding='utf-8', newline='\n') as f:
        reader = csv.DictReader(f)
        return list(reader) 

def write_csv(filename: str, data: List[Dict], fieldnames: List[str], method='w', write_headers=True) -> None:
    """Записывает список словарей в CSV"""
    file_path = BASE_DIR / "data" / filename
    with open(file_path, method, encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_headers:
            writer.writeheader()
        writer.writerows(data)

if __name__ == "__main__":
    data = read_csv("users.csv")
    print(f"Loaded {len(data)} users from CSV")
    print("Read user information:")
    for user in data:
        for key, value in user.items():
            print(f"{key}: {value}")
        print("\n")

    write_csv("users_update.csv", 
              data=[{"id": 7, "name": "Nikita", "email": "nikita@example.com", "is_active": True}],
              fieldnames=["id", "name", "email", "is_active"],
              method='w',
              write_headers=True
            )

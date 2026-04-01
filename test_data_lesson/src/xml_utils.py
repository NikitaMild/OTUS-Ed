import xml.etree.ElementTree as ET
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

def read_xml(filename: str) -> ET.Element:
    """Читает XML файл и возвращает корневой элемент"""
    file_path = BASE_DIR / "data" / filename
    tree = ET.parse(file_path)
    return tree.getroot()

def write_xml(filename: str, root: ET.Element) -> None:
    """Записывает объект ElementTree в файл с отступами"""
    file_path = BASE_DIR / "data" / filename
    tree = ET.ElementTree(root)

    tree.write(file_path, encoding='utf-8', xml_declaration=True)
    print(f"Сделали новый XML файл по пути: {file_path}")


def get_element_from_xml(filename: str, element: str) -> str:
    """Читает XML файл и берет возвращает элемент из дерева."""
    file_path = BASE_DIR / "data" / filename
    tree = ET.parse(file_path)
    root = tree.getroot()
    return root.find(element).text


if __name__ == "__main__":
    # Пример использования
    root = read_xml("config.xml")

    # Пример доступа к данным:
    app_name = root.find('app').get('name')
    db_host = root.find('database/host').text

    print(f"App: {app_name}, DB Host: {db_host}")

    # Пример изменения:
    old_version = root.find('app/version').text

    root.find('app/version').text = "1.1"

    new_version = root.find('app/version').text

    print(f"Обновили версию приложения с {old_version} на {new_version}")

    write_xml("config_updated.xml", root)

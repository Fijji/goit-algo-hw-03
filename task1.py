import sys
from pathlib import Path
import shutil

COLOR_BLUE_DIR = "\033[94m"
COLOR_YELLOW_FILES = "\033[93m"
COLOR_RESET = "\033[0m"

# Є написана функція display_tree, яка приймає шлях до директорії як аргумент.
def display_tree(path: Path, output_dir: Path, indent: str = "", prefix: str = "") -> None:
    # Код має обробку винятків за допомогою конструкції try-except, що дозволяє правильно обробляти помилки доступу до файлів або директорій.
    try:
        if path.is_dir():
            print(indent + prefix + COLOR_BLUE_DIR + str(path.name) + COLOR_RESET)
            indent += "    " if prefix else ""
            children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name))

            for index, child in enumerate(children):
                is_last = index == len(children) - 1
                # Рекурсивне читання директорій
                display_tree(child, output_dir, indent + ("" if is_last else "│   "), "└── " if is_last else "├── ")
        else:
            extension = path.suffix[1:].lower()
            dest_dir = output_dir / extension
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Копіювання файлів
            shutil.copy2(str(path), str(dest_dir))
            print(indent + prefix + COLOR_YELLOW_FILES + str(path.name) + COLOR_RESET)
    except Exception as e:
        print(f"Помилка файлу '{path.name}': {e}")
        print("Перевірте правильність виклику програми:")
        print("python task1.py <source_dir> [<destination_dir>]")

def display_directory_structure(source_dir: Path, destination_dir: Path):
    print(f"Копіювання файлів з {source_dir} в {destination_dir}:")
    display_tree(source_dir, destination_dir)

if __name__ == "__main__":
    try:
        # Отримання шляху до вихідної директорії та директорії призначення з аргументів командного рядка
        if len(sys.argv) < 2:
            raise ValueError("Не вказано вихідну директорію")

        source_dir = Path(sys.argv[1])
        destination_dir = Path("dist") if len(sys.argv) < 3 else Path(sys.argv[2])
        # Виклик функції для обробки дерева
        display_directory_structure(source_dir, destination_dir)
    except Exception as e:
        print(f"Помилка: {e}")
        print("Перевірте правильність виклику програми:")
        print("python task1.py <source_dir> [<destination_dir>]")
import os
import json
import datetime

def get_path() -> None:
    current_directory = os.getcwd()
    print(f'Текущий рабочий каталог: {current_directory}')
    new_directory = input('Введите новый каталог или оставьте пустым для текущего: ')
    if new_directory:
        os.chdir(new_directory)
        print(f'Новый рабочий каталог: {os.getcwd()}')

def create_directory_and_file() -> None:
    notes_directory = "Записки"
    if not os.path.exists(notes_directory):
        os.makedirs(notes_directory)
        print(f'Папка "{notes_directory}" создана')
    os.chdir(notes_directory)
    file_path = "data.txt"
    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            print(f'Файл "{file_path}" создан в папке "{notes_directory}"')
        initial_balance = int(input("Введите ваш остаток денег: "))
        with open(file_path, 'a', encoding='utf-8') as file:
            file.write(json.dumps({"Остаток денег": initial_balance}, ensure_ascii=False) + "\n")
        print("Остаток денег успешно записан в файл.")
    print("Файл готов к работе!")

def get_current_balance() -> int:
    with open("data.txt", "r", encoding='utf-8') as file:
        first_line = file.readline()
        current_balance_data = json.loads(first_line)
        return current_balance_data["Остаток денег"]

def update_balance(category: str, amount: int, current_balance: int) -> int:
    if category == "доход":
        current_balance += amount
    elif category == "расход":
        current_balance -= amount
    return current_balance

def is_valid_date(date_str: str) -> bool:
    try:
        date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        return date.year >= 2024
    except ValueError:
        return False

def is_valid_category(category: str) -> bool:
    return category.lower() in ["доход", "расход"]

def is_valid_amount(amount: str) -> bool:
    return amount.isdigit() and int(amount) > 0

def add_entry() -> None:
    while True:
        date = input("\nВведите дату (ГГГГ-ММ-ДД): ")
        if is_valid_date(date):
            break
        else:
            print("Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД (год 2024 и позже).")
    while True:
        category = input("Введите категорию (Доход/Расход): ")
        if is_valid_category(category):
            break
        else:
            print("Некорректная категория. Пожалуйста, введите 'Доход' или 'Расход'.")
    while True:
        amount = input("Введите сумму: ")
        if is_valid_amount(amount):
            break
        else:
            print("Некорректная сумма. Пожалуйста, введите положительное целое число.")
    description = input("Введите описание: ")
    current_balance = get_current_balance()
    new_balance = update_balance(category, int(amount), current_balance)
    new_entry = {
        "дата": date,
        "категория": category,
        "сумма": int(amount),
        "описание": description
    }
    with open("data.txt", "r+", encoding='utf-8') as file:
        lines = file.readlines()
        lines[0] = json.dumps({"Остаток денег": new_balance}, ensure_ascii=False) + "\n"
        file.seek(0)
        file.writelines(lines)
        file.write(json.dumps(new_entry, ensure_ascii=False) + "\n")

def search_entries() -> None:
    while True:
        search_field = input("Поиск по (дата, категория, сумма): ").lower()
        if search_field not in ["дата", "категория", "сумма"]:
            print("Некорректное поле для поиска. Пожалуйста, выберите из 'дата', 'категория' или 'сумма'.")
        else:
            break
    search_value = input("Введите значение для поиска: ").lower()
    with open("data.txt", "r", encoding='utf-8') as file:
        entries = file.readlines()[1:]
    found_entries = []
    for index, entry in enumerate(entries):
        data = json.loads(entry)
        if str(data.get(search_field, "")).lower() == search_value:
            found_entries.append((index + 1, data))
    if not found_entries:
        print("Записи не найдены.")
        return
    else:
        for idx, entry in found_entries:
            print(f"ID: {idx}, Запись: {entry}")

def update_entry() -> None:
    search_entries()
    entry_id = int(input("Введите ID записи для изменения: "))
    with open("data.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
        if entry_id >= len(lines):
            print("Записи с указанным ID не существует.")
            return
        new_date = input("Введите новую дату (ГГГГ-ММ-ДД): ")
        if not is_valid_date(new_date):
            print("Некорректный формат даты. Пожалуйста, введите дату в формате ГГГГ-ММ-ДД (год 2024 и позже).")
            return
        new_category = input("Введите новую категорию (Доход/Расход): ").lower()
        if not is_valid_category(new_category):
            print("Некорректная категория. Пожалуйста, введите 'Доход' или 'Расход'.")
            return
        new_amount = input("Введите новую сумму: ")
        if not is_valid_amount(new_amount):
            print("Некорректная сумма. Пожалуйста, введите положительное целое число.")
            return
        new_amount = int(new_amount)
        new_description = input("Введите новое описание: ")
        current_balance = json.loads(lines[0])["Остаток денег"]
        old_entry = json.loads(lines[entry_id])
        if old_entry["категория"] == "доход":
            current_balance -= old_entry["сумма"]
        elif old_entry["категория"] == "расход":
            current_balance += old_entry["сумма"]
        if new_category == "доход":
            current_balance += new_amount
        elif new_category == "расход":
            current_balance -= new_amount
        new_entry = {
            "дата": new_date,
            "категория": new_category,
            "сумма": new_amount,
            "описание": new_description
        }
        lines[0] = json.dumps({"Остаток денег": current_balance}) + "\n"
        lines[entry_id] = json.dumps(new_entry, ensure_ascii=False) + "\n"
    with open("data.txt", "w", encoding='utf-8') as file:
        file.writelines(lines)

def calculate_finances() -> None:
    if not os.path.exists("data.txt") or os.path.getsize("data.txt") == 0:
        print("Нет записей. Добавьте данные.")
        return
    with open("data.txt", "r", encoding='utf-8') as file:
        lines = file.readlines()
    if not lines:
        print("Файл пуст.")
        return
    try:
        data = json.loads(lines[0].strip())
        current_balance = data["Остаток денег"]
        print(f"\nТекущий баланс: {current_balance}")
    except (ValueError, KeyError) as e:
        print(f"Ошибка при чтении данных: {e}")
        return
    total_expenses = 0.0
    total_income = 0.0
    for line in lines[1:]:
        try:
            data = json.loads(line)
            amount = float(data["сумма"])
            if data.get("категория") == "расход":
                total_expenses += amount
            elif data.get("категория") == "доход":
                total_income += amount
        except (json.JSONDecodeError, ValueError):
            print("Ошибка чтения данных из строки:", line)
            continue
    print(f"Сумма расходов: {total_expenses:.2f}")
    print(f"Сумма доходов: {total_income:.2f}\n")

def main_menu() -> None:
    while True:
        print()
        print("1. Баланс")
        print("2. Добавить запись")
        print("3. Изменить рабочий каталог")
        print("4. Найти сведения")
        print("5. Изменить сведения")
        print("6. Выход")
        choice = input("Выберите действие: ")
        if choice == "1":
            calculate_finances()
        elif choice == "2":
            add_entry()
        elif choice == "3":
            get_path()
            create_directory_and_file()
        elif choice == "4":
            search_entries()
        elif choice == "5":
            update_entry()
        elif choice == "6":
            break
        else:
            print("Пожалуйста, введите корректный номер действия.")


if __name__ == "__main__":
    create_directory_and_file()
    main_menu()

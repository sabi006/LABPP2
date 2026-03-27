import psycopg2
import csv
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"]
    )

# Создание таблицы
def create_table():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(20) UNIQUE
        );
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table 'phonebook' is ready.")

# Добавление контакта
def add_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO phonebook (name, phone)
        VALUES (%s, %s)
        ON CONFLICT (phone) DO NOTHING;
    """, (name, phone))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Added contact: {name} - {phone}")

# Показ всех контактов
def show_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    for row in rows:
        print(row)

# Обновление контакта
def update_contact(name, phone):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE phonebook
        SET phone=%s
        WHERE name=%s;
    """, (phone, name))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Updated {name} with new phone: {phone}")

# Удаление контакта
def delete_contact(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM phonebook WHERE name=%s;", (name,))
    conn.commit()
    cur.close()
    conn.close()
    print(f"Deleted contact: {name}")

# Поиск контакта
def find_contact(name):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook WHERE name=%s;", (name,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    if rows:
        for row in rows:
            print(row)
    else:
        print(f"No contact found with name: {name}")

# Импорт из CSV
def import_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(row['name'], row['phone'])
    print(f"Contacts from {csv_file} imported successfully.")

# Меню
def menu():
    while True:
        print("\n1. Добавить контакт")
        print("2. Показать все контакты")
        print("3. Обновить контакт")
        print("4. Удалить контакт")
        print("5. Найти контакт")
        print("6. Импорт из CSV")
        print("0. Выход")
        choice = input("Выбор: ")

        if choice == "1":
            name = input("Имя: ")
            phone = input("Телефон: ")
            add_contact(name, phone)
        elif choice == "2":
            show_contacts()
        elif choice == "3":
            name = input("Имя контакта для обновления: ")
            phone = input("Новый телефон: ")
            update_contact(name, phone)
        elif choice == "4":
            name = input("Имя контакта для удаления: ")
            delete_contact(name)
        elif choice == "5":
            name = input("Имя для поиска: ")
            find_contact(name)
        elif choice == "6":
            csv_file = input("Путь к CSV файлу: ")
            import_csv(csv_file)
        elif choice == "0":
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор, попробуйте снова.")

# Основной запуск
if __name__ == "__main__":
    create_table()
    menu()
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

#  Загрузка контактов из CSV 
def load_from_csv(csv_file):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            add_contact(row['name'], row['phone'])

#  Показ всех контактов
def show_contacts():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# Основной запуск
if __name__ == "__main__":
    create_table()
    load_from_csv("contacts.csv")
    print("Current contacts in database:")
    for r in show_contacts():
        print(r)
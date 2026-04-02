from connect import connect

def search_contacts():
    pattern = input("Enter search pattern: ")
    conn = connect()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_contacts_by_pattern(%s);", (pattern,))
        rows = cur.fetchall()

        if not rows:
            print("No contacts found.")
        else:
            for row in rows:
                print(f"Name: {row[0]}, Phone: {row[1]}")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def add_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("CALL upsert_contact(%s, %s);", (name, phone))
        conn.commit()
        print("Contact added/updated successfully.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def delete_contact():
    name = input("Enter name (or leave empty): ")
    phone = input("Enter phone (or leave empty): ")

    name = name if name else None
    phone = phone if phone else None

    conn = connect()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("CALL delete_contact(%s, %s);", (name, phone))
        conn.commit()
        print("Contact deleted.")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def paginate_contacts():
    limit = int(input("Enter limit: "))
    offset = int(input("Enter offset: "))

    conn = connect()
    if not conn:
        return

    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s);", (limit, offset))
        rows = cur.fetchall()

        if not rows:
            print("No contacts found.")
        else:
            for row in rows:
                print(f"Name: {row[0]}, Phone: {row[1]}")
    except Exception as e:
        print("Error:", e)
    finally:
        cur.close()
        conn.close()


def main():
    while True:
        print("\n--- PHONEBOOK ---")
        print("1. Search")
        print("2. Add/Update contact")
        print("3. Delete contact")
        print("4. Show with pagination")
        print("0. Exit")

        choice = input("Choose: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            delete_contact()
        elif choice == "4":
            paginate_contacts()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()
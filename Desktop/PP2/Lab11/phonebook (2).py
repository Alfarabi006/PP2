import psycopg2
import csv

# Подключение к базе данных
conn = psycopg2.connect(
    database="postgres",                   
    user="omar",             
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Создание таблицы
def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()

# Вставка данных из CSV
def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # пропустить заголовок
        for row in reader:
            full_name = row[0].strip() + " " + row[1].strip()
            phone = row[2].strip()
            cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (full_name, phone))
    conn.commit()

# Вставка данных вручную
def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone: ")
    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()

# Обновление данных
def update_data():
    id_to_update = input("Enter ID to update: ")
    new_username = input("Enter new username (leave blank to keep current): ")
    new_phone = input("Enter new phone number (leave blank to keep current): ")

    if new_username:
        cur.execute("UPDATE phonebook SET username = %s WHERE id = %s", (new_username, id_to_update))
    if new_phone:
        cur.execute("UPDATE phonebook SET phone = %s WHERE id = %s", (new_phone, id_to_update))
    
    conn.commit()

# Запрос данных
def query_data():
    choice = input("Search by (1) username or (2) phone? ")
    if choice == '1':
        username = input("Enter username: ")
        cur.execute("SELECT * FROM phonebook WHERE username = %s", (username,))
    else:
        phone = input("Enter phone: ")
        cur.execute("SELECT * FROM phonebook WHERE phone = %s", (phone,))
    results = cur.fetchall()
    for row in results:
        print(row)

# Удаление данных
def delete_data():
    choice = input("Delete by (1) username or (2) ID? ")
    if choice == '1':
        username = input("Enter username to delete: ")
        cur.execute("DELETE FROM phonebook WHERE username = %s", (username,))
    elif choice == '2':
        id_to_delete = input("Enter ID to delete: ")
        cur.execute("DELETE FROM phonebook WHERE id = %s", (id_to_delete,))
    else:
        print("Invalid option.")
        return
    conn.commit()

def check_table():
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    for row in rows:
        print(row)

check_table()

def export_to_csv(filename):
    cur.execute("SELECT * FROM phonebook")
    rows = cur.fetchall()
    
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'username', 'phone'])  # заголовки
        writer.writerows(rows)

    print(f" Data exported to: {filename}")

# Главное меню
def main():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Phone")
        print("4. Query Data")
        print("5. Delete User")
        print("6. Exit")
        print("7. Show All Table")
        print("8. Export to CSV")
        choice = input("Choose an option: ")

        if choice == '1':
            insert_from_csv('/Users/sarsenbaisarbinaz/Desktop/pp2/githowto/repositories/w3school/lab 10/students.csv')
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_data()
        elif choice == '4':
            query_data()
        elif choice == '5':
            delete_data()
        elif choice == '6':
            break
        elif choice == '7':
            check_table()
        elif choice == '8':
            filename = input("Enter filename to save (e.g., phonebook_export.csv): ")
            export_to_csv(filename)
        else:
            print("Invalid option. Try again.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
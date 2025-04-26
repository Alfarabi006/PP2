import psycopg2

conn = psycopg2.connect(
    database="postgres",
    user="Omar",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def search_by_pattern():
    pattern = input("Enter search pattern (name or phone): ")
    cur.execute("SELECT * FROM search_pattern(%s)", (pattern,))
    results = cur.fetchall()
    for row in results:
        print(row)

def insert_or_update_user():
    name = input("Enter username: ")
    phone = input("Enter phone number: ")
    cur.execute("CALL insert_or_update_user(%s, %s)", (name, phone))
    conn.commit()

def insert_many_users():
    names = []
    phones = []
    n = int(input("How many users do you want to insert? "))
    for _ in range(n):
        name = input("Name: ")
        phone = input("Phone: ")
        names.append(name)
        phones.append(phone)
    cur.execute("CALL insert_many_users(%s, %s)", (names, phones))
    conn.commit()
    print("Users inserted (invalid ones are skipped).")

def paginate_users():
    limit = int(input("Enter number of records to display: "))
    offset = int(input("Enter offset: "))
    cur.execute("SELECT * FROM paginate_users(%s, %s)", (limit, offset))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_user():
    value = input("Enter username or phone to delete: ").strip()
    cur.execute("CALL delete_user(%s::TEXT)", (value,))
    conn.commit()
    print("User deleted.")

def main():
    while True:
        print("\n=== PhoneBook Menu ===")
        print("1. Search by pattern")
        print("2. Insert or update user")
        print("3. Insert many users")
        print("4. Show paginated users")
        print("5. Delete user")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            search_by_pattern()
        elif choice == '2':
            insert_or_update_user()
        elif choice == '3':
            insert_many_users()
        elif choice == '4':
            paginate_users()
        elif choice == '5':
            delete_user()
        elif choice == '6':
            break
        else:
            print("Invalid option. Try again.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
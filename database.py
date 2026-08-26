import sqlite3

# Connect to the database
connection = sqlite3.connect("business.db")

cursor = connection.cursor()

# Create customers table if it doesn't already exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    city TEXT
)
""")

# Keep the program running until the user chooses Exit
while True:

    print("\nCustomer Management System")
    print("1. Add customer")
    print("2. Search customer")
    print("3. View all customers")
    print("4. Update customer")
    print("5. Delete customer")
    print("6. Exit")

    choice = input("Choose an option: ")

    # -------------------------
    # 1. ADD CUSTOMER
    # -------------------------
      
    if choice == "1":
        name = input("Enter customer name: ").strip()
        email = input("Enter customer email: ").strip()
        city = input("Enter customer city: ").strip()

        if name == "":
            print("Name cannot be blank.")

        elif email == "":
            print("Email cannot be blank.")

        elif city == "":
            print("City cannot be blank.")

        else:
            cursor.execute("""
            INSERT INTO customers (name, email, city)
            VALUES (?, ?, ?)
            """, (name, email, city))

            connection.commit()

            print("Customer added successfully!")
    # -------------------------
    # 2. SEARCH CUSTOMER
    # -------------------------
       
    elif choice == "2":
        name = input("Enter customer name: ").strip()

        if name == "":
            print("Name cannot be blank.")

        else:
            cursor.execute("""
            SELECT id, name, email, city
            FROM customers
            WHERE name = ?
            """, (name,))

            customers = cursor.fetchall()

            if customers:
                for customer in customers:
                    print("ID:", customer[0])
                    print("Name:", customer[1])
                    print("Email:", customer[2])
                    print("City:", customer[3])
                    print("--------------------")
            else:
                print("No customers found.")
    # -------------------------
    # 3. VIEW ALL CUSTOMERS
    # -------------------------
    elif choice == "3":   

        cursor.execute("""
        SELECT id, name, email, city
        FROM customers
        ORDER BY name
        """)

        customers = cursor.fetchall()

        if customers:
            for customer in customers:
                  print("ID:", customer[0])
                  print("Name:", customer[1])
                  print("Email:", customer[2])
                  print("City:", customer[3])
                  print("--------------------")

        else:
            print("No customers found.")

    # -------------------------
    # 4. UPDATE CUSTOMER
    # -------------------------
       
    elif choice == "4":
        customer_id = input("Enter customer ID: ")

        name = input("Enter new name: ").strip()
        email = input("Enter new email: ").strip()
        city = input("Enter new city: ").strip()

        if name == "":
            print("Name cannot be blank.")

        elif email == "":
            print("Email cannot be blank.")

        elif city == "":
            print("City cannot be blank.")

        else:
            cursor.execute("""
            UPDATE customers
            SET name = ?, email = ?, city = ?
            WHERE id = ?
            """, (name, email, city, customer_id))

            connection.commit()

            if cursor.rowcount > 0:
                print("Customer updated successfully!")
            else:
                print("Customer ID not found.")
    # -------------------------
    # 5. DELETE CUSTOMER
    # -------------------------

    elif choice == "5":
        customer_id = input("Enter customer ID to delete: ")

        cursor.execute("""
        SELECT id, name, email, city
        FROM customers
        WHERE id = ?
        """, (customer_id,))

        customer = cursor.fetchone()

        if customer:
            print("\nCustomer found:")
            print("ID:", customer[0])
            print("Name:", customer[1])
            print("Email:", customer[2])
            print("City:", customer[3])

            confirm = input("Delete this customer? (y/n): ").strip().lower()

            if confirm == "y":
                cursor.execute("""
                DELETE FROM customers
                WHERE id = ?
                """, (customer_id,))

                connection.commit()

                print("Customer deleted successfully!")

            else:
                print("Delete cancelled.")

        else:
            print("Customer ID not found.")

    # -------------------------
    # 6. EXIT
    # -------------------------
    elif choice == "6":

        print("Goodbye!")
        break

    # -------------------------
    # INVALID MENU OPTION
    # -------------------------
    else:

        print("Invalid option.")

# Close database after leaving the loop
connection.close()
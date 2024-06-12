import sqlite3

# Connect to the database
conn = sqlite3.connect("ice_cream_parlor.db")
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS flavors (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        season TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY,
        name TEXT,
        quantity INTEGER
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS allergens (
        id INTEGER PRIMARY KEY,
        name TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS flavor_ingredients (
        flavor_id INTEGER,
        ingredient_id INTEGER,
        FOREIGN KEY (flavor_id) REFERENCES flavors (id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_suggestions (
        id INTEGER PRIMARY KEY,
        customer_name TEXT,
        flavor_name TEXT,
        description TEXT
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer_allergens (
        customer_name TEXT,
        allergen_id INTEGER,
        FOREIGN KEY (allergen_id) REFERENCES allergens (id)
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS carts (
        customer_name TEXT,
        flavor_id INTEGER,
        FOREIGN KEY (flavor_id) REFERENCES flavors (id)
    );
""")

# Commit the changes
conn.commit()

# Define functions to interact with the database
def add_flavor(name, description, season):
    cursor.execute("INSERT INTO flavors (name, description, season) VALUES (?,?,?)", (name, description, season))
    conn.commit()

def add_ingredient(name, quantity):
    cursor.execute("INSERT INTO ingredients (name, quantity) VALUES (?,?)", (name, quantity))
    conn.commit()

def add_allergen(name):
    cursor.execute("INSERT INTO allergens (name) VALUES (?)", (name,))
    conn.commit()

def add_flavor_ingredient(flavor_id, ingredient_id):
    cursor.execute("INSERT INTO flavor_ingredients (flavor_id, ingredient_id) VALUES (?,?)", (flavor_id, ingredient_id))
    conn.commit()

def add_customer_suggestion(customer_name, flavor_name, description):
    cursor.execute("INSERT INTO customer_suggestions (customer_name, flavor_name, description) VALUES (?,?,?)", (customer_name, flavor_name, description))
    conn.commit()

def add_customer_allergen(customer_name, allergen_id):
    cursor.execute("INSERT INTO customer_allergens (customer_name, allergen_id) VALUES (?,?)", (customer_name, allergen_id))
    conn.commit()

def add_to_cart(customer_name, flavor_id):
    cursor.execute("INSERT INTO carts (customer_name, flavor_id) VALUES (?,?)", (customer_name, flavor_id))
    conn.commit()

def search_flavors(name):
    cursor.execute("SELECT * FROM flavors WHERE name LIKE?", ("%" + name + "%",))
    return cursor.fetchall()

def filter_flavors(season):
    cursor.execute("SELECT * FROM flavors WHERE season =?", (season,))
    return cursor.fetchall()

def get_cart(customer_name):
    cursor.execute("SELECT f.name, f.description FROM carts c JOIN flavors f ON c.flavor_id = f.id WHERE c.customer_name =?", (customer_name,))
    return cursor.fetchall()

def main():
    while True:
        print("Ice Cream Parlor Cafe")
        print("1. Add flavor")
        print("2. Add ingredient")
        print("3. Add allergen")
        print("4. Add flavor ingredient")
        print("5. Add customer suggestion")
        print("6. Add customer allergen")
        print("7. Add to cart")
        print("8. Search flavors")
        print("9. Filter flavors")
        print("10. Get cart")
        print("11. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter flavor name: ")
            description = input("Enter flavor description: ")
            season = input("Enter flavor season: ")
            add_flavor(name, description, season)
        elif choice == "2":
            name = input("Enter ingredient name: ")
            quantity = int(input("Enter ingredient quantity: "))
            add_ingredient(name, quantity)
        elif choice == "3":
            name = input("Enter allergen name: ")
            add_allergen(name)
        elif choice == "4":
            flavor_id = int(input("Enter flavor ID: "))
            ingredient_id = int(input("Enter ingredient ID: "))
            add_flavor_ingredient(flavor_id, ingredient_id)
        elif choice == "5":
            customer_name = input("Enter customer name: ")
            flavor_name = input("Enter flavor name: ")
            description = input("Enter description: ")
            add_customer_suggestion(customer_name, flavor_name, description)
        elif choice == "6":
            customer_name = input("Enter customer name: ")
            allergen_id = int(input("Enter allergen ID: "))
            add_customer_allergen(customer_name, allergen_id)
        elif choice == "7":
            customer_name = input("Enter customer name: ")
            flavor_id = int(input("Enter flavor ID: "))
            add_to_cart(customer_name, flavor_id)
        elif choice == "8":
            name = input("Enter flavor name to search: ")
            results = search_flavors(name)
            for row in results:
                print(row)
        elif choice == "9":
            season = input("Enter season to filter: ")
            results = filter_flavors(season)
            for row in results:
                print(row)
        elif choice == "10":
            customer_name = input("Enter customer name: ")
            results = get_cart(customer_name)
            for row in results:
                print(row)
        elif choice == "11":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

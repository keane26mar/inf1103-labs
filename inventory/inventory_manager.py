import json
import os

FILENAME = "inventory.json"

# Default products used the first time the program runs (no inventory.json yet)
DEFAULT_INVENTORY = [
    {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
    {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
    {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
]


# ---------- Data Persistence ----------
def load_inventory():
    """Load inventory from inventory.json if it exists, otherwise use defaults."""
    if os.path.exists(FILENAME):
        print(f"{FILENAME} found.")
        try:
            with open(FILENAME, "r") as f:
                inventory = json.load(f)
            if isinstance(inventory, list) and len(inventory) > 0:
                print("Inventory loaded successfully.")
                return inventory
            print("File is empty or in the wrong format. Using default inventory.")
        except (json.JSONDecodeError, OSError):
            print("Could not read file. Using default inventory.")
    else:
        print(f"{FILENAME} not found. Creating it with default inventory.")
    inventory = [item.copy() for item in DEFAULT_INVENTORY]
    save_inventory(inventory)  # create/overwrite inventory.json with the defaults
    return inventory


def save_inventory(inventory, message="Inventory saved successfully."):
    """Save inventory list to inventory.json."""
    with open(FILENAME, "w") as f:
        json.dump(inventory, f, indent=4)
    print(message)


# ---------- Data Manipulation ----------
def find_product(inventory, product_id):
    """Return the product dictionary with the given ID, or None."""
    for product in inventory:
        if product["id"].lower() == product_id.lower():
            return product
    return None


def add_product(inventory):
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()
    if find_product(inventory, product_id):
        print("A product with that ID already exists!")
        return
    name = input("Product Name: ").strip()
    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input. Price must be a number and stock a whole number.")
        return
    inventory.append({"id": product_id, "name": name, "price": price, "stock": stock})
    print("\nProduct added successfully!")


def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Product ID: ").strip()
    product = find_product(inventory, product_id)
    if not product:
        print("Product not found.")
        return
    try:
        new_stock = int(input(f"New stock quantity for {product['name']}: "))
    except ValueError:
        print("Invalid input. Stock must be a whole number.")
        return
    product["stock"] = new_stock
    print("\nStock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    product_id = input("Enter Product ID: ").strip()
    product = find_product(inventory, product_id)
    if not product:
        print("\nProduct not found.")
        return
    print("\nProduct Found")
    print("-" * 48)
    print(f"ID: {product['id']}")
    print(f"Name: {product['name']}")
    print(f"Price: ${product['price']:.2f}")
    print(f"Stock: {product['stock']}")
    print("-" * 48)


def print_product(p):
    print(f"ID: {p['id']} | Name: {p['name']} | Price: ${p['price']:.2f} | Stock: {p['stock']}")


def display_all(inventory):
    print("\nCurrent Inventory")
    print("-" * 45)
    if not inventory:
        print("Inventory is empty.")
    for p in inventory:
        print_product(p)
    print("-" * 45)


# ---------- Menu System ----------
def show_menu():
    print("\n----------- MENU -----------")
    print("1. Display All Products")
    print("2. Add Product")
    print("3. Update Stock")
    print("4. Search Product")
    print("5. Save Inventory")
    print("6. Exit")
    print("----------------------------")


def main():
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    print()

    inventory = load_inventory()

    while True:
        show_menu()
        choice = input("\nEnter option: ").strip()

        if choice == "1":
            display_all(inventory)
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            print("\nSaving inventory...")
            save_inventory(inventory, "Inventory saved successfully to inventory.json.")
        elif choice == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("\nThank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("Invalid option. Please choose 1-6.")


if __name__ == "__main__":
    main()
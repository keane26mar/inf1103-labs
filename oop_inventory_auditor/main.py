from inventory import Inventory
from product import Product

def main():
    # Initialize Inventory and load previous data
    inventory = Inventory()
    inventory.load_from_file()

    while True:
        print("\n--- Inventory Management System ---")
        print("1. Display all products")
        print("2. Add a product")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            product_id = input("Enter Product ID: ").strip()
            name = input("Enter Product Name: ").strip()
            try:
                price = float(input("Enter Product Price: "))
                stock = int(input("Enter Initial Stock Quantity: "))
                
                if price < 0 or stock < 0:
                    print("Error: Price and stock quantities cannot be negative.")
                    continue
                
                if inventory.search_product(product_id):
                    print("Error: Product ID already exists.")
                else:
                    new_product = Product(product_id, name, price, stock)
                    inventory.add_product(new_product)
                    print("Product added successfully!")
            except ValueError:
                print("Error: Invalid numeric input for price or stock.")

        elif choice == "3":
            product_id = input("Enter Product ID to update stock: ").strip()
            product = inventory.search_product(product_id)
            if product:
                try:
                    qty = int(input("Enter quantity to add (use negative values to reduce stock): "))
                    product.update_stock(qty)
                    print(f"Stock updated successfully. New stock for {product.name}: {product.stock}")
                except ValueError:
                    print("Error: Invalid quantity entered.")
            else:
                print("Error: Product not found.")

        elif choice == "4":
            product_id = input("Enter Product ID to search: ").strip()
            product = inventory.search_product(product_id)
            if product:
                print("\nProduct Found:")
                product.display_information()
            else:
                print("Product not found.")

        elif choice == "5":
            inventory.save_to_file()

        elif choice == "6":
            inventory.save_to_file()
            print("Exiting program. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please select an option between 1 and 6.")


if __name__ == "__main__":
    main()
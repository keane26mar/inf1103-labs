from inventory import Inventory
from product import PhysicalProduct, DigitalProduct

def main():
    # Initialize Inventory and load previous data
    inventory = Inventory()
    inventory.load_from_file()

    while True:
        print("\n--- Inventory Management System (Lab 7) ---")
        print("1. Display all products")
        print("2. Add a product (Physical or Digital)")
        print("3. Update stock")
        print("4. Search for a product")
        print("5. Save inventory")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            print("\nSelect Product Type:")
            print("1. Physical Product")
            print("2. Digital Product")
            type_choice = input("Enter type choice (1-2): ").strip()

            if type_choice not in ["1", "2"]:
                print("Error: Invalid product type selection.")
                continue

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
                    continue

                if type_choice == "1":
                    weight = float(input("Enter Product Weight (kg): "))
                    if weight < 0:
                        print("Error: Weight cannot be negative.")
                        continue
                    new_product = PhysicalProduct(product_id, name, price, stock, weight)
                else:
                    download_size = float(input("Enter Download Size (MB): "))
                    if download_size < 0:
                        print("Error: Download size cannot be negative.")
                        continue
                    new_product = DigitalProduct(product_id, name, price, stock, download_size)

                inventory.add_product(new_product)
                print("Product added successfully!")
            except ValueError:
                print("Error: Invalid numeric input provided.")

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
                print(f"   Fulfilment: {product.get_fulfilment_info()}")
                if hasattr(product, 'calculate_shipping_cost'):
                    print(f"   Shipping Cost: ${product.calculate_shipping_cost():.2f}")
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
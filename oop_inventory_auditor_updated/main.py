import json
import os
from inventory import Inventory
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier
from order import Order

def save_orders_to_file(orders: list[Order], filename: str = "orders.json") -> None:
    """Saves all customer orders to a JSON file."""
    data = []
    for order in orders:
        lines_data = []
        for line in order.order_lines:
            lines_data.append({
                "product_id": line.product.product_id,
                "quantity": line.quantity
            })
        data.append({
            "order_id": order.order_id,
            "order_lines": lines_data
        })
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"Orders successfully saved to {filename}")


def load_orders_from_file(inventory: Inventory, filename: str = "orders.json") -> list[Order]:
    """Loads orders from a JSON file, linking them back to actual Product objects in inventory."""
    if not os.path.exists(filename):
        return []
    
    loaded_orders = []
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for item in data:
                order = Order(item["order_id"])
                for line_data in item["order_lines"]:
                    product = inventory.find_product(line_data["product_id"])
                    if product:
                        order.add_order_line(product, line_data["quantity"])
                loaded_orders.append(order)
        print(f"Orders successfully loaded from {filename}")
    except Exception as e:
        print(f"Error loading orders: {e}")
    
    return loaded_orders


def main() -> None:
    inventory = Inventory()
    inventory.load_from_file()

    # Load existing orders from file at startup
    orders: list[Order] = load_orders_from_file(inventory)

    while True:
        print("\n--- Inventory & Order Management System (Lab 8) ---")
        print("1. Display all products")
        print("2. Add a product (Physical/Digital)")
        print("3. Remove a product from Inventory (Aggregation test)")
        print("4. Update stock")
        print("5. Create a Customer Order (Composition test)")
        print("6. View Existing Orders")
        print("7. Save inventory and orders")
        print("8. Exit")

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            inventory.display_all()

        elif choice == "2":
            print("\n--- Enter Supplier Details ---")
            supplier_id = input("Enter Supplier ID: ").strip()
            supplier_name = input("Enter Supplier Name: ").strip()
            supplier_email = input("Enter Supplier Contact Email: ").strip()
            
            selected_supplier = Supplier(supplier_id, supplier_name, supplier_email)

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
                    print("Error: Price and stock cannot be negative.")
                    continue
                
                if inventory.find_product(product_id):
                    print("Error: Product ID already exists.")
                    continue

                if type_choice == "1":
                    weight = float(input("Enter Product Weight (kg): "))
                    new_product = PhysicalProduct(product_id, name, price, stock, selected_supplier, weight)
                else:
                    download_size = float(input("Enter Download Size (MB): "))
                    new_product = DigitalProduct(product_id, name, price, stock, selected_supplier, download_size)

                inventory.add_product(new_product)
                print("Product added successfully with associated supplier!")
            except ValueError:
                print("Error: Invalid numeric input provided.")

        elif choice == "3":
            product_id = input("Enter Product ID to remove from inventory: ").strip()
            product = inventory.find_product(product_id)
            if product:
                inventory.remove_product(product_id)
                print(f"Product '{product.name}' removed from inventory.")
            else:
                print("Product not found in inventory.")

        elif choice == "4":
            product_id = input("Enter Product ID to update stock: ").strip()
            product = inventory.find_product(product_id)
            if product:
                try:
                    qty = int(input("Enter quantity to add/reduce: "))
                    product.update_stock(qty)
                    print(f"Stock updated successfully. New stock: {product.stock}")
                except ValueError:
                    print("Error: Invalid quantity.")
            else:
                print("Product not found.")

        elif choice == "5":
            if not inventory.products:
                print("No products available to order.")
                continue
            
            order_id = input("Enter Order ID (e.g., ORD-001): ").strip()
            new_order = Order(order_id)
            
            while True:
                inventory.display_all()
                p_id = input("Enter Product ID to add to order (or type 'done'): ").strip()
                if p_id.lower() == 'done':
                    break
                
                product = inventory.find_product(p_id)
                if not product:
                    print("Product not found.")
                    continue
                
                try:
                    qty = int(input("Enter quantity ordered: "))
                    if qty <= 0:
                        print("Quantity must be greater than zero.")
                        continue
                    new_order.add_order_line(product, qty)
                    print("Order line added.")
                except ValueError:
                    print("Invalid quantity.")

            if new_order.order_lines:
                orders.append(new_order)
                new_order.display_order()
                # Automatically save orders to file upon creation
                save_orders_to_file(orders)
            else:
                print("Order cancelled (no lines added).")

        elif choice == "6":
            if not orders:
                print("No active orders found.")
            else:
                for order in orders:
                    order.display_order()

        elif choice == "7":
            inventory.save_to_file()
            save_orders_to_file(orders)

        elif choice == "8":
            inventory.save_to_file()
            save_orders_to_file(orders)
            print("Exiting program. Goodbye!")
            break
        else:
            print("Error: Invalid option.")

if __name__ == "__main__":
    main()
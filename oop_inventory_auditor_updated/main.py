from supplier import Supplier
from inventory import Inventory, load_products
from order import Order
from order_manager import OrderManager
from discount import NoDiscount, PercentageDiscount, BulkDiscount, StudentDiscount

def get_positive_float(prompt: str) -> float:
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")

def main() -> None:
    supplier = Supplier("S001", "Global Goods", "contact@globalgoods.com")
    inventory = Inventory()
    
    # Initialize OrderManager with JSON persistence
    order_manager = OrderManager("orders.json")

    # Load products from CSV and restore existing persisted orders from orders.json
    load_products("products.csv", inventory, supplier)
    order_manager.load_from_json(inventory)

    while True:
        print("\n--- Inventory & Order Management System (Lab 9) ---")
        print("1. Display all products")
        print("2. Create an order with Strategy Discount")
        print("3. View all orders")
        print("4. View a single order")
        print("5. Update an order")
        print("6. Delete an order")
        print("7. Exit")
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == "1":
            inventory.display_all()
            
        elif choice == "2":
            if not inventory.products:
                print("No products available in inventory.")
                continue
            
            # Validate Order ID
            order_id = input("Enter Order ID (e.g., ORD-001): ").strip()
            if not order_id:
                print("Error: Order ID cannot be empty.")
                continue
            
            if order_manager.find_order(order_id):
                print(f"Error: Order ID '{order_id}' already exists.")
                continue
            
            # Get Product ID from CSV
            prod_id_input = input("Enter Product ID from CSV (e.g., P001): ").strip()
            
            # Validation: Prevent Order ID and Product ID from being the same
            if order_id == prod_id_input:
                print(f"Error: Order ID and Product ID cannot both be '{order_id}'. Access denied.")
                continue
            
            selected_product = inventory.find_product(prod_id_input)
            
            if not selected_product:
                print(f"Error: Product ID '{prod_id_input}' does not exist in inventory/products.csv! Access denied.")
                continue
            
            try:
                quantity = int(input("Enter quantity: "))
                if quantity <= 0:
                    print("Quantity must be greater than zero.")
                    continue
            except ValueError:
                print("Invalid input. Please enter a valid whole number for quantity.")
                continue
            
            # Create order, add line, and calculate subtotal
            order = Order(order_id)
            order.add_order_line(selected_product, quantity)
            
            print(f"Subtotal before discount: ${order.calculate_total():.2f}")
            
            # Choose discount strategy manually
            print("\nSelect Discount Strategy:")
            print("1. No Discount")
            print("2. Percentage Discount (10%)")
            print("3. Bulk Discount ($20 off if >= $200)")
            print("4. Student Discount (15% off)")
            
            d_choice = input("Enter choice (1-4): ").strip()
            if d_choice == "1":
                order.set_discount(NoDiscount())
            elif d_choice == "2":
                order.set_discount(PercentageDiscount(10.0))
            elif d_choice == "3":
                order.set_discount(BulkDiscount(200.0, 20.0))
            elif d_choice == "4":
                order.set_discount(StudentDiscount(15.0))
            else:
                print("Invalid choice. Defaulting to No Discount.")
            
            print(f"Final Order Total after discount: ${order.calculate_total():.2f}")
            
            # Save order to manager and update orders.json automatically
            order_manager.add_order(order)
            print(f"Order '{order_id}' created and saved successfully!")

        elif choice == "3":
            order_manager.display_all_orders()
            
        elif choice == "4":
            # VIEW SINGLE ORDER
            order_id = input("Enter Order ID to view: ").strip()
            order = order_manager.find_order(order_id)
            if order:
                print(f"\n=== Order Details: {order.order_id} ===")
                print("  Items:")
                for line in order.order_lines:
                    print(f"    - {line.product.name} (ID: {line.product.product_id}) | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
                print(f"  Final Total (after discount): ${order.calculate_total():.2f}")
            else:
                print(f"Error: Order ID '{order_id}' not found.")

        elif choice == "5":
            # UPDATE ORDER
            order_id = input("Enter Order ID to update: ").strip()
            order = order_manager.find_order(order_id)
            if not order:
                print(f"Error: Order '{order_id}' not found.")
                continue
            
            print(f"Updating Order: {order.order_id}")
            print("1. Update quantity of existing item")
            print("2. Change discount strategy")
            u_choice = input("Enter choice (1-2): ").strip()
            
            if u_choice == "1":
                if order.order_lines:
                    try:
                        new_qty = int(input("Enter new quantity: "))
                        if new_qty <= 0:
                            print("Quantity must be greater than zero.")
                            continue
                        order.order_lines[0].quantity = new_qty
                        order_manager.save_to_json()  # Persist changes
                        print("Order quantity updated successfully!")
                    except ValueError:
                        print("Invalid quantity input.")
            elif u_choice == "2":
                print("\nSelect New Discount Strategy:")
                print("1. No Discount")
                print("2. Percentage Discount (10%)")
                print("3. Bulk Discount ($20 off if >= $200)")
                print("4. Student Discount (15% off)")
                d_choice = input("Enter choice (1-4): ").strip()
                if d_choice == "1":
                    order.set_discount(NoDiscount())
                elif d_choice == "2":
                    order.set_discount(PercentageDiscount(10.0))
                elif d_choice == "3":
                    order.set_discount(BulkDiscount(200.0, 20.0))
                elif d_choice == "4":
                    order.set_discount(StudentDiscount(15.0))
                
                order_manager.save_to_json()  # Persist changes
                print("Discount strategy updated successfully!")
            else:
                print("Invalid update choice.")

        elif choice == "6":
            # DELETE ORDER
            order_id = input("Enter Order ID to delete: ").strip()
            if order_manager.delete_order(order_id):
                print(f"Order '{order_id}' successfully deleted.")
            else:
                print(f"Error: Order ID '{order_id}' not found.")

        elif choice == "7":
            print("Exiting application.")
            break
        else:
            print("Invalid option. Please choose between 1 and 7.")

if __name__ == "__main__":
    main()
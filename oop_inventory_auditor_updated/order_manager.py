import json
from order import Order

class OrderManager:
    """Manages a collection of orders with JSON file persistence."""
    def __init__(self, storage_file: str = "orders.json"):
        self.storage_file = storage_file
        self.orders: list[Order] = []

    def add_order(self, order: Order) -> None:
        self.orders.append(order)
        self.save_to_json()

    def delete_order(self, order_id: str) -> bool:
        order = self.find_order(order_id)
        if order:
            self.orders.remove(order)
            self.save_to_json()
            return True
        return False

    def find_order(self, order_id: str) -> Order | None:
        for order in self.orders:
            if order.order_id == order_id:
                return order
        return None

    def display_all_orders(self) -> None:
        if not self.orders:
            print("\nNo orders recorded in the system.")
            return
        
        print("\n=== SUMMARY OF ALL ORDERS ===")
        for order in self.orders:
            print(f"\nOrder ID: {order.order_id}")
            print("  Items:")
            for line in order.order_lines:
                print(f"    - {line.product.name} (ID: {line.product.product_id}) | Qty: {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
            print(f"  Final Total: ${order.calculate_total():.2f}")

    def save_to_json(self) -> None:
        """Serializes current orders into orders.json."""
        data = []
        for order in self.orders:
            lines_data = []
            for line in order.order_lines:
                lines_data.append({
                    "product_id": line.product.product_id,
                    "product_name": line.product.name,
                    "product_price": line.product.price,
                    "quantity": line.quantity
                })
            data.append({
                "order_id": order.order_id,
                "order_lines": lines_data
            })
        
        try:
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except IOError as e:
            print(f"Error saving orders to file: {e}")

    def load_from_json(self, inventory) -> None:
        """Loads saved orders from orders.json on startup."""
        try:
            with open(self.storage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.orders.clear()
                for item in data:
                    order_id = item["order_id"]
                    order = Order(order_id)
                    for l_data in item["order_lines"]:
                        prod = inventory.find_product(l_data["product_id"])
                        if prod:
                            order.add_order_line(prod, l_data["quantity"])
                    self.orders.append(order)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            print("Error parsing orders.json. File may be corrupted.")
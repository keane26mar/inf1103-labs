from product import Product

class OrderLine:
    """Represents an item line within an order (Composition part)."""
    def __init__(self, product: Product, quantity: int) -> None:
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        """Calculates the subtotal for this order line."""
        return self.product.price * self.quantity


class Order:
    """Represents a customer order that creates and manages its OrderLines (Composition whole)."""
    def __init__(self, order_id: str) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        """Creates and manages internal OrderLine objects (Composition)."""
        order_line = OrderLine(product, quantity)
        self.order_lines.append(order_line)

    def calculate_total(self) -> float:
        """Calculates total order cost across all lines."""
        return sum(line.calculate_subtotal() for line in self.order_lines)

    def display_order(self) -> None:
        print(f"\n--- Order ID: {self.order_id} ---")
        for line in self.order_lines:
            print(f" - {line.product.name} x {line.quantity} | Subtotal: ${line.calculate_subtotal():.2f}")
        print(f"Total Order Cost: ${self.calculate_total():.2f}")
        print("-----------------------------")
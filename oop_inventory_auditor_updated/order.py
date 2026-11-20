from product import Product
from discount import DiscountStrategy, NoDiscount

class OrderLine:
    def __init__(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("OrderLine quantity must be greater than zero.")
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

class Order:
    def __init__(self, order_id: str, discount_strategy: DiscountStrategy | None = None) -> None:
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []
        self.discount: DiscountStrategy = discount_strategy if discount_strategy else NoDiscount()

    def add_order_line(self, product: Product, quantity: int) -> None:
        line = OrderLine(product, quantity)
        self.order_lines.append(line)

    def set_discount(self, discount_strategy: DiscountStrategy) -> None:
        """Dynamically updates the discount strategy."""
        self.discount = discount_strategy

    def calculate_total(self) -> float:
        """Delegates calculation entirely to the active discount strategy[cite: 3, 4]."""
        total = sum(line.calculate_subtotal() for line in self.order_lines)
        return self.discount.apply(total)
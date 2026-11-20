from abc import ABC
from supplier import Supplier

class Product(ABC):
    """Abstract base product class with validation rules."""
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier) -> None:
        if price <= 0:
            raise ValueError("Product price must be greater than zero.")
        if stock_quantity < 0:
            raise ValueError("Product stock quantity cannot be negative.")
        
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity
        self.supplier = supplier

class PhysicalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, weight: float) -> None:
        if weight <= 0:
            raise ValueError("Physical product weight must be greater than zero.")
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.weight = weight

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, download_size: float) -> None:
        if download_size <= 0:
            raise ValueError("Digital product download size must be greater than zero.")
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.download_size = download_size

class ProductFactory:
    """Factory class to centralize product creation logic."""
    @staticmethod
    def create(product_type: str, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, extra_arg: float = 1.0) -> Product:
        ptype = product_type.lower().strip()
        if ptype == "physical":
            return PhysicalProduct(product_id, name, price, stock_quantity, supplier, weight=extra_arg)
        elif ptype == "digital":
            return DigitalProduct(product_id, name, price, stock_quantity, supplier, download_size=extra_arg)
        else:
            raise ValueError(f"Unknown product type: {product_type}")
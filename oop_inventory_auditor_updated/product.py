from abc import ABC, abstractmethod
from shipping import CanBeShipped
from supplier import Supplier

class Product(ABC):
    """Abstract base class representing a generic product associated with a Supplier."""
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier) -> None:
        self._product_id: str = product_id
        self.name: str = name
        self._price: float = price
        self._stock: int = stock
        self.supplier: Supplier = supplier  # Association

    @property
    def product_id(self) -> str:
        return self._product_id

    @property
    def price(self) -> float:
        return self._price

    @property
    def stock(self) -> int:
        return self._stock

    def update_stock(self, quantity: int) -> None:
        """Safely updates the product's stock level."""
        self._stock += quantity

    def display_information(self) -> None:
        """Displays common product and associated supplier details."""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock} | Supplier: {self.name}", end="")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        """Abstract method defining how the product is fulfilled."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product with weight and shipping capabilities."""
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, weight: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._weight: float = weight

    @property
    def weight(self) -> float:
        return self._weight

    def display_information(self) -> None:
        """Overrides display_information to include weight."""
        super().display_information()
        print(f" | Weight: {self._weight} kg")

    def get_fulfilment_info(self) -> str:
        return "Requires physical shipping and handling."

    def calculate_shipping_cost(self) -> float:
        return 5.00 + (self._weight * 2.00)


class DigitalProduct(Product):
    """Represents a digital product with a download size."""
    def __init__(self, product_id: str, name: str, price: float, stock: int, supplier: Supplier, download_size: float) -> None:
        super().__init__(product_id, name, price, stock, supplier)
        self._download_size: float = download_size

    @property
    def download_size(self) -> float:
        return self._download_size

    def display_information(self) -> None:
        """Overrides display_information to include download size."""
        super().display_information()
        print(f" | Download Size: {self._download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "Delivered digitally via secure download link."
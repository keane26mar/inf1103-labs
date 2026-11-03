from abc import ABC, abstractmethod
from shipping import CanBeShipped

class Product(ABC):
    """Abstract base class representing a generic product[cite: 15]."""
    def __init__(self, product_id, name, price, stock):
        self._product_id = product_id
        self.name = name
        self._price = price
        self._stock = stock

    @property
    def product_id(self):
        return self._product_id

    @property
    def price(self):
        return self._price

    @property
    def stock(self):
        return self._stock

    def update_stock(self, quantity):
        """Safely updates the product's stock level."""
        self._stock += quantity

    def display_information(self):
        """Displays common product details."""
        print(f"ID: {self._product_id} | Name: {self.name} | Price: ${self._price:.2f} | Stock: {self._stock}", end="")

    @abstractmethod
    def get_fulfilment_info(self):
        """Abstract method defining how the product is fulfilled[cite: 15]."""
        pass


class PhysicalProduct(Product, CanBeShipped):
    """Represents a physical product with weight and shipping capabilities[cite: 13, 15]."""
    def __init__(self, product_id, name, price, stock, weight):
        super().__init__(product_id, name, price, stock)
        self._weight = weight  # weight in kg[cite: 13]

    @property
    def weight(self):
        return self._weight

    def display_information(self):
        """Overrides display_information to include weight[cite: 13, 14]."""
        super().display_information()
        print(f" | Weight: {self._weight} kg")

    def get_fulfilment_info(self):
        """Returns physical fulfilment information[cite: 15]."""
        return "Requires physical shipping and handling."

    def calculate_shipping_cost(self):
        """Calculates shipping cost based on weight (e.g., $5 base + $2 per kg)[cite: 15]."""
        return 5.00 + (self._weight * 2.00)


class DigitalProduct(Product):
    """Represents a digital product with a download size[cite: 13]."""
    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self._download_size = download_size  # download size in MB[cite: 13]

    @property
    def download_size(self):
        return self._download_size

    def display_information(self):
        """Overrides display_information to include download size[cite: 13, 14]."""
        super().display_information()
        print(f" | Download Size: {self._download_size} MB")

    def get_fulfilment_info(self):
        """Returns digital fulfilment information[cite: 15]."""
        return "Delivered digitally via secure download link."
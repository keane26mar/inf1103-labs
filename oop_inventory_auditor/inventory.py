import json
import os
from product import Product

class Inventory:
    """Manages a collection of Product objects and file persistence."""
    def __init__(self):
        self._products = []

    def add_product(self, product):
        """Adds a new Product object to the inventory list."""
        self._products.append(product)

    def search_product(self, product_id):
        """Searches for a product by its ID and returns the Product object or None."""
        for product in self._products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self):
        """Displays all products currently in the inventory."""
        if not self._products:
            print("Inventory is currently empty.")
            return
        print("\n=== Current Inventory ===")
        for product in self._products:
            product.display_information()
        print("=========================")

    def save_to_file(self, filename="inventory.json"):
        """Saves all products in inventory to a JSON file."""
        data = []
        for p in self._products:
            data.append({
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory successfully saved to {filename}")

    def load_from_file(self, filename="inventory.json"):
        """Loads inventory data from a JSON file into Product objects."""
        if not os.path.exists(filename):
            print(f"No existing {filename} found. Starting with an empty inventory.")
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self._products = []
                for item in data:
                    product = Product(
                        item["product_id"],
                        item["name"],
                        float(item["price"]),
                        int(item["stock"])
                    )
                    self._products.append(product)
            print(f"Inventory successfully loaded from {filename}")
        except Exception as e:
            print(f"Error loading inventory: {e}")
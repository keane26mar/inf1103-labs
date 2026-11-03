import json
import os
from product import PhysicalProduct, DigitalProduct

class Inventory:
    """Manages a collection of Product objects and file persistence[cite: 16]."""
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
        """Displays all products currently in the inventory[cite: 16]."""
        if not self._products:
            print("Inventory is currently empty.")
            return
        print("\n=== Current Inventory ===")
        for product in self._products:
            product.display_information()
            print(f"   Fulfilment: {product.get_fulfilment_info()}")
            if hasattr(product, 'calculate_shipping_cost'):
                print(f"   Shipping Cost: ${product.calculate_shipping_cost():.2f}")
        print("=========================")

    def save_to_file(self, filename="inventory.json"):
        """Saves all products in inventory to a JSON file preserving types[cite: 16]."""
        data = []
        for p in self._products:
            item = {
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock
            }
            if isinstance(p, PhysicalProduct):
                item["type"] = "physical"
                item["weight"] = p.weight
            elif isinstance(p, DigitalProduct):
                item["type"] = "digital"
                item["download_size"] = p.download_size
            data.append(item)
            
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Inventory successfully saved to {filename}")

    def load_from_file(self, filename="inventory.json"):
        """Loads inventory data from a JSON file into correct subclasses[cite: 16]."""
        if not os.path.exists(filename):
            print(f"No existing {filename} found. Starting with an empty inventory.")
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self._products = []
                for item in data:
                    ptype = item.get("type")
                    if ptype == "physical":
                        product = PhysicalProduct(
                            item["product_id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item["weight"])
                        )
                    elif ptype == "digital":
                        product = DigitalProduct(
                            item["product_id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            float(item["download_size"])
                        )
                    else:
                        continue
                    self._products.append(product)
            print(f"Inventory successfully loaded from {filename}")
        except Exception as e:
            print(f"Error loading inventory: {e}")
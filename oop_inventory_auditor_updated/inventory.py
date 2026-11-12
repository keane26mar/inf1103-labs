import json
import os
from product import PhysicalProduct, DigitalProduct
from supplier import Supplier
from product import Product

class Inventory:
    """Manages an aggregated collection of Product objects and JSON persistence."""
    def __init__(self) -> None:
        self.products: list[Product] = []  # Aggregation collection with type hints

    def add_product(self, product: Product) -> None:
        """Adds an existing Product object to the inventory."""
        self.products.append(product)

    def remove_product(self, product_id: str) -> None:
        """Removes a product reference by ID without destroying the product object."""
        self.products = [p for p in self.products if p.product_id != product_id]

    def find_product(self, product_id: str) -> Product | None:
        """Finds and returns a matching Product or None."""
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def display_all(self) -> None:
        """Displays all products using polymorphism."""
        if not self.products:
            print("Inventory is currently empty.")
            return
        print("\n=== Current Inventory (Aggregation) ===")
        for product in self.products:
            product.display_information()
            print(f"   Fulfilment: {product.get_fulfilment_info()}")
            if hasattr(product, 'calculate_shipping_cost'):
                print(f"   Shipping Cost: ${product.calculate_shipping_cost():.2f}")
            print(f"   Supplier Info: {product.supplier.name} ({product.supplier.contact_email})")
        print("=======================================")

    def save_to_file(self, filename: str = "inventory.json") -> None:
        """Saves inventory data including supplier information and product types."""
        data = []
        for p in self.products:
            item = {
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock,
                "supplier_id": p.supplier.supplier_id,
                "supplier_name": p.supplier.name,
                "supplier_email": p.supplier.contact_email
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

    def load_from_file(self, filename: str = "inventory.json") -> None:
        """Loads inventory data reconstructing Supplier and Subclass objects."""
        if not os.path.exists(filename):
            print(f"No existing {filename} found. Starting with an empty inventory.")
            return
        try:
            with open(filename, "r") as f:
                data = json.load(f)
                self.products = []
                for item in data:
                    supplier = Supplier(
                        item["supplier_id"],
                        item["supplier_name"],
                        item["supplier_email"]
                    )
                    ptype = item.get("type")
                    if ptype == "physical":
                        product = PhysicalProduct(
                            item["product_id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            supplier,
                            float(item["weight"])
                        )
                    elif ptype == "digital":
                        product = DigitalProduct(
                            item["product_id"],
                            item["name"],
                            float(item["price"]),
                            int(item["stock"]),
                            supplier,
                            float(item["download_size"])
                        )
                    else:
                        continue
                    self.products.append(product)
            print(f"Inventory successfully loaded from {filename}")
        except Exception as e:
            print(f"Error loading inventory: {e}")
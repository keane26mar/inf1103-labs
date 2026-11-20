import csv
from product import Product, ProductFactory
from supplier import Supplier

class Inventory:
    def __init__(self) -> None:
        self.products: list[Product] = []

    def add_product(self, product: Product) -> None:
        self.products.append(product)

    def find_product(self, product_id: str) -> Product | None:
        for p in self.products:
            if p.product_id.lower() == product_id.lower():
                return p
        return None

    def display_all(self) -> None:
        if not self.products:
            print("\nInventory is currently empty.")
            return
        print("\n--- Current Inventory Products ---")
        for p in self.products:
            print(f"ID: {p.product_id} | Name: {p.name} | Price: ${p.price:.2f} | Stock: {p.stock_quantity}")


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    """Loads products from CSV using try/except/else/finally and ProductFactory[cite: 5, 6]."""
    loaded = 0
    try:
        file = open(path, newline="", encoding="utf-8")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip header row
            if header is None:
                print("CSV file is empty.")
                return

            for row_idx, row in enumerate(reader, start=2):
                if not row or len(row) < 5:
                    continue
                try:
                    ptype = row[0].strip()
                    pid = row[1].strip()
                    name = row[2].strip()
                    price = float(row[3].strip())
                    stock = int(row[4].strip())
                    extra = float(row[5].strip()) if len(row) > 5 else 1.0

                    prod = ProductFactory.create(ptype, pid, name, price, stock, supplier, extra)
                    inventory.add_product(prod)
                    loaded += 1
                except ValueError as e:
                    print(f"Skipping invalid row {row_idx}: {e}")
        print(f"{loaded} products loaded successfully.")
    finally:
        print("Load attempt finished.")
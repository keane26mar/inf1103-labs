from supplier import Supplier
from product import Product, PhysicalProduct, DigitalProduct
from inventory import Inventory
from order import Order

print("--- 1. Test Generalisation & Inheritance ---")
sup = Supplier("S01", "TechCorp", "support@techcorp.com")
phys_prod = PhysicalProduct("P01", "Laptop", 999.99, 10, sup, 2.5)
digi_prod = DigitalProduct("D01", "Software License", 49.99, 100, sup, 1.2)

# Prove 'is-a' relationship (Generalisation)
print(f"Is PhysicalProduct an instance of Product? {isinstance(phys_prod, Product)}")
print(f"Is DigitalProduct an instance of Product? {isinstance(digi_prod, Product)}")

# Prove inherited attributes and polymorphic method execution (LSP)
catalog: list[Product] = [phys_prod, digi_prod]
for item in catalog:
    print(f" - Product: {item.name} | Fulfilment: {item.get_fulfilment_info()}")


print("\n--- 2. Test Association (Product -> Supplier) ---")
print(f"Supplier Association Test: Product '{phys_prod.name}' linked to Supplier '{phys_prod.supplier.name}'")


print("\n--- 3. Test Aggregation (Inventory manages Products) ---")
inv = Inventory()
inv.add_product(phys_prod)
print(f"Aggregation Test: Inventory holds {len(inv.products)} product.")
inv.remove_product("P01")
print(f"After removal, Inventory count: {len(inv.products)}, but Supplier/Product object still exists in memory.")


print("\n--- 4. Test Composition (Order owns OrderLine) ---")
order = Order("ORD-001")
order.add_order_line(phys_prod, 2)
print(f"Composition Test: Order created with {len(order.order_lines)} order line(s) internally owned by the Order.")
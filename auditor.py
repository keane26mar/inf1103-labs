# Initialize inventory and failed entry counters
total_inventory = 0
failed_entries = 0

print("--- Real-Time Delivery Auditor Started ---")

while True:
  # Ask user to enter a stock quantity or 'quit'
  user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

  # Check if the user wants to quit
  if user_input.lower() == "quit":
    break

  # Handle invalid input: check if the string contains only digits (Hint: isdigit())
  if not user_input.isdigit():
    print(
        "Error: Invalid input detected (text or invalid characters). Entry"
        " rejected."
    )
    failed_entries += 1
    continue

  # Convert the valid string to an integer
  stock_quantity = int(user_input)

  # Enforce business rules: Reject negative numbers
  if stock_quantity < 0:
    print("Error: Negative values are not allowed. Entry rejected.")
    failed_entries += 1
    continue

  # Manage State: Keep a running total of the inventory
  total_inventory += stock_quantity

  # Trigger Overstock Alert: If total inventory exceeds 500 units
  if total_inventory > 500:
    print(
        "OVERSTOCK ALERT: Total inventory has exceeded 500 units! Stopping"
        " processing immediately."
    )
    break
  else:
    print(f"Current Inventory Total: {total_inventory}")

# Reporting: Print summary when loop terminates
print("\n=== Delivery Audit Report ===")
print(f"Total Units Processed: {total_inventory}")
print(f"Number of Failed/Rejected Entries: {failed_entries}")
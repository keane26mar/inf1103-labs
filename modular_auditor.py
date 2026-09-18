def get_valid_input():
    """Prompts the user for a stock quantity.
    Input: nothing
    Output: a valid integer, or the string "quit" if the user wants to exit,
             or None if the entry was invalid/rejected.
    """
    user_input = input("Enter stock quantity (or type 'quit' to exit): ").strip()

    if user_input.lower() == "quit":
        return "quit"

    if not user_input.isdigit():
        print("Error: Invalid input detected (text or invalid characters). Entry rejected.")
        return None

    stock_quantity = int(user_input)

    if stock_quantity < 0:
        print("Error: Negative values are not allowed. Entry rejected.")
        return None

    return stock_quantity


def process_delivery(current_total, new_value):
    """Input: current running total, new delivery value.
    Output: the new running total.
    """
    return current_total + new_value


def calculate_tax(amount):
    """Input: a single delivery's amount.
    Output: 10% tax on that delivery.
    """
    return amount * 0.10


def generate_report(total_units, failed_attempts):
    """Input: total deliveries processed, number of failed/rejected entries.
    Output: nothing (prints the summary).
    """
    print("\n=== Delivery Audit Report ===")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")


def main():
    total_inventory = 0
    deliveries_processed = 0
    failed_entries = 0

    print("--- Real-Time Delivery Auditor Started ---")

    while True:
        result = get_valid_input()

        # 'quit' signal ends the loop
        if result == "quit":
            break

        # None means the entry was invalid/rejected
        if result is None:
            failed_entries += 1
            continue

        # Valid entry: result is the stock quantity
        new_value = result

        total_inventory = process_delivery(total_inventory, new_value)
        tax = calculate_tax(new_value)
        deliveries_processed += 1

        print(f"Current Inventory Total: {total_inventory} | Tax on this delivery: {tax:.2f}")

    generate_report(deliveries_processed, failed_entries)


if __name__ == "__main__":
    main()
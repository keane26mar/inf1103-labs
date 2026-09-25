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


def load_inventory():
    """Reads previously saved inventory data from inventory.txt.
    Input: nothing
    Output: tuple (total_inventory, history_list). If the file does not
             exist yet, returns (0, []) so the program starts with an
             empty inventory instead of raising an error.
    """
    try:
        with open("inventory.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]

        if not lines:
            return 0, []

        total_inventory = int(lines[0])
        history = [int(value) for value in lines[1:]]
        return total_inventory, history

    except FileNotFoundError:
        return 0, []


def save_inventory(total_inventory, history):
    """Writes the final total and the full transaction history to inventory.txt.
    Input: total_inventory, history list
    Output: nothing (writes to file)
    """
    with open("inventory.txt", "w") as f:
        f.write(f"{total_inventory}\n")
        for entry in history:
            f.write(f"{entry}\n")

    print("Inventory successfully saved to inventory.txt")


def generate_report(total_units, failed_attempts, history):
    """Input: total deliveries processed, number of failed/rejected entries, history list.
    Output: nothing (prints the summary).
    """
    print("\n=== Delivery Audit Report ===")
    print(f"Total Deliveries Processed: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Transaction History: {history}")


def main():
    # Persistence: load whatever was saved from a previous run
    total_inventory, history = load_inventory()

    deliveries_processed = 0
    failed_entries = 0

    print("--- Real-Time Delivery Auditor Started ---")
    print(f"Loaded existing inventory total: {total_inventory}")

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
        history.append(new_value)  # History Tracking: record every valid transaction
        tax = calculate_tax(new_value)
        deliveries_processed += 1

        print(f"Current Inventory Total: {total_inventory} | Tax on this delivery: {tax:.2f}")

    # Write-Back: save the final total and full history before exiting
    save_inventory(total_inventory, history)

    generate_report(deliveries_processed, failed_entries, history)


if __name__ == "__main__":
    main()
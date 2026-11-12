class Supplier:
    """Represents a supplier associated with products (Association relationship)."""
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        self._supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    @property
    def supplier_id(self) -> str:
        return self._supplier_id

    def display_information(self) -> None:
        """Displays supplier details."""
        print(f"Supplier ID: {self._supplier_id} | Name: {self.name} | Email: {self.contact_email}")
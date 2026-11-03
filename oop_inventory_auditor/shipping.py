from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """Interface-style abstract base class for items that can be shipped[cite: 15]."""
    
    @abstractmethod
    def calculate_shipping_cost(self):
        """Calculates and returns the shipping cost for the item[cite: 15]."""
        pass
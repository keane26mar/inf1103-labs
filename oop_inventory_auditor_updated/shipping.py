from abc import ABC, abstractmethod

class CanBeShipped(ABC):
    """Interface-style abstract base class for items that can be shipped."""
    
    @abstractmethod
    def calculate_shipping_cost(self) -> float:
        """Calculates and returns the shipping cost."""
        pass
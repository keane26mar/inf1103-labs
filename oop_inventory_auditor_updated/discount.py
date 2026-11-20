from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    """Abstract base strategy for order discounts."""
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class NoDiscount(DiscountStrategy):
    """Applies no discount, returning the original total."""
    def apply(self, total: float) -> float:
        return total

class PercentageDiscount(DiscountStrategy):
    """Applies a percentage-based discount (e.g., 10% off)."""
    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)

class BulkDiscount(DiscountStrategy):
    """Applies a flat monetary discount if the total meets or exceeds a threshold."""
    def __init__(self, threshold: float, discount_amount: float):
        if threshold < 0 or discount_amount < 0:
            raise ValueError("Threshold and discount amount cannot be negative.")
        self.threshold = threshold
        self.discount_amount = discount_amount

    def apply(self, total: float) -> float:
        if total >= self.threshold:
            return max(0.0, total - self.discount_amount)
        return total

class StudentDiscount(DiscountStrategy):
    """Applies a specific student percentage discount (e.g., 15% off)."""
    def __init__(self, percentage: float = 15.0):
        if percentage < 0 or percentage > 100:
            raise ValueError("Student percentage must be between 0 and 100.")
        self.percentage = percentage

    def apply(self, total: float) -> float:
        return total * (1 - self.percentage / 100)
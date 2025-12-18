"""
Strategy Pattern - Behavioral Design Pattern
Defines a family of algorithms and makes them interchangeable
"""
from abc import ABC, abstractmethod
from src.domain.product import Product


class IPricingStrategy(ABC):
    """Abstract strategy for pricing calculations"""
    
    @abstractmethod
    def calculate_price(self, product: Product, quantity: int) -> float:
        """Calculate price based on strategy"""
        pass


class RegularPricingStrategy(IPricingStrategy):
    """Regular pricing - no discounts"""
    
    def calculate_price(self, product: Product, quantity: int) -> float:
        """Calculate regular price"""
        return product.price * quantity


class BulkDiscountStrategy(IPricingStrategy):
    """Bulk discount - discount for buying multiple items"""
    
    def __init__(self, min_quantity: int = 10, discount_percentage: float = 10.0):
        self.min_quantity = min_quantity
        self.discount_percentage = discount_percentage
    
    def calculate_price(self, product: Product, quantity: int) -> float:
        """Calculate price with bulk discount"""
        total = product.price * quantity
        if quantity >= self.min_quantity:
            total = total * (1 - self.discount_percentage / 100)
        return total


class SeasonalDiscountStrategy(IPricingStrategy):
    """Seasonal discount - fixed percentage discount"""
    
    def __init__(self, discount_percentage: float = 15.0):
        self.discount_percentage = discount_percentage
    
    def calculate_price(self, product: Product, quantity: int) -> float:
        """Calculate price with seasonal discount"""
        return product.apply_discount(self.discount_percentage) * quantity


class MembershipPricingStrategy(IPricingStrategy):
    """Membership-based pricing"""
    
    def __init__(self, membership_discount: float = 5.0):
        self.membership_discount = membership_discount
    
    def calculate_price(self, product: Product, quantity: int) -> float:
        """Calculate price with membership discount"""
        return product.apply_discount(self.membership_discount) * quantity


class PricingContext:
    """
    Context for pricing strategies
    Demonstrates Strategy Pattern usage
    """
    
    def __init__(self, strategy: IPricingStrategy = None):
        self._strategy = strategy or RegularPricingStrategy()
    
    def set_strategy(self, strategy: IPricingStrategy) -> None:
        """Change the pricing strategy"""
        self._strategy = strategy
    
    def calculate_price(self, product: Product, quantity: int) -> float:
        """Calculate price using the current strategy"""
        return self._strategy.calculate_price(product, quantity)

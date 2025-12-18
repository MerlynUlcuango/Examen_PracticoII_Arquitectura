"""
Product Entity - Domain Layer
Represents a product in the e-commerce system
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Product:
    """Product entity with business rules"""
    id: int
    name: str
    price: float
    category: str
    stock: int
    description: Optional[str] = None
    
    def is_available(self) -> bool:
        """Business rule: Product is available if in stock"""
        return self.stock > 0
    
    def can_purchase(self, quantity: int) -> bool:
        """Business rule: Can purchase if enough stock"""
        return self.stock >= quantity
    
    def reduce_stock(self, quantity: int) -> None:
        """Business rule: Reduce stock after purchase"""
        if not self.can_purchase(quantity):
            raise ValueError(f"Insufficient stock. Available: {self.stock}, Requested: {quantity}")
        self.stock -= quantity
    
    def apply_discount(self, percentage: float) -> float:
        """Business rule: Calculate discounted price"""
        if not 0 <= percentage <= 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        return self.price * (1 - percentage / 100)

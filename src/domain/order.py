"""
Order Entity - Domain Layer
Represents an order in the e-commerce system
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict
from enum import Enum


class OrderStatus(Enum):
    """Order status enumeration"""
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


@dataclass
class OrderItem:
    """Represents an item in an order"""
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    
    def get_subtotal(self) -> float:
        """Calculate subtotal for this item"""
        return self.quantity * self.unit_price


@dataclass
class Order:
    """Order entity with business rules"""
    id: int
    customer_id: int
    items: List[OrderItem] = field(default_factory=list)
    status: OrderStatus = OrderStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    discount_percentage: float = 0.0
    
    def add_item(self, item: OrderItem) -> None:
        """Add item to order"""
        self.items.append(item)
    
    def calculate_subtotal(self) -> float:
        """Calculate order subtotal"""
        return sum(item.get_subtotal() for item in self.items)
    
    def calculate_discount(self) -> float:
        """Calculate discount amount"""
        return self.calculate_subtotal() * (self.discount_percentage / 100)
    
    def calculate_total(self) -> float:
        """Business rule: Calculate order total with discount"""
        return self.calculate_subtotal() - self.calculate_discount()
    
    def can_cancel(self) -> bool:
        """Business rule: Order can be cancelled if not shipped"""
        return self.status in [OrderStatus.PENDING, OrderStatus.PROCESSING]
    
    def cancel(self) -> None:
        """Cancel the order"""
        if not self.can_cancel():
            raise ValueError(f"Cannot cancel order with status {self.status.value}")
        self.status = OrderStatus.CANCELLED
    
    def process(self) -> None:
        """Process the order"""
        if self.status != OrderStatus.PENDING:
            raise ValueError("Only pending orders can be processed")
        self.status = OrderStatus.PROCESSING
    
    def ship(self) -> None:
        """Ship the order"""
        if self.status != OrderStatus.PROCESSING:
            raise ValueError("Only processing orders can be shipped")
        self.status = OrderStatus.SHIPPED

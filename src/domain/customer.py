"""
Customer Entity - Domain Layer
Represents a customer in the e-commerce system
"""
from dataclasses import dataclass


@dataclass
class Customer:
    """Customer entity with business rules"""
    id: int
    name: str
    email: str
    membership_level: str = "BRONZE"  # BRONZE, SILVER, GOLD
    total_purchases: float = 0.0
    
    def get_discount_rate(self) -> float:
        """Business rule: Discount based on membership level"""
        discount_rates = {
            "BRONZE": 0.0,
            "SILVER": 5.0,
            "GOLD": 10.0
        }
        return discount_rates.get(self.membership_level, 0.0)
    
    def update_membership(self) -> None:
        """Business rule: Update membership based on total purchases"""
        if self.total_purchases >= 1000:
            self.membership_level = "GOLD"
        elif self.total_purchases >= 500:
            self.membership_level = "SILVER"
        else:
            self.membership_level = "BRONZE"
    
    def add_purchase(self, amount: float) -> None:
        """Business rule: Track purchases and update membership"""
        self.total_purchases += amount
        self.update_membership()

"""
Order Repository - Data Access Layer
"""
from typing import List, Optional, Dict
from src.domain.order import Order, OrderStatus
from src.repository.base_repository import IRepository


class OrderRepository(IRepository[Order]):
    """Order repository implementation using in-memory storage"""
    
    def __init__(self):
        self._orders: Dict[int, Order] = {}
        self._next_id = 1
    
    def add(self, entity: Order) -> Order:
        """Add a new order"""
        if entity.id == 0:
            entity.id = self._next_id
            self._next_id += 1
        self._orders[entity.id] = entity
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[Order]:
        """Get order by ID"""
        return self._orders.get(entity_id)
    
    def get_all(self) -> List[Order]:
        """Get all orders"""
        return list(self._orders.values())
    
    def update(self, entity: Order) -> Order:
        """Update an order"""
        if entity.id not in self._orders:
            raise ValueError(f"Order with ID {entity.id} not found")
        self._orders[entity.id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete an order"""
        if entity_id in self._orders:
            del self._orders[entity_id]
            return True
        return False
    
    def find_by_customer(self, customer_id: int) -> List[Order]:
        """Find orders by customer ID"""
        return [o for o in self._orders.values() if o.customer_id == customer_id]
    
    def find_by_status(self, status: OrderStatus) -> List[Order]:
        """Find orders by status"""
        return [o for o in self._orders.values() if o.status == status]

"""
Customer Repository - Data Access Layer
"""
from typing import List, Optional, Dict
from src.domain.customer import Customer
from src.repository.base_repository import IRepository


class CustomerRepository(IRepository[Customer]):
    """Customer repository implementation using in-memory storage"""
    
    def __init__(self):
        self._customers: Dict[int, Customer] = {}
        self._next_id = 1
    
    def add(self, entity: Customer) -> Customer:
        """Add a new customer"""
        if entity.id == 0:
            entity.id = self._next_id
            self._next_id += 1
        self._customers[entity.id] = entity
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[Customer]:
        """Get customer by ID"""
        return self._customers.get(entity_id)
    
    def get_all(self) -> List[Customer]:
        """Get all customers"""
        return list(self._customers.values())
    
    def update(self, entity: Customer) -> Customer:
        """Update a customer"""
        if entity.id not in self._customers:
            raise ValueError(f"Customer with ID {entity.id} not found")
        self._customers[entity.id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete a customer"""
        if entity_id in self._customers:
            del self._customers[entity_id]
            return True
        return False
    
    def find_by_email(self, email: str) -> Optional[Customer]:
        """Find customer by email"""
        for customer in self._customers.values():
            if customer.email == email:
                return customer
        return None

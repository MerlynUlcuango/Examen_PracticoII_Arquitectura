"""
Product Repository - Data Access Layer
Demonstrates Dependency Inversion Principle (SOLID)
"""
from typing import List, Optional, Dict
from src.domain.product import Product
from src.repository.base_repository import IRepository


class ProductRepository(IRepository[Product]):
    """
    Product repository implementation using in-memory storage
    In production, this would connect to a database
    """
    
    def __init__(self):
        self._products: Dict[int, Product] = {}
        self._next_id = 1
    
    def add(self, entity: Product) -> Product:
        """Add a new product"""
        if entity.id == 0:
            entity.id = self._next_id
            self._next_id += 1
        self._products[entity.id] = entity
        return entity
    
    def get_by_id(self, entity_id: int) -> Optional[Product]:
        """Get product by ID"""
        return self._products.get(entity_id)
    
    def get_all(self) -> List[Product]:
        """Get all products"""
        return list(self._products.values())
    
    def update(self, entity: Product) -> Product:
        """Update a product"""
        if entity.id not in self._products:
            raise ValueError(f"Product with ID {entity.id} not found")
        self._products[entity.id] = entity
        return entity
    
    def delete(self, entity_id: int) -> bool:
        """Delete a product"""
        if entity_id in self._products:
            del self._products[entity_id]
            return True
        return False
    
    def find_by_category(self, category: str) -> List[Product]:
        """Find products by category"""
        return [p for p in self._products.values() if p.category == category]
    
    def find_available(self) -> List[Product]:
        """Find available products"""
        return [p for p in self._products.values() if p.is_available()]

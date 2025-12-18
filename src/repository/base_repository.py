"""
Base Repository Interface
Demonstrates Interface Segregation Principle (SOLID)
"""
from abc import ABC, abstractmethod
from typing import List, Optional, TypeVar, Generic

T = TypeVar('T')


class IRepository(ABC, Generic[T]):
    """Generic repository interface"""
    
    @abstractmethod
    def add(self, entity: T) -> T:
        """Add a new entity"""
        pass
    
    @abstractmethod
    def get_by_id(self, entity_id: int) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[T]:
        """Get all entities"""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Update an entity"""
        pass
    
    @abstractmethod
    def delete(self, entity_id: int) -> bool:
        """Delete an entity"""
        pass

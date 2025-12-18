"""
Factory Pattern - Creational Design Pattern
Used to create objects without specifying the exact class
"""
from abc import ABC, abstractmethod
from typing import Dict, Type
from src.domain.product import Product


class IProductFactory(ABC):
    """Abstract factory for creating products"""
    
    @abstractmethod
    def create_product(self, name: str, price: float, stock: int) -> Product:
        """Create a product"""
        pass


class ElectronicsFactory(IProductFactory):
    """Factory for creating electronics products"""
    
    def create_product(self, name: str, price: float, stock: int) -> Product:
        """Create an electronics product"""
        return Product(
            id=0,
            name=name,
            price=price,
            category="ELECTRONICS",
            stock=stock,
            description=f"Electronics product: {name}"
        )


class ClothingFactory(IProductFactory):
    """Factory for creating clothing products"""
    
    def create_product(self, name: str, price: float, stock: int) -> Product:
        """Create a clothing product"""
        return Product(
            id=0,
            name=name,
            price=price,
            category="CLOTHING",
            stock=stock,
            description=f"Clothing product: {name}"
        )


class BooksFactory(IProductFactory):
    """Factory for creating book products"""
    
    def create_product(self, name: str, price: float, stock: int) -> Product:
        """Create a book product"""
        return Product(
            id=0,
            name=name,
            price=price,
            category="BOOKS",
            stock=stock,
            description=f"Book: {name}"
        )


class ProductFactoryRegistry:
    """
    Registry for product factories
    Demonstrates Factory Pattern with Registry
    """
    
    def __init__(self):
        self._factories: Dict[str, IProductFactory] = {}
    
    def register_factory(self, category: str, factory: IProductFactory) -> None:
        """Register a factory for a category"""
        self._factories[category] = factory
    
    def create_product(self, category: str, name: str, price: float, stock: int) -> Product:
        """Create a product using the registered factory"""
        factory = self._factories.get(category)
        if not factory:
            raise ValueError(f"No factory registered for category: {category}")
        return factory.create_product(name, price, stock)


# Singleton instance of the registry
_registry_instance = None


def get_product_factory_registry() -> ProductFactoryRegistry:
    """Get the singleton instance of the product factory registry"""
    global _registry_instance
    if _registry_instance is None:
        _registry_instance = ProductFactoryRegistry()
        # Register default factories
        _registry_instance.register_factory("ELECTRONICS", ElectronicsFactory())
        _registry_instance.register_factory("CLOTHING", ClothingFactory())
        _registry_instance.register_factory("BOOKS", BooksFactory())
    return _registry_instance

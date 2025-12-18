"""
Product Service - Application Layer
Manages product-related operations
"""
from typing import List, Optional
from src.domain.product import Product
from src.repository.product_repository import ProductRepository
from src.patterns.factory_pattern import get_product_factory_registry


class ProductService:
    """Service for managing products"""
    
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
        self.factory_registry = get_product_factory_registry()
    
    def create_product(
        self, 
        name: str, 
        price: float, 
        category: str, 
        stock: int,
        description: str = None
    ) -> Product:
        """Create a new product using factory pattern"""
        try:
            # Try to use factory
            product = self.factory_registry.create_product(category, name, price, stock)
        except ValueError:
            # Fallback to direct creation if no factory registered
            product = Product(
                id=0,
                name=name,
                price=price,
                category=category,
                stock=stock,
                description=description
            )
        
        return self.product_repo.add(product)
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        return self.product_repo.get_by_id(product_id)
    
    def get_all_products(self) -> List[Product]:
        """Get all products"""
        return self.product_repo.get_all()
    
    def get_available_products(self) -> List[Product]:
        """Get all available products"""
        return self.product_repo.find_available()
    
    def get_products_by_category(self, category: str) -> List[Product]:
        """Get products by category"""
        return self.product_repo.find_by_category(category)
    
    def update_stock(self, product_id: int, new_stock: int) -> Product:
        """Update product stock"""
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        product.stock = new_stock
        return self.product_repo.update(product)
    
    def delete_product(self, product_id: int) -> bool:
        """Delete a product"""
        return self.product_repo.delete(product_id)

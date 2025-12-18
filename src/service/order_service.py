"""
Order Service - Application Layer
Orchestrates business logic and coordinates between layers
Demonstrates Single Responsibility Principle
"""
from typing import List, Optional
from src.domain.order import Order, OrderItem, OrderStatus
from src.domain.product import Product
from src.domain.customer import Customer
from src.repository.order_repository import OrderRepository
from src.repository.product_repository import ProductRepository
from src.repository.customer_repository import CustomerRepository
from src.patterns.observer_pattern import OrderSubject
from src.patterns.strategy_pattern import PricingContext, IPricingStrategy


class OrderService:
    """
    Service for managing orders
    Demonstrates Service Layer pattern and orchestration
    """
    
    def __init__(
        self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        customer_repo: CustomerRepository,
        order_subject: OrderSubject = None
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.customer_repo = customer_repo
        self.order_subject = order_subject or OrderSubject()
        self.pricing_context = PricingContext()
    
    def create_order(self, customer_id: int) -> Order:
        """Create a new order for a customer"""
        customer = self.customer_repo.get_by_id(customer_id)
        if not customer:
            raise ValueError(f"Customer with ID {customer_id} not found")
        
        order = Order(id=0, customer_id=customer_id)
        order.discount_percentage = customer.get_discount_rate()
        
        saved_order = self.order_repo.add(order)
        self.order_subject.notify(saved_order)
        return saved_order
    
    def add_item_to_order(
        self, 
        order_id: int, 
        product_id: int, 
        quantity: int,
        pricing_strategy: IPricingStrategy = None
    ) -> Order:
        """Add an item to an order"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")
        
        if order.status != OrderStatus.PENDING:
            raise ValueError("Can only add items to pending orders")
        
        product = self.product_repo.get_by_id(product_id)
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        if not product.can_purchase(quantity):
            raise ValueError(f"Insufficient stock for product {product.name}")
        
        # Use pricing strategy if provided
        if pricing_strategy:
            self.pricing_context.set_strategy(pricing_strategy)
            unit_price = self.pricing_context.calculate_price(product, 1)
        else:
            unit_price = product.price
        
        # Reduce stock
        product.reduce_stock(quantity)
        self.product_repo.update(product)
        
        # Add item to order
        item = OrderItem(
            product_id=product_id,
            product_name=product.name,
            quantity=quantity,
            unit_price=unit_price
        )
        order.add_item(item)
        
        updated_order = self.order_repo.update(order)
        self.order_subject.notify(updated_order)
        return updated_order
    
    def process_order(self, order_id: int) -> Order:
        """Process an order"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")
        
        if len(order.items) == 0:
            raise ValueError("Cannot process an empty order")
        
        order.process()
        
        # Update customer's total purchases
        customer = self.customer_repo.get_by_id(order.customer_id)
        if customer:
            customer.add_purchase(order.calculate_total())
            self.customer_repo.update(customer)
        
        updated_order = self.order_repo.update(order)
        self.order_subject.notify(updated_order)
        return updated_order
    
    def ship_order(self, order_id: int) -> Order:
        """Ship an order"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")
        
        order.ship()
        updated_order = self.order_repo.update(order)
        self.order_subject.notify(updated_order)
        return updated_order
    
    def cancel_order(self, order_id: int) -> Order:
        """Cancel an order"""
        order = self.order_repo.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with ID {order_id} not found")
        
        order.cancel()
        updated_order = self.order_repo.update(order)
        self.order_subject.notify(updated_order)
        return updated_order
    
    def get_customer_orders(self, customer_id: int) -> List[Order]:
        """Get all orders for a customer"""
        return self.order_repo.find_by_customer(customer_id)
    
    def get_order(self, order_id: int) -> Optional[Order]:
        """Get an order by ID"""
        return self.order_repo.get_by_id(order_id)

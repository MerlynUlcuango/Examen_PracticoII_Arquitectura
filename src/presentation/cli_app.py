"""
CLI Application - Presentation Layer
Demonstrates MVC/MVP pattern with separation of concerns
"""
from typing import Optional
from src.service.order_service import OrderService
from src.service.product_service import ProductService
from src.service.customer_service import CustomerService
from src.repository.order_repository import OrderRepository
from src.repository.product_repository import ProductRepository
from src.repository.customer_repository import CustomerRepository
from src.patterns.observer_pattern import (
    OrderSubject, EmailNotificationObserver, 
    InventoryObserver, AnalyticsObserver
)
from src.patterns.strategy_pattern import (
    BulkDiscountStrategy, SeasonalDiscountStrategy, 
    MembershipPricingStrategy
)
from src.patterns.singleton_pattern import get_config


class ECommerceApp:
    """
    Main application class - Presentation Layer
    Demonstrates Dependency Injection and Inversion of Control
    """
    
    def __init__(self):
        # Initialize repositories
        self.product_repo = ProductRepository()
        self.customer_repo = CustomerRepository()
        self.order_repo = OrderRepository()
        
        # Initialize observer pattern
        self.order_subject = OrderSubject()
        self.order_subject.attach(EmailNotificationObserver())
        self.order_subject.attach(InventoryObserver())
        self.order_subject.attach(AnalyticsObserver())
        
        # Initialize services
        self.product_service = ProductService(self.product_repo)
        self.customer_service = CustomerService(self.customer_repo)
        self.order_service = OrderService(
            self.order_repo,
            self.product_repo,
            self.customer_repo,
            self.order_subject
        )
        
        # Get configuration
        self.config = get_config()
    
    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "=" * 60)
        print(f"Welcome to {self.config.get('app_name')}")
        print(f"Version: {self.config.get('version')}")
        print("=" * 60)
    
    def display_menu(self):
        """Display main menu"""
        print("\n--- Main Menu ---")
        print("1. Product Management")
        print("2. Customer Management")
        print("3. Order Management")
        print("4. View System Info")
        print("5. Exit")
    
    def display_product_menu(self):
        """Display product management menu"""
        print("\n--- Product Management ---")
        print("1. Create Product")
        print("2. View All Products")
        print("3. View Available Products")
        print("4. View Products by Category")
        print("5. Back to Main Menu")
    
    def display_customer_menu(self):
        """Display customer management menu"""
        print("\n--- Customer Management ---")
        print("1. Create Customer")
        print("2. View All Customers")
        print("3. View Customer Details")
        print("4. Back to Main Menu")
    
    def display_order_menu(self):
        """Display order management menu"""
        print("\n--- Order Management ---")
        print("1. Create Order")
        print("2. Add Item to Order")
        print("3. Process Order")
        print("4. View Order")
        print("5. View Customer Orders")
        print("6. Cancel Order")
        print("7. Back to Main Menu")
    
    def create_sample_data(self):
        """Create sample data for demonstration"""
        print("\n--- Creating Sample Data ---")
        
        # Create products
        products = [
            ("Laptop", 999.99, "ELECTRONICS", 10),
            ("Smartphone", 699.99, "ELECTRONICS", 15),
            ("T-Shirt", 29.99, "CLOTHING", 50),
            ("Jeans", 59.99, "CLOTHING", 30),
            ("Python Book", 49.99, "BOOKS", 20),
        ]
        
        for name, price, category, stock in products:
            self.product_service.create_product(name, price, category, stock)
            print(f"Created product: {name}")
        
        # Create customers
        customers = [
            ("John Doe", "john@example.com"),
            ("Jane Smith", "jane@example.com"),
            ("Bob Johnson", "bob@example.com"),
        ]
        
        for name, email in customers:
            self.customer_service.create_customer(name, email)
            print(f"Created customer: {name}")
        
        print("\nSample data created successfully!")
    
    def display_products(self):
        """Display all products"""
        products = self.product_service.get_all_products()
        if not products:
            print("\nNo products found.")
            return
        
        print("\n--- Products ---")
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Category':<15} {'Stock':<10}")
        print("-" * 60)
        for product in products:
            print(f"{product.id:<5} {product.name:<20} ${product.price:<9.2f} "
                  f"{product.category:<15} {product.stock:<10}")
    
    def display_customers(self):
        """Display all customers"""
        customers = self.customer_service.get_all_customers()
        if not customers:
            print("\nNo customers found.")
            return
        
        print("\n--- Customers ---")
        print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Level':<10} {'Purchases':<10}")
        print("-" * 75)
        for customer in customers:
            print(f"{customer.id:<5} {customer.name:<20} {customer.email:<30} "
                  f"{customer.membership_level:<10} ${customer.total_purchases:<9.2f}")
    
    def demonstrate_patterns(self):
        """Demonstrate design patterns"""
        print("\n" + "=" * 60)
        print("Design Patterns Demonstration")
        print("=" * 60)
        
        # 1. Factory Pattern
        print("\n1. FACTORY PATTERN - Creating products by category")
        laptop = self.product_service.create_product(
            "Gaming Laptop", 1499.99, "ELECTRONICS", 5
        )
        print(f"Created: {laptop.name} in {laptop.category} category")
        
        # 2. Strategy Pattern
        print("\n2. STRATEGY PATTERN - Different pricing strategies")
        product = self.product_service.get_product(1)
        if product:
            from src.patterns.strategy_pattern import (
                RegularPricingStrategy, BulkDiscountStrategy,
                SeasonalDiscountStrategy, PricingContext
            )
            
            context = PricingContext()
            
            context.set_strategy(RegularPricingStrategy())
            regular_price = context.calculate_price(product, 5)
            print(f"Regular price for 5 items: ${regular_price:.2f}")
            
            context.set_strategy(BulkDiscountStrategy(min_quantity=3, discount_percentage=10))
            bulk_price = context.calculate_price(product, 5)
            print(f"Bulk discount price for 5 items: ${bulk_price:.2f}")
            
            context.set_strategy(SeasonalDiscountStrategy(discount_percentage=15))
            seasonal_price = context.calculate_price(product, 5)
            print(f"Seasonal discount price for 5 items: ${seasonal_price:.2f}")
        
        # 3. Observer Pattern
        print("\n3. OBSERVER PATTERN - Order notifications")
        print("Creating and processing an order...")
        customer = self.customer_service.get_customer(1)
        if customer:
            order = self.order_service.create_order(customer.id)
            print(f"\nOrder #{order.id} created")
            
            product = self.product_service.get_product(1)
            if product:
                self.order_service.add_item_to_order(order.id, product.id, 2)
                print(f"\nAdded {product.name} to order")
                
                self.order_service.process_order(order.id)
                print(f"\nOrder processed")
        
        # 4. Singleton Pattern
        print("\n4. SINGLETON PATTERN - Configuration manager")
        config1 = get_config()
        config2 = get_config()
        print(f"Same instance? {config1 is config2}")
        print(f"App Name: {config1.get('app_name')}")
        print(f"Version: {config1.get('version')}")
    
    def run_demo(self):
        """Run a complete demonstration"""
        self.display_welcome()
        
        print("\n--- Architecture Demonstration ---")
        print("\nThis application demonstrates:")
        print("✓ Layered Architecture (Domain, Repository, Service, Presentation)")
        print("✓ SOLID Principles")
        print("✓ Design Patterns (Factory, Strategy, Observer, Singleton)")
        print("✓ Clean Code Practices")
        print("✓ Dependency Injection")
        
        # Create sample data
        self.create_sample_data()
        
        # Display data
        self.display_products()
        self.display_customers()
        
        # Demonstrate patterns
        self.demonstrate_patterns()
        
        print("\n" + "=" * 60)
        print("Architecture Demonstration Complete!")
        print("=" * 60)


def main():
    """Main entry point"""
    app = ECommerceApp()
    app.run_demo()


if __name__ == "__main__":
    main()

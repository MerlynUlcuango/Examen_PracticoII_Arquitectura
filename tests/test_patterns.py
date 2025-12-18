"""
Tests for Design Patterns
Demonstrates testing of pattern implementations
"""
import unittest
from src.patterns.factory_pattern import (
    ElectronicsFactory, ClothingFactory, BooksFactory,
    ProductFactoryRegistry, get_product_factory_registry
)
from src.patterns.strategy_pattern import (
    RegularPricingStrategy, BulkDiscountStrategy,
    SeasonalDiscountStrategy, PricingContext
)
from src.patterns.singleton_pattern import ConfigurationManager, get_config
from src.patterns.observer_pattern import (
    OrderSubject, EmailNotificationObserver,
    InventoryObserver, AnalyticsObserver
)
from src.domain.product import Product
from src.domain.order import Order


class TestFactoryPattern(unittest.TestCase):
    """Test cases for Factory Pattern"""
    
    def test_electronics_factory(self):
        """Test electronics factory creates correct product"""
        factory = ElectronicsFactory()
        product = factory.create_product("Laptop", 999.99, 10)
        self.assertEqual(product.category, "ELECTRONICS")
        self.assertEqual(product.name, "Laptop")
    
    def test_clothing_factory(self):
        """Test clothing factory creates correct product"""
        factory = ClothingFactory()
        product = factory.create_product("T-Shirt", 29.99, 50)
        self.assertEqual(product.category, "CLOTHING")
    
    def test_factory_registry(self):
        """Test factory registry"""
        registry = ProductFactoryRegistry()
        registry.register_factory("ELECTRONICS", ElectronicsFactory())
        product = registry.create_product("ELECTRONICS", "Phone", 699.99, 15)
        self.assertEqual(product.category, "ELECTRONICS")
    
    def test_singleton_registry(self):
        """Test singleton registry returns same instance"""
        registry1 = get_product_factory_registry()
        registry2 = get_product_factory_registry()
        self.assertIs(registry1, registry2)


class TestStrategyPattern(unittest.TestCase):
    """Test cases for Strategy Pattern"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.product = Product(1, "Test", 100.0, "TEST", 10)
        self.context = PricingContext()
    
    def test_regular_pricing(self):
        """Test regular pricing strategy"""
        strategy = RegularPricingStrategy()
        price = strategy.calculate_price(self.product, 5)
        self.assertEqual(price, 500.0)
    
    def test_bulk_discount_strategy(self):
        """Test bulk discount strategy"""
        strategy = BulkDiscountStrategy(min_quantity=3, discount_percentage=10)
        price = strategy.calculate_price(self.product, 5)
        self.assertEqual(price, 450.0)
    
    def test_bulk_discount_below_minimum(self):
        """Test bulk discount not applied below minimum"""
        strategy = BulkDiscountStrategy(min_quantity=10, discount_percentage=10)
        price = strategy.calculate_price(self.product, 5)
        self.assertEqual(price, 500.0)
    
    def test_seasonal_discount(self):
        """Test seasonal discount strategy"""
        strategy = SeasonalDiscountStrategy(discount_percentage=20)
        price = strategy.calculate_price(self.product, 5)
        self.assertEqual(price, 400.0)
    
    def test_context_switch_strategy(self):
        """Test switching strategies in context"""
        self.context.set_strategy(RegularPricingStrategy())
        regular = self.context.calculate_price(self.product, 5)
        
        # Use bulk discount with minimum quantity met
        self.context.set_strategy(BulkDiscountStrategy(min_quantity=3, discount_percentage=10))
        bulk = self.context.calculate_price(self.product, 5)
        
        self.assertNotEqual(regular, bulk)


class TestObserverPattern(unittest.TestCase):
    """Test cases for Observer Pattern"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.subject = OrderSubject()
        self.order = Order(1, 1)
    
    def test_attach_observer(self):
        """Test attaching an observer"""
        observer = EmailNotificationObserver()
        self.subject.attach(observer)
        # Verify no error when notifying
        self.subject.notify(self.order)
    
    def test_detach_observer(self):
        """Test detaching an observer"""
        observer = EmailNotificationObserver()
        self.subject.attach(observer)
        self.subject.detach(observer)
        # Verify no error when notifying
        self.subject.notify(self.order)
    
    def test_multiple_observers(self):
        """Test multiple observers receive notifications"""
        observers = [
            EmailNotificationObserver(),
            InventoryObserver(),
            AnalyticsObserver()
        ]
        for observer in observers:
            self.subject.attach(observer)
        
        # Should not raise error
        self.subject.notify(self.order)


class TestSingletonPattern(unittest.TestCase):
    """Test cases for Singleton Pattern"""
    
    def test_singleton_same_instance(self):
        """Test singleton returns same instance"""
        config1 = ConfigurationManager()
        config2 = ConfigurationManager()
        self.assertIs(config1, config2)
    
    def test_get_config_function(self):
        """Test get_config returns singleton"""
        config1 = get_config()
        config2 = get_config()
        self.assertIs(config1, config2)
    
    def test_configuration_persistence(self):
        """Test configuration persists across instances"""
        config1 = get_config()
        config1.set('test_key', 'test_value')
        
        config2 = get_config()
        self.assertEqual(config2.get('test_key'), 'test_value')


if __name__ == '__main__':
    unittest.main()

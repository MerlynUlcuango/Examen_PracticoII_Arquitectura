"""
Unit Tests for Domain Layer
Demonstrates testing of business logic
"""
import unittest
from src.domain.product import Product
from src.domain.customer import Customer
from src.domain.order import Order, OrderItem, OrderStatus


class TestProduct(unittest.TestCase):
    """Test cases for Product entity"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.product = Product(
            id=1,
            name="Test Product",
            price=100.0,
            category="TEST",
            stock=10
        )
    
    def test_is_available_with_stock(self):
        """Test product is available when in stock"""
        self.assertTrue(self.product.is_available())
    
    def test_is_not_available_without_stock(self):
        """Test product is not available when out of stock"""
        self.product.stock = 0
        self.assertFalse(self.product.is_available())
    
    def test_can_purchase_sufficient_stock(self):
        """Test can purchase with sufficient stock"""
        self.assertTrue(self.product.can_purchase(5))
    
    def test_cannot_purchase_insufficient_stock(self):
        """Test cannot purchase with insufficient stock"""
        self.assertFalse(self.product.can_purchase(15))
    
    def test_reduce_stock_success(self):
        """Test reducing stock successfully"""
        initial_stock = self.product.stock
        self.product.reduce_stock(3)
        self.assertEqual(self.product.stock, initial_stock - 3)
    
    def test_reduce_stock_insufficient(self):
        """Test reducing stock with insufficient quantity raises error"""
        with self.assertRaises(ValueError):
            self.product.reduce_stock(20)
    
    def test_apply_discount(self):
        """Test applying discount to product"""
        discounted_price = self.product.apply_discount(10)
        self.assertEqual(discounted_price, 90.0)
    
    def test_apply_invalid_discount(self):
        """Test invalid discount percentage raises error"""
        with self.assertRaises(ValueError):
            self.product.apply_discount(150)


class TestCustomer(unittest.TestCase):
    """Test cases for Customer entity"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.customer = Customer(
            id=1,
            name="Test Customer",
            email="test@example.com"
        )
    
    def test_initial_membership_level(self):
        """Test initial membership level is BRONZE"""
        self.assertEqual(self.customer.membership_level, "BRONZE")
    
    def test_bronze_discount_rate(self):
        """Test BRONZE membership has 0% discount"""
        self.assertEqual(self.customer.get_discount_rate(), 0.0)
    
    def test_upgrade_to_silver(self):
        """Test upgrading to SILVER membership"""
        self.customer.add_purchase(500.0)
        self.assertEqual(self.customer.membership_level, "SILVER")
        self.assertEqual(self.customer.get_discount_rate(), 5.0)
    
    def test_upgrade_to_gold(self):
        """Test upgrading to GOLD membership"""
        self.customer.add_purchase(1000.0)
        self.assertEqual(self.customer.membership_level, "GOLD")
        self.assertEqual(self.customer.get_discount_rate(), 10.0)
    
    def test_total_purchases_tracking(self):
        """Test total purchases are tracked correctly"""
        self.customer.add_purchase(100.0)
        self.customer.add_purchase(200.0)
        self.assertEqual(self.customer.total_purchases, 300.0)


class TestOrder(unittest.TestCase):
    """Test cases for Order entity"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.order = Order(id=1, customer_id=1)
    
    def test_initial_status(self):
        """Test initial order status is PENDING"""
        self.assertEqual(self.order.status, OrderStatus.PENDING)
    
    def test_add_item(self):
        """Test adding item to order"""
        item = OrderItem(
            product_id=1,
            product_name="Test Product",
            quantity=2,
            unit_price=50.0
        )
        self.order.add_item(item)
        self.assertEqual(len(self.order.items), 1)
    
    def test_calculate_subtotal(self):
        """Test calculating order subtotal"""
        item1 = OrderItem(1, "Product 1", 2, 50.0)
        item2 = OrderItem(2, "Product 2", 1, 100.0)
        self.order.add_item(item1)
        self.order.add_item(item2)
        self.assertEqual(self.order.calculate_subtotal(), 200.0)
    
    def test_calculate_total_with_discount(self):
        """Test calculating total with discount"""
        item = OrderItem(1, "Product", 2, 100.0)
        self.order.add_item(item)
        self.order.discount_percentage = 10.0
        self.assertEqual(self.order.calculate_total(), 180.0)
    
    def test_process_order(self):
        """Test processing order changes status"""
        self.order.process()
        self.assertEqual(self.order.status, OrderStatus.PROCESSING)
    
    def test_ship_order(self):
        """Test shipping order"""
        self.order.process()
        self.order.ship()
        self.assertEqual(self.order.status, OrderStatus.SHIPPED)
    
    def test_cancel_pending_order(self):
        """Test cancelling pending order"""
        self.assertTrue(self.order.can_cancel())
        self.order.cancel()
        self.assertEqual(self.order.status, OrderStatus.CANCELLED)
    
    def test_cannot_cancel_shipped_order(self):
        """Test cannot cancel shipped order"""
        self.order.process()
        self.order.ship()
        self.assertFalse(self.order.can_cancel())


if __name__ == '__main__':
    unittest.main()

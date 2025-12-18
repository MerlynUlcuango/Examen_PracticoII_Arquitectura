# Ejemplos de Uso

## Ejemplo 1: Ejecutar la Demostración Completa

```bash
python -m src.presentation.cli_app
```

Esto ejecutará una demostración completa que incluye:
- Creación de productos de ejemplo
- Creación de clientes
- Demostración de todos los patrones de diseño
- Procesamiento de pedidos con observadores

## Ejemplo 2: Usar el Sistema Programáticamente

```python
from src.repository.product_repository import ProductRepository
from src.repository.customer_repository import CustomerRepository
from src.repository.order_repository import OrderRepository
from src.service.product_service import ProductService
from src.service.customer_service import CustomerService
from src.service.order_service import OrderService
from src.patterns.observer_pattern import (
    OrderSubject, EmailNotificationObserver, InventoryObserver
)

# Inicializar repositorios
product_repo = ProductRepository()
customer_repo = CustomerRepository()
order_repo = OrderRepository()

# Inicializar servicios
product_service = ProductService(product_repo)
customer_service = CustomerService(customer_repo)

# Configurar observadores
order_subject = OrderSubject()
order_subject.attach(EmailNotificationObserver())
order_subject.attach(InventoryObserver())

order_service = OrderService(
    order_repo, 
    product_repo, 
    customer_repo, 
    order_subject
)

# Crear un producto
product = product_service.create_product(
    name="Laptop",
    price=999.99,
    category="ELECTRONICS",
    stock=10
)

# Crear un cliente
customer = customer_service.create_customer(
    name="Juan Pérez",
    email="juan@example.com"
)

# Crear un pedido
order = order_service.create_order(customer.id)

# Agregar items al pedido
order = order_service.add_item_to_order(order.id, product.id, 2)

# Procesar el pedido (notifica a observadores)
order = order_service.process_order(order.id)

print(f"Pedido #{order.id} procesado. Total: ${order.calculate_total():.2f}")
```

## Ejemplo 3: Usar Diferentes Estrategias de Precios

```python
from src.patterns.strategy_pattern import (
    BulkDiscountStrategy, 
    SeasonalDiscountStrategy,
    PricingContext
)
from src.domain.product import Product

# Crear producto
product = Product(1, "Laptop", 1000.0, "ELECTRONICS", 10)

# Usar estrategia de descuento por volumen
context = PricingContext()
context.set_strategy(BulkDiscountStrategy(min_quantity=5, discount_percentage=15))
price = context.calculate_price(product, 10)
print(f"Precio con descuento por volumen: ${price:.2f}")

# Cambiar a descuento de temporada
context.set_strategy(SeasonalDiscountStrategy(discount_percentage=20))
price = context.calculate_price(product, 10)
print(f"Precio con descuento de temporada: ${price:.2f}")
```

## Ejemplo 4: Usar Factory Pattern

```python
from src.patterns.factory_pattern import get_product_factory_registry

# Obtener el registro de fábricas
registry = get_product_factory_registry()

# Crear productos de diferentes categorías
laptop = registry.create_product("ELECTRONICS", "MacBook Pro", 1999.99, 5)
shirt = registry.create_product("CLOTHING", "Camisa", 49.99, 100)
book = registry.create_product("BOOKS", "Clean Code", 39.99, 50)

print(f"{laptop.name} - Categoría: {laptop.category}")
print(f"{shirt.name} - Categoría: {shirt.category}")
print(f"{book.name} - Categoría: {book.category}")
```

## Ejemplo 5: Sistema de Membresías

```python
from src.domain.customer import Customer

# Crear cliente
customer = Customer(1, "María García", "maria@example.com")

print(f"Nivel inicial: {customer.membership_level}")
print(f"Descuento: {customer.get_discount_rate()}%")

# Simular compras
customer.add_purchase(300.0)
print(f"Después de $300: {customer.membership_level} - {customer.get_discount_rate()}%")

customer.add_purchase(300.0)
print(f"Después de $600: {customer.membership_level} - {customer.get_discount_rate()}%")

customer.add_purchase(500.0)
print(f"Después de $1100: {customer.membership_level} - {customer.get_discount_rate()}%")
```

## Ejemplo 6: Gestión de Estados de Pedidos

```python
from src.domain.order import Order, OrderItem, OrderStatus

# Crear pedido
order = Order(id=1, customer_id=1)

# Agregar items
item1 = OrderItem(1, "Laptop", 2, 999.99)
item2 = OrderItem(2, "Mouse", 1, 29.99)
order.add_item(item1)
order.add_item(item2)

# Verificar estados
print(f"Estado inicial: {order.status.value}")
print(f"Subtotal: ${order.calculate_subtotal():.2f}")

# Procesar pedido
order.process()
print(f"Estado después de procesar: {order.status.value}")

# Enviar pedido
order.ship()
print(f"Estado después de enviar: {order.status.value}")

# Intentar cancelar pedido enviado
if order.can_cancel():
    order.cancel()
else:
    print("No se puede cancelar un pedido enviado")
```

## Ejemplo 7: Testing

```bash
# Ejecutar todos los tests
python -m unittest discover tests -v

# Ejecutar tests de dominio
python -m unittest tests.test_domain -v

# Ejecutar tests de patrones
python -m unittest tests.test_patterns -v

# Ejecutar un test específico
python -m unittest tests.test_domain.TestProduct.test_apply_discount
```

## Ejemplo 8: Extender el Sistema

### Agregar una nueva estrategia de precios

```python
from src.patterns.strategy_pattern import IPricingStrategy
from src.domain.product import Product

class BlackFridayStrategy(IPricingStrategy):
    """Descuento especial para Black Friday"""
    
    def calculate_price(self, product: Product, quantity: int) -> float:
        # 50% de descuento en todo
        return product.price * quantity * 0.5

# Usar la nueva estrategia
context = PricingContext()
context.set_strategy(BlackFridayStrategy())
price = context.calculate_price(product, 5)
```

### Agregar un nuevo observador

```python
from src.patterns.observer_pattern import IOrderObserver
from src.domain.order import Order

class LoggingObserver(IOrderObserver):
    """Observador que registra eventos en un archivo"""
    
    def update(self, order: Order) -> None:
        with open('orders.log', 'a') as f:
            f.write(f"Order #{order.id} - Status: {order.status.value}\n")

# Usar el nuevo observador
order_subject.attach(LoggingObserver())
```

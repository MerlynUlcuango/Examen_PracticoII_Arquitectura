# Documentación de Arquitectura

## Diagrama de Arquitectura en Capas

```
┌─────────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                           │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              CLI Application (cli_app.py)                 │  │
│  │  - Interfaz de usuario                                    │  │
│  │  - Orquestación de alto nivel                            │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                              │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │   Product   │  │   Customer   │  │   Order Service     │   │
│  │   Service   │  │   Service    │  │  - Coordina lógica  │   │
│  │             │  │              │  │  - Usa Observer     │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                    REPOSITORY LAYER                             │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │   Product   │  │   Customer   │  │   Order Repository  │   │
│  │ Repository  │  │ Repository   │  │  - Acceso a datos   │   │
│  │             │  │              │  │  - Implementa CRUD  │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
│                              ↓                                  │
│         ┌────────────────────────────────────────┐             │
│         │   Base Repository Interface (IRepo)    │             │
│         └────────────────────────────────────────┘             │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      DOMAIN LAYER                               │
│                                                                 │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │   Product   │  │   Customer   │  │       Order         │   │
│  │   Entity    │  │   Entity     │  │      Entity         │   │
│  │  - Reglas   │  │  - Reglas    │  │   - Reglas          │   │
│  │  - Validación│ │  - Membresía │  │   - Estados         │   │
│  └─────────────┘  └──────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    DESIGN PATTERNS                              │
│                                                                 │
│  Factory ────→ Crea productos por categoría                    │
│  Strategy ───→ Diferentes estrategias de precios               │
│  Observer ───→ Notifica eventos de pedidos                     │
│  Singleton ──→ Configuración única del sistema                 │
└─────────────────────────────────────────────────────────────────┘
```

## Flujo de Datos

### Crear y Procesar un Pedido

```
Usuario (CLI)
    ↓
OrderService.create_order(customer_id)
    ↓
1. Valida cliente en CustomerRepository
2. Crea Order en memoria
3. Guarda en OrderRepository
4. Notifica a Observer (OrderSubject)
    ↓
Observadores reciben notificación:
    - EmailNotificationObserver
    - InventoryObserver
    - AnalyticsObserver
```

### Agregar Item al Pedido

```
Usuario (CLI)
    ↓
OrderService.add_item_to_order(order_id, product_id, quantity)
    ↓
1. Valida pedido en OrderRepository
2. Valida producto en ProductRepository
3. Verifica stock disponible (Domain logic)
4. Aplica estrategia de precios (Strategy Pattern)
5. Reduce stock del producto
6. Agrega item al pedido
7. Actualiza OrderRepository
8. Notifica a observadores
```

## Principios SOLID en Práctica

### 1. Single Responsibility Principle (SRP)

**Ejemplo**: Clase Product
```python
class Product:
    # RESPONSABILIDAD ÚNICA: Gestionar datos y reglas de producto
    def is_available(self) -> bool:
        return self.stock > 0
    
    def can_purchase(self, quantity: int) -> bool:
        return self.stock >= quantity
```

❌ **Violación**: Si Product también manejara persistencia o UI
✅ **Correcto**: Repository maneja persistencia, Service maneja lógica

### 2. Open/Closed Principle (OCP)

**Ejemplo**: Estrategias de Precios
```python
# Abierto para extensión
class NewDiscountStrategy(IPricingStrategy):
    def calculate_price(self, product, quantity):
        # Nueva lógica sin modificar código existente
        pass

# Cerrado para modificación
# No necesitamos modificar PricingContext
```

### 3. Liskov Substitution Principle (LSP)

**Ejemplo**: Repositorios
```python
def process_data(repo: IRepository):
    # Funciona con cualquier implementación de IRepository
    entity = repo.get_by_id(1)
    # ProductRepository, CustomerRepository, OrderRepository
```

### 4. Interface Segregation Principle (ISP)

**Ejemplo**: Interfaces específicas
```python
# ❌ No forzamos métodos innecesarios
class IRepository:
    def add(self, entity): pass
    def get_by_id(self, id): pass
    # Métodos básicos que todos necesitan

# Extensiones específicas en subclases
class ProductRepository(IRepository):
    def find_by_category(self, category): pass  # Específico de productos
```

### 5. Dependency Inversion Principle (DIP)

**Ejemplo**: Inyección de Dependencias
```python
class OrderService:
    def __init__(self, order_repo: IRepository, product_repo: IRepository):
        # Depende de abstracciones, no de implementaciones concretas
        self.order_repo = order_repo
        self.product_repo = product_repo
```

## Patrones de Diseño Detallados

### Factory Pattern - Diagrama

```
ProductFactoryRegistry
    │
    ├── register_factory(category, factory)
    │
    └── create_product(category, name, price, stock)
            │
            ├─→ ElectronicsFactory → Product(category="ELECTRONICS")
            ├─→ ClothingFactory → Product(category="CLOTHING")
            └─→ BooksFactory → Product(category="BOOKS")
```

**Ventajas**:
- Centraliza la creación de objetos
- Facilita agregar nuevas categorías
- Desacopla cliente del código de creación

### Strategy Pattern - Diagrama

```
PricingContext
    │
    └── set_strategy(IPricingStrategy)
            │
            ├─→ RegularPricingStrategy
            ├─→ BulkDiscountStrategy
            ├─→ SeasonalDiscountStrategy
            └─→ MembershipPricingStrategy
```

**Ventajas**:
- Algoritmos intercambiables en tiempo de ejecución
- Elimina condicionales complejos
- Facilita testing de cada estrategia

### Observer Pattern - Diagrama

```
OrderSubject
    │
    ├── attach(observer)
    ├── detach(observer)
    └── notify(order)
            │
            ├─→ EmailNotificationObserver
            ├─→ InventoryObserver
            └─→ AnalyticsObserver
```

**Ventajas**:
- Desacoplamiento entre sujeto y observadores
- Fácil agregar/quitar observadores
- Notificaciones automáticas

### Singleton Pattern - Diagrama

```
ConfigurationManager (Singleton)
    │
    ├── __new__() → Retorna instancia única
    └── get(key) → Configuración global

get_config() → Siempre la misma instancia
```

**Ventajas**:
- Control de acceso a recurso único
- Punto de acceso global
- Inicialización lazy

## Métricas de Calidad del Código

### Cohesión Alta
Cada módulo tiene una responsabilidad clara:
- `domain/`: Solo entidades y lógica de negocio
- `repository/`: Solo acceso a datos
- `service/`: Solo orquestación
- `patterns/`: Solo implementaciones de patrones

### Acoplamiento Bajo
- Dependencias solo hacia abstracciones
- Comunicación a través de interfaces
- Inyección de dependencias

### Mantenibilidad
- Código auto-documentado
- Nombres descriptivos
- Funciones pequeñas y enfocadas
- Separación de preocupaciones

## Testing Strategy (Estructura recomendada)

```
tests/
├── unit/
│   ├── test_domain.py         # Pruebas de entidades
│   ├── test_repository.py     # Pruebas de repositorios
│   └── test_patterns.py       # Pruebas de patrones
├── integration/
│   └── test_services.py       # Pruebas de servicios
└── e2e/
    └── test_workflows.py      # Pruebas de flujos completos
```

## Extensibilidad

### Agregar una nueva estrategia de precios

```python
class LoyaltyPointsStrategy(IPricingStrategy):
    def calculate_price(self, product, quantity):
        # Implementar lógica de puntos de lealtad
        pass

# Usar sin modificar código existente
context.set_strategy(LoyaltyPointsStrategy())
```

### Agregar un nuevo observador

```python
class SMSNotificationObserver(IOrderObserver):
    def update(self, order):
        # Enviar SMS
        pass

# Agregar al sistema
order_subject.attach(SMSNotificationObserver())
```

### Agregar una nueva entidad

1. Crear entidad en `domain/`
2. Crear repositorio en `repository/`
3. Crear servicio en `service/`
4. Usar en `presentation/`

## Conclusiones

Este proyecto demuestra:

✅ **Arquitectura Sólida**: Capas bien definidas y separadas
✅ **Principios SOLID**: Aplicados consistentemente
✅ **Patrones de Diseño**: Uso apropiado de patrones comunes
✅ **Código Limpio**: Legible, mantenible y extensible
✅ **Buenas Prácticas**: Siguiendo estándares de la industria

El diseño permite:
- Fácil testing
- Modificación sin romper código existente
- Escalabilidad
- Reusabilidad de componentes

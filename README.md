# Examen Práctico II - Arquitectura de Software

## Descripción del Proyecto

Este proyecto es una implementación práctica de conceptos de arquitectura de software para la Unidad 2. Demuestra la aplicación de:

- **Arquitectura en Capas** (Layered Architecture)
- **Principios SOLID**
- **Patrones de Diseño** (Design Patterns)
- **Separación de Responsabilidades**
- **Inyección de Dependencias**

## Sistema E-Commerce

El proyecto implementa un sistema de comercio electrónico simplificado con las siguientes capas:

### 📋 Estructura del Proyecto

```
src/
├── domain/           # Capa de Dominio - Entidades y lógica de negocio
│   ├── product.py    # Entidad Producto
│   ├── customer.py   # Entidad Cliente
│   └── order.py      # Entidad Pedido
│
├── repository/       # Capa de Repositorio - Acceso a datos
│   ├── base_repository.py      # Interfaz base de repositorio
│   ├── product_repository.py   # Repositorio de productos
│   ├── customer_repository.py  # Repositorio de clientes
│   └── order_repository.py     # Repositorio de pedidos
│
├── service/          # Capa de Servicio - Lógica de aplicación
│   ├── product_service.py      # Servicio de productos
│   ├── customer_service.py     # Servicio de clientes
│   └── order_service.py        # Servicio de pedidos
│
├── patterns/         # Patrones de Diseño
│   ├── factory_pattern.py      # Patrón Factory
│   ├── strategy_pattern.py     # Patrón Strategy
│   ├── observer_pattern.py     # Patrón Observer
│   └── singleton_pattern.py    # Patrón Singleton
│
└── presentation/     # Capa de Presentación - Interfaz de usuario
    └── cli_app.py    # Aplicación CLI
```

## 🏗️ Arquitectura en Capas

### 1. Capa de Dominio (Domain Layer)
Contiene las entidades principales y la lógica de negocio:
- **Product**: Representa productos con reglas de inventario
- **Customer**: Gestiona clientes y niveles de membresía
- **Order**: Maneja pedidos y estados

### 2. Capa de Repositorio (Repository Layer)
Abstrae el acceso a datos:
- Implementa el patrón Repository
- Sigue el principio de Inversión de Dependencias (DIP)
- Proporciona operaciones CRUD

### 3. Capa de Servicio (Service Layer)
Orquesta la lógica de negocio:
- Coordina entre repositorios
- Aplica reglas de negocio complejas
- Gestiona transacciones

### 4. Capa de Presentación (Presentation Layer)
Interfaz con el usuario:
- CLI para demostración
- Separación de UI y lógica de negocio

## 🎯 Principios SOLID

### 1. Single Responsibility Principle (SRP)
Cada clase tiene una única responsabilidad:
- `Product`: Gestiona datos y reglas de productos
- `ProductRepository`: Solo acceso a datos de productos
- `ProductService`: Solo lógica de aplicación de productos

### 2. Open/Closed Principle (OCP)
Abierto para extensión, cerrado para modificación:
- Interfaces de repositorio permiten diferentes implementaciones
- Estrategias de precios son extensibles

### 3. Liskov Substitution Principle (LSP)
Las clases derivadas pueden sustituir a sus clases base:
- Todas las estrategias de precios implementan `IPricingStrategy`
- Todos los repositorios implementan `IRepository`

### 4. Interface Segregation Principle (ISP)
Interfaces específicas en lugar de generales:
- `IRepository` proporciona operaciones básicas
- Métodos específicos en implementaciones concretas

### 5. Dependency Inversion Principle (DIP)
Depender de abstracciones, no de implementaciones:
- Servicios dependen de interfaces de repositorio
- Inyección de dependencias en constructores

## 🎨 Patrones de Diseño Implementados

### 1. Factory Pattern (Patrón Fábrica)
**Archivo**: `src/patterns/factory_pattern.py`

Crea objetos sin especificar la clase exacta:
```python
factory = get_product_factory_registry()
product = factory.create_product("ELECTRONICS", "Laptop", 999.99, 10)
```

### 2. Strategy Pattern (Patrón Estrategia)
**Archivo**: `src/patterns/strategy_pattern.py`

Define familia de algoritmos intercambiables:
```python
context = PricingContext()
context.set_strategy(BulkDiscountStrategy())
price = context.calculate_price(product, quantity)
```

Estrategias disponibles:
- `RegularPricingStrategy`: Precio regular
- `BulkDiscountStrategy`: Descuento por volumen
- `SeasonalDiscountStrategy`: Descuento de temporada
- `MembershipPricingStrategy`: Descuento por membresía

### 3. Observer Pattern (Patrón Observador)
**Archivo**: `src/patterns/observer_pattern.py`

Notifica cambios a múltiples observadores:
```python
order_subject = OrderSubject()
order_subject.attach(EmailNotificationObserver())
order_subject.attach(InventoryObserver())
order_subject.notify(order)
```

Observadores implementados:
- `EmailNotificationObserver`: Notificaciones por email
- `InventoryObserver`: Actualización de inventario
- `AnalyticsObserver`: Seguimiento de métricas

### 4. Singleton Pattern (Patrón Singleton)
**Archivo**: `src/patterns/singleton_pattern.py`

Garantiza una única instancia:
```python
config = get_config()  # Siempre devuelve la misma instancia
```

## 🚀 Cómo Ejecutar

### Requisitos
- Python 3.8 o superior

### Instalación y Ejecución
```bash
# Navegar al directorio del proyecto
cd Examen_PracticoII_Arquitectura

# Ejecutar la aplicación de demostración
python -m src.presentation.cli_app
```

### Salida Esperada
La aplicación demostrará:
1. Creación de datos de ejemplo
2. Visualización de productos y clientes
3. Uso de patrones de diseño
4. Procesamiento de pedidos con observadores

## 📚 Conceptos Demostrados

### Arquitectura Limpia (Clean Architecture)
- Separación clara de responsabilidades
- Independencia de frameworks
- Testabilidad
- Reglas de negocio protegidas

### Inyección de Dependencias
```python
order_service = OrderService(
    order_repo=OrderRepository(),
    product_repo=ProductRepository(),
    customer_repo=CustomerRepository()
)
```

### Inversión de Control (IoC)
Los servicios reciben dependencias en lugar de crearlas.

## 🎓 Objetivos de Aprendizaje

Este proyecto demuestra:

1. ✅ **Diseño Modular**: Código organizado en capas independientes
2. ✅ **Mantenibilidad**: Código fácil de modificar y extender
3. ✅ **Escalabilidad**: Arquitectura que soporta crecimiento
4. ✅ **Testabilidad**: Componentes aislados y testeables
5. ✅ **Reutilización**: Componentes reutilizables
6. ✅ **Buenas Prácticas**: Siguiendo estándares de la industria

## 📖 Documentación Adicional

### Reglas de Negocio Implementadas

#### Productos
- Un producto está disponible si tiene stock > 0
- No se puede comprar más de lo disponible en stock
- Los descuentos deben estar entre 0% y 100%

#### Clientes
- Niveles de membresía: BRONZE, SILVER, GOLD
- Actualización automática basada en compras totales:
  - BRONZE: < $500
  - SILVER: $500 - $999
  - GOLD: >= $1000

#### Pedidos
- Estados: PENDING, PROCESSING, SHIPPED, DELIVERED, CANCELLED
- Solo pedidos pendientes pueden recibir nuevos items
- Solo pedidos pendientes/en proceso pueden cancelarse
- Descuentos aplicados según membresía del cliente

## 👨‍💻 Autor

Proyecto desarrollado como parte del Examen Práctico de la Unidad 2 de Arquitectura de Software.

## 📝 Licencia

Este proyecto es con fines educativos.
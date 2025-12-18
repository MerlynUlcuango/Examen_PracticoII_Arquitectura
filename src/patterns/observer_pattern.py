"""
Observer Pattern - Behavioral Design Pattern
Defines a subscription mechanism to notify multiple objects about events
"""
from abc import ABC, abstractmethod
from typing import List
from src.domain.order import Order


class IOrderObserver(ABC):
    """Observer interface for order events"""
    
    @abstractmethod
    def update(self, order: Order) -> None:
        """Called when order state changes"""
        pass


class EmailNotificationObserver(IOrderObserver):
    """Observer that sends email notifications"""
    
    def update(self, order: Order) -> None:
        """Send email notification"""
        print(f"[EMAIL] Order #{order.id} status changed to {order.status.value}")
        print(f"[EMAIL] Sending notification to customer #{order.customer_id}")


class InventoryObserver(IOrderObserver):
    """Observer that updates inventory"""
    
    def update(self, order: Order) -> None:
        """Update inventory based on order"""
        print(f"[INVENTORY] Processing order #{order.id}")
        print(f"[INVENTORY] Updating stock for {len(order.items)} items")


class AnalyticsObserver(IOrderObserver):
    """Observer that tracks analytics"""
    
    def update(self, order: Order) -> None:
        """Track order analytics"""
        total = order.calculate_total()
        print(f"[ANALYTICS] Order #{order.id} - Total: ${total:.2f}")
        print(f"[ANALYTICS] Status: {order.status.value}")


class OrderSubject:
    """
    Subject that notifies observers about order changes
    Demonstrates Observer Pattern
    """
    
    def __init__(self):
        self._observers: List[IOrderObserver] = []
    
    def attach(self, observer: IOrderObserver) -> None:
        """Attach an observer"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: IOrderObserver) -> None:
        """Detach an observer"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, order: Order) -> None:
        """Notify all observers about order changes"""
        for observer in self._observers:
            observer.update(order)

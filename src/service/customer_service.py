"""
Customer Service - Application Layer
Manages customer-related operations
"""
from typing import List, Optional
from src.domain.customer import Customer
from src.repository.customer_repository import CustomerRepository


class CustomerService:
    """Service for managing customers"""
    
    def __init__(self, customer_repo: CustomerRepository):
        self.customer_repo = customer_repo
    
    def create_customer(self, name: str, email: str) -> Customer:
        """Create a new customer"""
        # Check if email already exists
        existing = self.customer_repo.find_by_email(email)
        if existing:
            raise ValueError(f"Customer with email {email} already exists")
        
        customer = Customer(id=0, name=name, email=email)
        return self.customer_repo.add(customer)
    
    def get_customer(self, customer_id: int) -> Optional[Customer]:
        """Get a customer by ID"""
        return self.customer_repo.get_by_id(customer_id)
    
    def get_customer_by_email(self, email: str) -> Optional[Customer]:
        """Get a customer by email"""
        return self.customer_repo.find_by_email(email)
    
    def get_all_customers(self) -> List[Customer]:
        """Get all customers"""
        return self.customer_repo.get_all()
    
    def update_customer(self, customer: Customer) -> Customer:
        """Update a customer"""
        return self.customer_repo.update(customer)
    
    def delete_customer(self, customer_id: int) -> bool:
        """Delete a customer"""
        return self.customer_repo.delete(customer_id)

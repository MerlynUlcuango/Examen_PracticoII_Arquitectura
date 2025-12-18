# Tests Directory

This directory contains unit tests for the e-commerce system architecture.

## Test Structure

- `test_domain.py` - Tests for domain entities (Product, Customer, Order)
- `test_patterns.py` - Tests for design pattern implementations

## Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_domain

# Run specific test class
python -m unittest tests.test_domain.TestProduct

# Run specific test method
python -m unittest tests.test_domain.TestProduct.test_is_available_with_stock
```

## Test Coverage

The tests cover:
- Business logic in domain entities
- Design pattern implementations
- Edge cases and error handling
- State transitions

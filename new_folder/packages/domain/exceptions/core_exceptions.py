class DomainException(Exception):
    """Base exception for domain logic errors."""
    pass

class NotFoundError(DomainException):
    def __init__(self, entity_name: str, identifier: str):
        super().__init__(f"{entity_name} '{identifier}' not found.")

class InsufficientStockError(DomainException):
    def __init__(self, part_id: str, required: int, available: int):
        super().__init__(f"Cannot reserve {required} units for part {part_id}. Only {available} available.")

class InvalidOperationError(DomainException):
    def __init__(self, reason: str):
        super().__init__(f"Invalid Operation: {reason}")
        
class DatabaseError(DomainException):
    pass

class ValidationError(DomainException):
    pass
    
class BusinessRuleViolationError(DomainException):
    pass

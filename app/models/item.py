from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class ItemCategory(str, Enum):
    """Valid item categories."""
    ELECTRONICS = "electronics"
    CLOTHING = "clothing"
    FOOD = "food"
    BOOKS = "books"
    OTHER = "other"


class Item(BaseModel):
    """Item model with validation rules."""
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price must be positive")
    tax: Optional[float] = Field(default=None, ge=0, description="Tax must be non-negative")
    category: ItemCategory  # Required field - will break existing tests

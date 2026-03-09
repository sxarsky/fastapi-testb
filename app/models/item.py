from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    """Item model with validation rules."""
    name: str
    description: Optional[str] = None
    price: float = Field(gt=0, description="Price must be positive")
    tax: Optional[float] = Field(default=None, ge=0, description="Tax must be non-negative")

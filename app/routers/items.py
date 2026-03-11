from fastapi import APIRouter, HTTPException, status
from typing import Dict
from app.models.item import Item

router = APIRouter(prefix="/items", tags=["items"])

# In-memory storage
items_db: Dict[int, Item] = {}
next_id = 1


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item):
    """Create a new item."""
    global next_id
    item_id = next_id
    items_db[item_id] = item
    next_id += 1
    return {"id": item_id, **item.model_dump()}


@router.get("/{item_id}")
def get_item(item_id: int):
    """Get item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **items_db[item_id].model_dump()}


@router.get("/")
def list_items():
    """List all items."""
    return [{"id": item_id, **item.model_dump()} for item_id, item in items_db.items()]


@router.put("/{item_id}")
def update_item(item_id: int, item: Item):
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    items_db[item_id] = item
    return {"id": item_id, **item.model_dump()}


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None

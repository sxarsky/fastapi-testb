from fastapi import APIRouter, HTTPException, status
from typing import List, Dict
from models.item import Item

router = APIRouter(prefix="/items", tags=["items"])

# In-memory storage for items
items_db: Dict[int, dict] = {}
next_id = 1


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_item(item: Item) -> dict:
    """Create a new item."""
    global next_id
    item_dict = item.model_dump()
    item_dict["id"] = next_id
    items_db[next_id] = item_dict
    next_id += 1
    return item_dict


@router.get("/{item_id}")
def get_item(item_id: int) -> dict:
    """Get item by ID."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    return items_db[item_id]


@router.get("/")
def list_items() -> List[dict]:
    """List all items."""
    return list(items_db.values())


@router.put("/{item_id}")
def update_item(item_id: int, item: Item) -> dict:
    """Update an existing item."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    item_dict = item.model_dump()
    item_dict["id"] = item_id
    items_db[item_id] = item_dict
    return item_dict


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int):
    """Delete an item."""
    if item_id not in items_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )
    del items_db[item_id]
    return None

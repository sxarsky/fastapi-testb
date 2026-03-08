from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

app = FastAPI(
    title="TestBot FastAPI Demo",
    description="Demo API for TestBot validation",
    version="1.0.0"
)

# Security
security = HTTPBearer()

# Simple in-memory storage
items_db = {}
users_db = {
    "test@test.com": {
        "id": "user-1",
        "email": "test@test.com",
        "name": "Test User",
        "api_key": "test-api-key-12345"
    }
}

# Models
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

class ItemResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    price: float
    tax: Optional[float]
    created_at: str

class User(BaseModel):
    email: str
    name: str

class UserResponse(BaseModel):
    id: str
    email: str
    name: str

# Auth dependency
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    # Simple token validation
    if token not in ["test-api-key-12345", "admin-key"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return token

# Routes
@app.get("/")
def read_root():
    return {
        "message": "Welcome to TestBot FastAPI Demo",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Items endpoints
@app.get("/items", response_model=List[ItemResponse])
def list_items(token: str = Depends(verify_token)):
    """List all items"""
    return list(items_db.values())

@app.post("/items", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(item: Item, token: str = Depends(verify_token)):
    """Create a new item"""
    item_id = str(uuid.uuid4())
    item_data = {
        "id": item_id,
        **item.dict(),
        "created_at": datetime.utcnow().isoformat()
    }
    items_db[item_id] = item_data
    return item_data

@app.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: str, token: str = Depends(verify_token)):
    """Get a specific item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    return items_db[item_id]

@app.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: str, item: Item, token: str = Depends(verify_token)):
    """Update an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item_data = {
        "id": item_id,
        **item.dict(),
        "created_at": items_db[item_id]["created_at"]
    }
    items_db[item_id] = item_data
    return item_data

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: str, token: str = Depends(verify_token)):
    """Delete an item"""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")
    del items_db[item_id]
    return None

# Users endpoints (public - no auth)
@app.get("/users", response_model=List[UserResponse])
def list_users():
    """List all users"""
    return [
        {"id": user["id"], "email": user["email"], "name": user["name"]}
        for user in users_db.values()
    ]

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str):
    """Get a specific user"""
    user = next((u for u in users_db.values() if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user["id"], "email": user["email"], "name": user["name"]}

# Public endpoint for testing
@app.get("/public/stats")
def get_stats():
    """Get public statistics"""
    return {
        "total_items": len(items_db),
        "total_users": len(users_db),
        "timestamp": datetime.utcnow().isoformat()
    }

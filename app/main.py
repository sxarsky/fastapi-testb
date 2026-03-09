from fastapi import FastAPI
from datetime import datetime
from app.routers import items

app = FastAPI(
    title="TestBot FastAPI Demo",
    description="Demo API for TestBot validation",
    version="1.0.0"
)

app.include_router(items.router)


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

#!/bin/bash
set -e

# TestBot Setup Script for FastAPI
# This script starts the FastAPI service and seeds test data

cd "$(dirname "$0")"

echo "Starting FastAPI service..."
docker-compose up -d

echo "Waiting for service to be ready..."
# Brief wait for container to initialize
sleep 3

echo "Seeding test data..."
API_BASE="http://localhost:8000"
API_KEY="test-api-key-12345"

# Create sample items
curl -s -X POST "$API_BASE/items" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Laptop","description":"High-performance laptop","price":1299.99,"tax":129.99}' > /dev/null

curl -s -X POST "$API_BASE/items" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Mouse","description":"Wireless mouse","price":29.99,"tax":3.00}' > /dev/null

curl -s -X POST "$API_BASE/items" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Keyboard","description":"Mechanical keyboard","price":89.99,"tax":9.00}' > /dev/null

echo "✓ FastAPI setup complete"

# Optional: Output JSON for TestBot to override baseUrl
# echo '{"baseUrl":"http://localhost:8000"}'

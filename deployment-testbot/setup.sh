#!/bin/bash
set -e

# TestBot Setup Script for FastAPI
# This script starts the FastAPI service

cd "$(dirname "$0")"

echo "Starting FastAPI service..."
docker compose up -d

echo "Waiting for service to be ready..."
# Brief wait for container to initialize
sleep 5

echo "✓ FastAPI setup complete"

# Optional: Output JSON for TestBot to override baseUrl
# echo '{"baseUrl":"http://localhost:8000"}'

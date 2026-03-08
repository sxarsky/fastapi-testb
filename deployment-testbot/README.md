# FastAPI - TestBot Deployment

TestBot-compatible deployment scripts for FastAPI demo application.

## Files

- **setup.sh** - Starts FastAPI service and seeds test data
- **get-token.sh** - Outputs API token for authentication
- **docker-compose.yml** - Service configuration
- **app/** - FastAPI application code

## TestBot Configuration

```yaml
- uses: skyramp/testbot@v1
  with:
    skyramp_license_file: ${{ secrets.SKYRAMP_LICENSE }}
    cursor_api_key: ${{ secrets.CURSOR_API_KEY }}
    target_setup_command: './deployment-testbot/fastapi/setup.sh'
    target_ready_check_command: 'curl -f http://localhost:8000/health'
    auth_token_command: './deployment-testbot/fastapi/get-token.sh'
    target_teardown_command: 'docker-compose -f deployment-testbot/fastapi/docker-compose.yml down'
```

## Application Details

- **Port:** 8000
- **API Base:** http://localhost:8000
- **Health Endpoint:** /health
- **API Docs:** http://localhost:8000/docs
- **Auth Type:** Bearer Token
- **Token:** test-api-key-12345

## API Endpoints

### Authenticated Endpoints
- `GET /items` - List all items
- `POST /items` - Create new item
- `GET /items/{item_id}` - Get specific item
- `PUT /items/{item_id}` - Update item
- `DELETE /items/{item_id}` - Delete item

### Public Endpoints
- `GET /` - Welcome message
- `GET /health` - Health check
- `GET /users` - List users
- `GET /public/stats` - Public statistics

## Manual Testing

```bash
# Start services
./setup.sh

# Get token
TOKEN=$(./get-token.sh)

# Test API
curl http://localhost:8000/items \
  -H "Authorization: Bearer $TOKEN"

# Stop services
docker-compose down
```

## Test Data

Setup script creates 3 sample items:
- Laptop ($1299.99)
- Mouse ($29.99)
- Keyboard ($89.99)

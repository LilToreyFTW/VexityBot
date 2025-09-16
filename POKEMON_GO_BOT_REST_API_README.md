# Pokemon Go Bot REST API Integration

## 🚀 Overview

This integration provides complete REST API control for Pokemon Go Bots, matching the exact API specification you provided. It includes secure authentication, comprehensive bot management, Pokemon operations, item management, and location control.

## 🔐 Authentication System

### Bot Configuration
Each bot requires a secure password set in the `rest_api_password` setting in your `config.properties` file or `restApiPassword` in JSON config files.

```properties
# config.properties
rest_api_password=your_secure_random_password_here
```

```json
{
  "restApiPassword": "your_secure_random_password_here"
}
```

### Authentication Process
1. **Request Token**: POST to `http://localhost:8080/api/bot/{name}/auth`
2. **Send Raw Password**: The request body must contain the raw password (not JSON)
3. **Receive Token**: Server responds with a session token
4. **Use Token**: Include token in `X-PGB-ACCESS-TOKEN` header for all subsequent requests

### Example Authentication
```bash
# Get token
curl -X POST http://localhost:8080/api/bot/default/auth \
  -H "Content-Type: text/plain" \
  -d "your_secure_password"

# Response:
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

# Use token for authenticated requests
curl -X GET http://localhost:8080/api/bot/default/pokemons \
  -H "X-PGB-ACCESS-TOKEN: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

## 📡 REST API Endpoints

### General Endpoints

#### `GET /api/bots`
List all bots (no authentication required)
```bash
curl http://localhost:8080/api/bots
```

### Bot Control Endpoints

#### `POST /api/bot/{name}/load`
Load a bot
```bash
curl -X POST http://localhost:8080/api/bot/default/load \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/unload`
Unload a bot
```bash
curl -X POST http://localhost:8080/api/bot/default/unload \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/reload`
Reload a bot
```bash
curl -X POST http://localhost:8080/api/bot/default/reload \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/start`
Start a bot
```bash
curl -X POST http://localhost:8080/api/bot/default/start \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/stop`
Stop a bot
```bash
curl -X POST http://localhost:8080/api/bot/default/stop \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

### Pokemon Management Endpoints

#### `GET /api/bot/{name}/pokemons`
List all Pokemon
```bash
curl http://localhost:8080/api/bot/default/pokemons \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/pokemon/{id}/transfer`
Transfer a Pokemon
```bash
curl -X POST http://localhost:8080/api/bot/default/pokemon/12345/transfer \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/pokemon/{id}/evolve`
Evolve a Pokemon
```bash
curl -X POST http://localhost:8080/api/bot/default/pokemon/12345/evolve \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/pokemon/{id}/powerup`
Power up a Pokemon
```bash
curl -X POST http://localhost:8080/api/bot/default/pokemon/12345/powerup \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/pokemon/{id}/favorite`
Toggle favorite for a Pokemon
```bash
curl -X POST http://localhost:8080/api/bot/default/pokemon/12345/favorite \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/pokemon/{id}/rename`
Rename a Pokemon
```bash
curl -X POST http://localhost:8080/api/bot/default/pokemon/12345/rename \
  -H "Content-Type: text/plain" \
  -H "X-PGB-ACCESS-TOKEN: your_token" \
  -d "New Pokemon Name"
```

### Item Management Endpoints

#### `GET /api/bot/{name}/items`
List all items
```bash
curl http://localhost:8080/api/bot/default/items \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `DELETE /api/bot/{name}/item/{id}/drop/{quantity}`
Drop quantity of an item
```bash
curl -X DELETE http://localhost:8080/api/bot/default/item/12345/drop/5 \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/useIncense`
Use an incense
```bash
curl -X POST http://localhost:8080/api/bot/default/useIncense \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/useLuckyEgg`
Use a lucky egg
```bash
curl -X POST http://localhost:8080/api/bot/default/useLuckyEgg \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

### Location and Profile Endpoints

#### `GET /api/bot/{name}/location`
Get bot current location
```bash
curl http://localhost:8080/api/bot/default/location \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `POST /api/bot/{name}/location/{latitude}/{longitude}`
Change bot location
```bash
curl -X POST http://localhost:8080/api/bot/default/location/40.7589/-73.9851 \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `GET /api/bot/{name}/profile`
Get account profile
```bash
curl http://localhost:8080/api/bot/default/profile \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `GET /api/bot/{name}/pokedex`
Get account pokedex
```bash
curl http://localhost:8080/api/bot/default/pokedex \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

#### `GET /api/bot/{name}/eggs`
Get eggs
```bash
curl http://localhost:8080/api/bot/default/eggs \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

## 🐍 Python Integration

### Basic Usage

```python
from PokemonGoBot_SpringBoot_Integration import PokemonGoBotSpringBootIntegration

# Create integration instance
integration = PokemonGoBotSpringBootIntegration()

# Register a bot
config = {
    'credentials': {
        'username': 'your_username',
        'password': 'your_password',
        'auth_type': 'PTC'
    },
    'location': {
        'lat': 40.7589,
        'lng': -73.9851,
        'alt': 10
    }
}
integration.register_bot('my_bot', config)

# Set password for authentication
integration.set_bot_password('my_bot', 'secure_password_123')

# Authenticate
integration.authenticate_bot('my_bot', 'secure_password_123')

# Control bot
integration.load_bot('my_bot')
integration.start_bot('my_bot')

# Manage Pokemon
pokemon_data = integration.get_pokemons('my_bot')
integration.transfer_pokemon('my_bot', 'pokemon_id')
integration.evolve_pokemon('my_bot', 'pokemon_id')

# Manage items
item_data = integration.get_items('my_bot')
integration.drop_item('my_bot', 'item_id', 5)
integration.use_incense('my_bot')

# Location control
integration.set_location('my_bot', 40.7128, -74.0060)
location = integration.get_location('my_bot')

# Stop bot
integration.stop_bot('my_bot')
integration.unload_bot('my_bot')
```

### GUI Integration

```python
from PokemonGoBot_GUI_Integration import PokemonGoBotGUITab
import tkinter as tk

# Create GUI
root = tk.Tk()
notebook = ttk.Notebook(root)

# Add Pokemon Go Bot tab
pokemon_tab = PokemonGoBotGUITab(notebook)
notebook.add(pokemon_tab.parent, text="Pokemon Go Bot")

# The GUI includes:
# - Bot Management (Load/Unload/Start/Stop/Reload)
# - Pokemon Management (Transfer/Evolve/Power Up/Favorite/Rename)
# - Item Management (Drop/Use Incense/Use Lucky Egg)
# - Statistics and Monitoring
# - Configuration Management
# - Real-time Logs
```

## 🔧 Configuration

### Spring Boot Backend Configuration

```json
{
    "enabled": true,
    "base_url": "http://localhost:8080",
    "server_port": 8080,
    "jar_file": "PokemonGoBot.jar",
    "config_file": "config.properties",
    "java_executable": "java",
    "spring_profile": "dev",
    "auto_start": true,
    "auto_restart": true,
    "restart_delay": 5
}
```

### Bot Configuration

```json
{
    "bot_name": "my_bot",
    "enabled": true,
    "location": {
        "lat": 40.7589,
        "lng": -73.9851,
        "alt": 10
    },
    "credentials": {
        "username": "your_username",
        "password": "your_password",
        "auth_type": "PTC"
    },
    "settings": {
        "walk_speed": 4.16,
        "catch_pokemon": true,
        "spin_pokestops": true,
        "battle_gyms": false,
        "catch_legendary": true,
        "catch_shiny": true,
        "transfer_duplicates": true,
        "min_cp_threshold": 100,
        "max_pokemon_storage": 1000
    },
    "advanced": {
        "human_like_delays": true,
        "random_movements": true,
        "smart_timing": true,
        "ban_bypass": true,
        "ai_automation": true
    },
    "restApiPassword": "your_secure_random_password"
}
```

## 🚀 Quick Start

### 1. Start Spring Boot Backend
```bash
# Using the Python wrapper
python pokemon-go-bot.py

# Or using Java directly
java -jar PokemonGoBot.jar --server-port=8080
```

### 2. Test API Connection
```bash
# Check if backend is running
curl http://localhost:8080/actuator/health

# List all bots
curl http://localhost:8080/api/bots
```

### 3. Authenticate and Control Bot
```bash
# Authenticate
TOKEN=$(curl -X POST http://localhost:8080/api/bot/default/auth \
  -H "Content-Type: text/plain" \
  -d "your_password" | jq -r '.token')

# Start bot
curl -X POST http://localhost:8080/api/bot/default/start \
  -H "X-PGB-ACCESS-TOKEN: $TOKEN"

# Get Pokemon
curl http://localhost:8080/api/bot/default/pokemons \
  -H "X-PGB-ACCESS-TOKEN: $TOKEN"
```

### 4. Use Python Integration
```python
# Run the test script
python test_pokemon_go_bot_rest_api.py

# Or use in your code
from PokemonGoBot_SpringBoot_Integration import PokemonGoBotSpringBootIntegration
integration = PokemonGoBotSpringBootIntegration()
# ... use integration methods
```

## 📊 Error Handling

### HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters, not enough resources)
- **401**: Unauthorized (invalid password or token)
- **404**: Not Found (bot not found)
- **500**: Internal Server Error

### Common Error Scenarios
- **Authentication Failed**: Check password and token
- **Bot Not Found**: Ensure bot is registered and loaded
- **Insufficient Resources**: Not enough candy, stardust, or items
- **Invalid Parameters**: Check latitude/longitude, quantities, etc.

## 🔒 Security Features

- **Secure Authentication**: Random session tokens
- **Password Protection**: Each bot has its own password
- **Token Expiration**: Tokens expire after 1 hour
- **Input Validation**: All parameters are validated
- **Error Handling**: Comprehensive error responses

## 📈 Performance Tips

1. **Reuse Tokens**: Don't authenticate for every request
2. **Batch Operations**: Group related operations together
3. **Monitor Status**: Check bot status before operations
4. **Handle Errors**: Implement proper error handling
5. **Rate Limiting**: Don't overwhelm the API with requests

## 🧪 Testing

### Run Test Suite
```bash
python test_pokemon_go_bot_rest_api.py
```

### Test Individual Endpoints
```bash
# Test authentication
curl -X POST http://localhost:8080/api/bot/default/auth \
  -H "Content-Type: text/plain" \
  -d "test_password"

# Test bot control
curl -X POST http://localhost:8080/api/bot/default/start \
  -H "X-PGB-ACCESS-TOKEN: your_token"

# Test Pokemon operations
curl http://localhost:8080/api/bot/default/pokemons \
  -H "X-PGB-ACCESS-TOKEN: your_token"
```

## 🎯 Use Cases

### 1. Bot Management
- Load/unload bots dynamically
- Start/stop bots remotely
- Monitor bot status and performance
- Reload bots with new configurations

### 2. Pokemon Operations
- Transfer duplicate Pokemon automatically
- Evolve Pokemon when enough candy
- Power up high IV Pokemon
- Manage favorites and nicknames

### 3. Item Management
- Drop excess items to free space
- Use incense and lucky eggs strategically
- Monitor item inventory
- Optimize item usage

### 4. Location Control
- Change bot location remotely
- Set specific coordinates
- Monitor current location
- Plan optimal routes

### 5. Account Management
- View account profile and stats
- Check Pokedex progress
- Monitor egg inventory
- Track achievements

## 🔧 Troubleshooting

### Common Issues

1. **"Authentication failed"**
   - Check password is correct
   - Ensure token is valid and not expired
   - Verify bot is registered

2. **"Bot not found"**
   - Register bot first
   - Check bot name spelling
   - Ensure bot is loaded

3. **"Not enough resources"**
   - Check candy/stardust/item counts
   - Verify Pokemon/item exists
   - Check quantity parameters

4. **"Invalid parameters"**
   - Validate latitude/longitude ranges
   - Check quantity limits
   - Verify data types

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable debug logging for detailed information
```

## 📚 API Reference

### Request Headers
- `Content-Type: application/json` (for JSON requests)
- `Content-Type: text/plain` (for raw data requests)
- `X-PGB-ACCESS-TOKEN: your_token` (for authenticated requests)

### Response Format
```json
{
  "success": true,
  "data": {...},
  "message": "Operation completed successfully"
}
```

### Error Response Format
```json
{
  "error": "Error description",
  "code": 400,
  "message": "Bad Request"
}
```

---

**Pokemon Go Bot REST API Integration v1.0**
*Complete external control system for Pokemon Go Bots*

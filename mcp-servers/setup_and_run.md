# MCP Servers Setup and Run Guide

This guide will help you set up and run the Travvy MCP (Model Context Protocol) servers locally.

## Prerequisites

- Python 3.11 or higher
- UV package manager (modern Python package installer)
- Git (for cloning repositories)

## Setup Instructions

### 1. Install UV Package Manager

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify installation
uv --version
```

### 2. Navigate to the MCP Servers Directory

```bash
cd /Users/saikumar/travvy/mcp-servers
```

### 3. Create a Virtual Environment with UV

```bash
# Create virtual environment with Python 3.11
uv venv --python 3.11

# Activate virtual environment
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
# Install all dependencies using UV
uv pip install -r requirements.txt

# Alternative: Use UV sync if pyproject.toml is available
# uv sync
```

### 5. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your API keys
nano .env  # or use your preferred editor
```

Required API keys:
- **GOOGLE_MAPS_API_KEY**: Get from [Google Cloud Console](https://console.cloud.google.com/)
- **RAPIDAPI_KEY**: Get from [RapidAPI](https://rapidapi.com/)
- **GROQ_API_KEY**: Get from [Groq](https://groq.com/)

### 6. Test Individual Servers

You can test each server individually:

#### Weather Server
```bash
python weather_server.py
```

#### Maps Server  
```bash
python maps_server.py
```

#### Flights Server
```bash
python flights.py
```

#### Hotels/Accommodation Server
```bash
python accomadation.py
```

#### Trains Server
```bash
python train_server.py
```

### 7. Run with MCP Client

To use the servers with an MCP client:

```bash
python client.py
```

## Available MCP Servers

### 1. **Weather Server** (`weather_server.py`)
- **Tools**: `get_alerts`, `get_forecast`
- **Description**: Provides weather alerts and forecasts using US National Weather Service API
- **Dependencies**: No API key required

### 2. **Maps Server** (`maps_server.py`) 
- **Tools**: `geocode_address`, `reverse_geocode`, `search_places`, `get_directions`, `get_distance_matrix`
- **Description**: Geographic information and mapping services using Google Maps API
- **Required**: `GOOGLE_MAPS_API_KEY`

### 3. **Flights Server** (`flights.py`)
- **Tools**: `search_airport`, `search_flights`, `get_flight_details`
- **Description**: Flight search and booking capabilities
- **Dependencies**: Uses fast-flights library

### 4. **Hotels Server** (`accomadation.py`)
- **Tools**: `search_hotels`, `get_hotel_details`, `get_hotel_amenities`
- **Description**: Hotel search and accommodation services
- **Required**: `RAPIDAPI_KEY`, `RAPIDAPI_HOST`

### 5. **Trains Server** (`train_server.py`)
- **Tools**: `get_station_status`, `get_train_info`, `search_trains`, `get_route`, `search_stations`
- **Description**: Indian Railways train information and booking
- **Dependencies**: Uses custom trains.py module

## Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   # Make sure all dependencies are installed
   uv pip install -r requirements.txt
   ```

1. **UV Not Found**
   ```bash
   # Install UV package manager
   curl -LsSf https://astral.sh/uv/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"
   ```

2. **API Key Errors**
   ```bash
   # Check your .env file has the correct API keys
   cat .env
   ```

3. **Permission Errors**
   ```bash
   # Make sure scripts are executable
   chmod +x *.py
   ```

4. **Virtual Environment Issues**
   ```bash
   # Remove and recreate virtual environment
   rm -rf .venv
   uv venv --python 3.11
   source .venv/bin/activate
   uv pip install -r requirements.txt
   ```

5. **Port Already in Use**
   - Each server runs on stdio transport, so no port conflicts should occur

### Testing Individual Tools

You can test individual tools by importing them:

```python
# Test weather server
from weather_server import get_forecast
import asyncio

async def test():
    result = await get_forecast(37.7749, -122.4194)  # San Francisco
    print(result)

asyncio.run(test())
```

## MCP Configuration

The `mcp_config.json` file contains the configuration for all servers. Each server is configured with:

- **command**: Python interpreter
- **args**: Script filename
- **transport**: stdio (standard input/output)
- **env**: Required environment variables
- **description**: Server description

## Development

### Adding New Tools

To add new tools to any server:

1. Define your async function
2. Use the `@mcp.tool()` decorator
3. Add proper docstring with Args description
4. Handle errors appropriately

Example:
```python
@mcp.tool()
async def my_new_tool(param: str) -> str:
    """Description of what this tool does.
    
    Args:
        param: Description of the parameter
    """
    # Your implementation here
    return "result"
```

### Logging

All servers use Python's logging module. Logs are sent to stderr to avoid interfering with MCP communication on stdout.

## Production Deployment

For production deployment:

1. Use proper environment variable management
2. Implement rate limiting
3. Add monitoring and health checks
4. Use production-grade error handling
5. Consider using Docker containers

## Support

If you encounter issues:

1. Check the logs in stderr
2. Verify API keys are correct
3. Ensure all dependencies are installed
4. Test individual servers before using with MCP client

For more information about MCP, visit: https://modelcontextprotocol.io/

# Travvy MCP Server

A modular MCP (Model Context Protocol) server for travel-related tools and services.

## Overview

This server provides travel assistant capabilities including flight search and weather information through a clean, modular architecture following MCP best practices.

## Features

### Flight Tools
- **search_flights**: General flight search between airports
- **get_best_flights**: Best flights as determined by Google Flights
- **get_cheapest_flights**: Flights sorted by price

### Weather Tools  
- **get_weather_forecast**: Weather forecast for any location
- **get_weather_alerts**: Active weather alerts for US states

## Architecture

```
src/
├── travvy_mcp/
│   ├── __init__.py
│   ├── server.py          # Main MCP server implementation
│   ├── tools/             # Tool implementations
│   │   ├── __init__.py
│   │   ├── base.py        # Base tool classes
│   │   ├── flights.py     # Flight search tools
│   │   └── weather.py     # Weather tools
│   └── utils/
│       ├── __init__.py
│       └── formatters.py  # Response formatters
```

## Local Development

1. **Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run Server**
   ```bash
   python main.py
   ```

3. **Test MCP Protocol**
   ```bash
   curl -X POST http://localhost:8080/ \
     -H "Content-Type: application/json" \
     -d '{"jsonrpc": "2.0", "id": 1, "method": "tools/list"}'
   ```

## Cloud Deployment

### Google Cloud Run

```bash
gcloud run deploy travvy-mcp-server \
  --source . \
  --region europe-west1 \
  --allow-unauthenticated
```

### Docker

```bash
docker build -t travvy-mcp-server .
docker run -p 8080:8080 travvy-mcp-server
```

## MCP Client Configuration

For HTTP transport:

```json
{
  "mcpServers": {
    "travvy": {
      "httpUrl": "https://your-deployment-url.run.app/"
    }
  }
}
```

## API Reference

### Health Endpoints

- `GET /info` - Server information
- `GET /health` - Health check
- `GET /servers` - Legacy compatibility endpoint

### MCP Protocol

- `POST /` - Main MCP JSON-RPC endpoint

### Example Tool Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "search_flights",
    "arguments": {
      "origin": "JFK",
      "destination": "LAX", 
      "departure_date": "2024-12-25"
    }
  }
}
```

## Environment Variables

- `PORT` - Server port (default: 8080)
- `HOST` - Server host (default: 0.0.0.0)

## Development Guidelines

### Adding New Tools

1. Create tool class inheriting from `BaseMCPTool`
2. Implement `get_schema()` and `execute()` methods
3. Add to appropriate tool collection
4. Update tool registrations in server

### Code Style

- Follow PEP 8
- Use type hints
- Keep functions under 40 lines
- Keep files under 300 lines
- Write descriptive docstrings

## Requirements

- Python 3.11+
- FastAPI
- httpx
- pydantic

## License

MIT License
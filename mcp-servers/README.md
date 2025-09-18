# Travvy MCP Servers

Model Context Protocol (MCP) servers for the Travvy travel assistant platform.

## Overview

This package contains 5 specialized MCP servers for travel-related functionality:

- **weather_server.py** - Weather information and alerts
- **maps_server.py** - Geographic services and mapping  
- **flights.py** - Flight search and booking
- **accomadation.py** - Hotel and accommodation search
- **train_server.py** - Indian Railways information

## Quick Start

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create and activate virtual environment
uv venv --python 3.11
source .venv/bin/activate

# Install dependencies
uv sync

# Test all servers
uv run python test_servers.py

# Run individual servers
uv run python weather_server.py
uv run python maps_server.py
uv run python flights.py
uv run python accomadation.py
uv run python train_server.py
```

## Environment Variables

Copy `env.example` to `.env` and configure:

- `GOOGLE_MAPS_API_KEY` - For maps_server.py
- `RAPIDAPI_KEY` - For accomadation.py
- `GROQ_API_KEY` - For AI client functionality

## Documentation

See `QUICK_START.md` for detailed setup instructions.

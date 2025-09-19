#!/usr/bin/env python3
"""
Entry point for Travvy MCP Server
"""

import os
import sys
import uvicorn
from dotenv import load_dotenv

# Add src to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from travvy_mcp import get_server

# Load environment variables
load_dotenv()


def main():
    """Main entry point for Cloud Run"""
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    # Initialize the MCP server
    TravvyMCPServer = get_server()
    server = TravvyMCPServer(
        title="Travvy MCP Server",
        version="1.0.0"
    )
    
    app = server.get_app()
    
    print(f"🚀 Starting Travvy MCP Server on {host}:{port}")
    print(f"📋 Protocol: MCP {server.protocol_version}")
    print(f"🛠️  Available tools: {len(server.all_tools)}")
    for tool in server.all_tools:
        print(f"   - {tool.name}: {tool.description}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )


if __name__ == "__main__":
    main()
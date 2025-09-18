#!/usr/bin/env python3
"""
Main application for serving Travvy MCP servers on Cloud Run
"""
import os
import asyncio
from typing import Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import all MCP servers
from flights import mcp as flights_server
from weather_server import mcp as weather_server
from maps_server import maps_server
from train_server import train_server
from accomadation import mcp as accommodation_server

# FastAPI app for Cloud Run
app = FastAPI(
    title="Travvy MCP Servers",
    description="Travel Assistant MCP Servers deployed on Google Cloud Run",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Server registry
servers = {
    "flights": flights_server,
    "weather": weather_server,
    "maps": maps_server,
    "trains": train_server,
    "accommodation": accommodation_server,
}

# Request/Response models
class MCPRequest(BaseModel):
    server: str
    tool: str
    arguments: Dict[str, Any]

class MCPResponse(BaseModel):
    success: bool
    result: Any = None
    error: str = None

@app.get("/")
async def root():
    """Health check and service info"""
    return {
        "service": "Travvy MCP Servers",
        "status": "healthy",
        "available_servers": list(servers.keys()),
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run"""
    return {"status": "healthy", "servers": len(servers)}

@app.get("/servers")
async def list_servers():
    """List all available MCP servers and their tools"""
    server_info = {}
    for name, server in servers.items():
        try:
            # Get available tools from each server
            tools = []
            if hasattr(server, 'tools'):
                tools = list(server.tools.keys())
            server_info[name] = {
                "name": name,
                "tools": tools,
                "status": "available"
            }
        except Exception as e:
            server_info[name] = {
                "name": name,
                "tools": [],
                "status": f"error: {str(e)}"
            }
    return server_info

@app.post("/execute")
async def execute_tool(request: MCPRequest) -> MCPResponse:
    """Execute a tool on a specific MCP server"""
    
    # Validate server exists
    if request.server not in servers:
        raise HTTPException(
            status_code=404, 
            detail=f"Server '{request.server}' not found. Available: {list(servers.keys())}"
        )
    
    server = servers[request.server]
    
    try:
        # Check if tool exists
        if not hasattr(server, 'tools') or request.tool not in server.tools:
            available_tools = list(server.tools.keys()) if hasattr(server, 'tools') else []
            raise HTTPException(
                status_code=404,
                detail=f"Tool '{request.tool}' not found in server '{request.server}'. Available: {available_tools}"
            )
        
        # Execute the tool
        tool_func = server.tools[request.tool]
        
        # Handle both sync and async functions
        if asyncio.iscoroutinefunction(tool_func):
            result = await tool_func(**request.arguments)
        else:
            result = tool_func(**request.arguments)
        
        return MCPResponse(success=True, result=result)
        
    except Exception as e:
        return MCPResponse(success=False, error=str(e))

@app.get("/servers/{server_name}/tools")
async def get_server_tools(server_name: str):
    """Get available tools for a specific server"""
    if server_name not in servers:
        raise HTTPException(status_code=404, detail=f"Server '{server_name}' not found")
    
    server = servers[server_name]
    tools = []
    
    if hasattr(server, 'tools'):
        for tool_name, tool_func in server.tools.items():
            tool_info = {
                "name": tool_name,
                "description": getattr(tool_func, '__doc__', 'No description available')
            }
            tools.append(tool_info)
    
    return {"server": server_name, "tools": tools}

# Specific server endpoints for convenience
@app.post("/flights/{tool_name}")
async def flights_endpoint(tool_name: str, arguments: Dict[str, Any]):
    """Direct flights server endpoint"""
    request = MCPRequest(server="flights", tool=tool_name, arguments=arguments)
    return await execute_tool(request)

@app.post("/weather/{tool_name}")
async def weather_endpoint(tool_name: str, arguments: Dict[str, Any]):
    """Direct weather server endpoint"""
    request = MCPRequest(server="weather", tool=tool_name, arguments=arguments)
    return await execute_tool(request)

@app.post("/maps/{tool_name}")
async def maps_endpoint(tool_name: str, arguments: Dict[str, Any]):
    """Direct maps server endpoint"""
    request = MCPRequest(server="maps", tool=tool_name, arguments=arguments)
    return await execute_tool(request)

@app.post("/trains/{tool_name}")
async def trains_endpoint(tool_name: str, arguments: Dict[str, Any]):
    """Direct trains server endpoint"""
    request = MCPRequest(server="trains", tool=tool_name, arguments=arguments)
    return await execute_tool(request)

@app.post("/accommodation/{tool_name}")
async def accommodation_endpoint(tool_name: str, arguments: Dict[str, Any]):
    """Direct accommodation server endpoint"""
    request = MCPRequest(server="accommodation", tool=tool_name, arguments=arguments)
    return await execute_tool(request)

def main():
    """Main entry point for Cloud Run"""
    port = int(os.getenv("PORT", 8080))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"🚀 Starting Travvy MCP Servers on {host}:{port}")
    print(f"📋 Available servers: {list(servers.keys())}")
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()

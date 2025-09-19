"""
Main MCP Server for Travvy
"""

import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .tools import FlightTools, WeatherTools, TrainTools, AccommodationTools


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TravvyMCPServer:
    """
    Main MCP Server class that implements the Model Context Protocol
    for travel-related tools and services.
    """
    
    def __init__(self, title: str = "Travvy MCP Server", version: str = "1.0.0"):
        self.title = title
        self.version = version
        self.protocol_version = "2024-11-05"
        
        # Initialize FastAPI app
        self.app = FastAPI(
            title=title,
            description="MCP-compliant Travel Assistant Server",
            version=version
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Initialize tools
        self.flight_tools = FlightTools()
        self.weather_tools = WeatherTools()
        self.train_tools = TrainTools()
        self.accommodation_tools = AccommodationTools()
        
        # Collect all tools
        self.all_tools = (
            self.flight_tools.get_all_tools() + 
            self.weather_tools.get_all_tools() +
            self.train_tools.get_all_tools() +
            self.accommodation_tools.get_all_tools()
        )
        
        # Create tool lookup
        self.tool_lookup = {tool.name: tool for tool in self.all_tools}
        
        # Setup routes
        self._setup_routes()
        
        logger.info(f"Initialized {title} with {len(self.all_tools)} tools")
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.post("/")
        async def mcp_handler(request: Request):
            """Main MCP JSON-RPC endpoint"""
            return await self._handle_mcp_request(request)
        
        @self.app.get("/info")
        async def server_info():
            """Server information endpoint"""
            return {
                "service": self.title,
                "status": "healthy",
                "protocol": "MCP",
                "protocolVersion": self.protocol_version,
                "version": self.version,
                "tools": len(self.all_tools),
                "toolNames": [tool.name for tool in self.all_tools]
            }
        
        @self.app.get("/health")
        async def health_check():
            """Health check endpoint for Cloud Run"""
            return {"status": "healthy", "tools": len(self.all_tools)}
        
        @self.app.get("/servers")
        async def list_servers():
            """List available tools (for compatibility)"""
            return {
                "travvy": {
                    "name": "travvy",
                    "tools": [tool.name for tool in self.all_tools],
                    "status": "available"
                }
            }
    
    async def _handle_mcp_request(self, request: Request) -> JSONResponse:
        """Handle MCP JSON-RPC requests"""
        try:
            body = await request.json()
            method = body.get("method")
            params = body.get("params", {})
            request_id = body.get("id")
            
            logger.info(f"Received MCP request: {method}")
            
            if method == "initialize":
                result = await self._handle_initialize(params)
                return JSONResponse(self._create_response(request_id, result))
            
            elif method == "tools/list":
                result = await self._handle_tools_list()
                return JSONResponse(self._create_response(request_id, result))
            
            elif method == "tools/call":
                result = await self._handle_tool_call(params)
                return JSONResponse(self._create_response(request_id, result))
            
            else:
                error = self._create_error(-32601, f"Method not found: {method}")
                return JSONResponse(self._create_response(request_id, error=error))
                
        except json.JSONDecodeError:
            error = self._create_error(-32700, "Parse error: Invalid JSON")
            return JSONResponse(self._create_response(None, error=error))
        
        except Exception as e:
            logger.error(f"Error handling MCP request: {str(e)}")
            error = self._create_error(-32603, f"Internal error: {str(e)}")
            return JSONResponse(self._create_response(None, error=error))
    
    async def _handle_initialize(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle initialize request"""
        client_info = params.get("clientInfo", {})
        logger.info(f"Initializing for client: {client_info}")
        
        return {
            "protocolVersion": self.protocol_version,
            "capabilities": {
                "tools": {},
                "resources": {}
            },
            "serverInfo": {
                "name": "travvy",
                "version": self.version
            }
        }
    
    async def _handle_tools_list(self) -> Dict[str, Any]:
        """Handle tools/list request"""
        tools_list = []
        
        # Add flight tools
        tools_list.extend(self.flight_tools.get_tool_schemas())
        
        # Add weather tools  
        tools_list.extend(self.weather_tools.get_tool_schemas())
        
        # Add train tools
        tools_list.extend(self.train_tools.get_tool_schemas())
        
        # Add accommodation tools
        tools_list.extend(self.accommodation_tools.get_tool_schemas())
        
        logger.info(f"Listing {len(tools_list)} tools")
        return {"tools": tools_list}
    
    async def _handle_tool_call(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Handle tools/call request"""
        tool_name = params.get("name")
        arguments = params.get("arguments", {})
        
        logger.info(f"Calling tool: {tool_name} with args: {arguments}")
        
        if tool_name not in self.tool_lookup:
            raise Exception(f"Tool not found: {tool_name}")
        
        tool = self.tool_lookup[tool_name]
        
        try:
            result = await tool.execute(**arguments)
            
            # Format result for MCP
            if isinstance(result, list):
                text_content = "\n".join(str(item) for item in result)
            else:
                text_content = str(result)
            
            return {
                "content": [
                    {
                        "type": "text",
                        "text": text_content
                    }
                ]
            }
            
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            raise Exception(f"Tool execution failed: {str(e)}")
    
    def _create_response(self, request_id: Optional[str], result: Any = None, error: Dict = None) -> Dict[str, Any]:
        """Create JSON-RPC response"""
        response = {
            "jsonrpc": "2.0",
            "id": request_id
        }
        
        if error:
            response["error"] = error
        else:
            response["result"] = result
        
        return response
    
    def _create_error(self, code: int, message: str, data: Any = None) -> Dict[str, Any]:
        """Create JSON-RPC error"""
        error = {"code": code, "message": message}
        if data:
            error["data"] = data
        return error
    
    def get_app(self) -> FastAPI:
        """Get the FastAPI app instance"""
        return self.app

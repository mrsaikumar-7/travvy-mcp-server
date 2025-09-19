"""
Base tool class for MCP tools
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List
import httpx


class BaseMCPTool(ABC):
    """Base class for all MCP tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_schema(self) -> Dict[str, Any]:
        """Return the JSON schema for this tool"""
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """Execute the tool with given arguments"""
        pass
    
    def to_mcp_tool(self) -> Dict[str, Any]:
        """Convert to MCP tool format"""
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.get_schema()
        }


class HTTPTool(BaseMCPTool):
    """Base class for tools that make HTTP requests"""
    
    def __init__(self, name: str, description: str, timeout: int = 30):
        super().__init__(name, description)
        self.timeout = timeout
    
    async def make_request(self, url: str, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """Make HTTP request with error handling"""
        if headers is None:
            headers = {}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise Exception(f"Network error: {str(e)}")
            except httpx.HTTPStatusError as e:
                raise Exception(f"HTTP error {e.response.status_code}: {e.response.text}")
            except Exception as e:
                raise Exception(f"Unexpected error: {str(e)}")

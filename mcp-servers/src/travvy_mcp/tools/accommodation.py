"""
Accommodation/Hotel tools for MCP
"""

import os
import re
from typing import Any, List, Dict

from .base import HTTPTool
from ..utils.formatters import AccommodationFormatter


class AccommodationTools:
    """Collection of accommodation-related MCP tools"""
    
    def __init__(self):
        self.tools = [
            DestinationSearchTool(),
            HotelSearchTool()
        ]
    
    def get_all_tools(self) -> List[HTTPTool]:
        """Get all accommodation tools"""
        return self.tools
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get all tool schemas in MCP format"""
        return [tool.to_mcp_tool() for tool in self.tools]


class BaseAccommodationTool(HTTPTool):
    """Base class for accommodation tools"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY")
        self.rapidapi_host = os.getenv("RAPIDAPI_HOST", "booking-com15.p.rapidapi.com")
        
        if not self.rapidapi_key:
            raise ValueError("RAPIDAPI_KEY environment variable is required")
    
    async def make_booking_request(self, endpoint: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Make request to Booking.com API via RapidAPI"""
        url = f"https://{self.rapidapi_host}{endpoint}"
        
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": self.rapidapi_host
        }
        
        try:
            return await self.make_request(url, headers)
        except Exception as e:
            return {"error": str(e)}


class DestinationSearchTool(BaseAccommodationTool):
    """Search for hotel destinations by name"""
    
    def __init__(self):
        super().__init__(
            name="search_destinations",
            description="Search for hotel destinations by city or location name"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The destination to search for (e.g., 'Paris', 'New York', 'Tokyo')",
                    "minLength": 2
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, query: str, **kwargs) -> str:
        """Execute destination search"""
        try:
            endpoint = "/api/v1/hotels/searchDestination"
            params = {"query": query}
            
            result = await self.make_booking_request(endpoint, params)
            
            if "error" in result:
                return f"Error searching destinations: {result['error']}"
            
            formatter = AccommodationFormatter()
            return formatter.format_destinations(result, query)
            
        except Exception as e:
            return f"Error searching destinations: {str(e)}"


class HotelSearchTool(BaseAccommodationTool):
    """Get hotels for a specific destination"""
    
    def __init__(self):
        super().__init__(
            name="search_hotels",
            description="Search for hotels in a specific destination"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "destination_id": {
                    "type": "string",
                    "description": "The destination ID (city_ufi from search_destinations)"
                },
                "checkin_date": {
                    "type": "string",
                    "description": "Check-in date in YYYY-MM-DD format",
                    "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
                },
                "checkout_date": {
                    "type": "string",
                    "description": "Check-out date in YYYY-MM-DD format",
                    "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
                },
                "adults": {
                    "type": "integer",
                    "description": "Number of adults",
                    "minimum": 1,
                    "maximum": 10,
                    "default": 2
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of hotels to return",
                    "minimum": 1,
                    "maximum": 50,
                    "default": 10
                }
            },
            "required": ["destination_id", "checkin_date", "checkout_date"]
        }
    
    async def execute(self, destination_id: str, checkin_date: str, checkout_date: str,
                     adults: int = 2, max_results: int = 10, **kwargs) -> str:
        """Execute hotel search"""
        try:
            endpoint = "/api/v1/hotels/searchHotels"
            params = {
                "dest_id": destination_id,
                "search_type": "CITY",
                "arrival_date": checkin_date,
                "departure_date": checkout_date,
                "adults": str(adults)
            }
            
            result = await self.make_booking_request(endpoint, params)
            
            if "error" in result:
                return f"Error searching hotels: {result['error']}"
            
            formatter = AccommodationFormatter()
            return formatter.format_hotels(result, destination_id, max_results)
            
        except Exception as e:
            return f"Error searching hotels: {str(e)}"

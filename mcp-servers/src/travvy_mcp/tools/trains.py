"""
Train tools for MCP - Indian Railways
"""

import os
from typing import Any, List, Dict
import json
import httpx

from .base import HTTPTool


class TrainTools:
    """Collection of train-related MCP tools"""
    
    def __init__(self):
        self.tools = [
            StationStatusTool(),
            TrainDetailsTool(),
            TrainsBetweenStationsTool(),
            TrainRouteTool(),
            TrainsOnDateTool(),
            PNRStatusTool(),
            StationSearchTool(),
            SeatAvailabilityTool()
        ]
    
    def get_all_tools(self) -> List[HTTPTool]:
        """Get all train tools"""
        return self.tools
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get all tool schemas in MCP format"""
        return [tool.to_mcp_tool() for tool in self.tools]


class BaseTrainTool(HTTPTool):
    """Base class for train tools"""
    
    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.base_url = "https://irctc1.p.rapidapi.com"
        self.api_key = os.getenv("RAPIDAPI_KEY")  # From environment
        
        if not self.api_key:
            # For demo purposes, use a placeholder that will show error
            self.api_key = "demo-key-missing"
    
    async def make_train_request(self, endpoint: str, params: Dict[str, str] = None) -> Dict[str, Any]:
        """Make request to train API"""
        if self.api_key == "demo-key-missing":
            return {
                "error": "RAPIDAPI_KEY environment variable not set. Please configure your API key.",
                "demo": True,
                "endpoint": endpoint,
                "params": params
            }
        
        headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "irctc1.p.rapidapi.com"
        }
        
        url = f"{self.base_url}{endpoint}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, headers=headers, params=params, timeout=30.0)
                response.raise_for_status()
                return response.json()
            except Exception as e:
                return {"error": str(e)}


class StationStatusTool(BaseTrainTool):
    """Get live station status"""
    
    def __init__(self):
        super().__init__(
            name="get_station_live_status",
            description="Get live status of trains at a railway station"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "station_code": {
                    "type": "string",
                    "description": "Railway station code (e.g., NDLS for New Delhi)",
                    "pattern": "^[A-Z]{3,5}$"
                }
            },
            "required": ["station_code"]
        }
    
    async def execute(self, station_code: str, **kwargs) -> str:
        """Execute station status request"""
        try:
            station_code = station_code.upper()
            endpoint = f"/api/v3/station/live/{station_code}"
            result = await self.make_train_request(endpoint)
            
            if "error" in result:
                return f"Error getting station status: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting station status: {str(e)}"


class TrainDetailsTool(BaseTrainTool):
    """Get train details by train number"""
    
    def __init__(self):
        super().__init__(
            name="get_train_details",
            description="Get detailed information about a train by its number"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "train_number": {
                    "type": "string",
                    "description": "Train number (e.g., 12951, 22691)",
                    "pattern": "^[0-9]{4,5}$"
                }
            },
            "required": ["train_number"]
        }
    
    async def execute(self, train_number: str, **kwargs) -> str:
        """Execute train details request"""
        try:
            endpoint = f"/api/v3/trainDetails/{train_number}"
            result = await self.make_train_request(endpoint)
            
            if "error" in result:
                return f"Error getting train details: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting train details: {str(e)}"


class TrainsBetweenStationsTool(BaseTrainTool):
    """Get trains between two stations"""
    
    def __init__(self):
        super().__init__(
            name="get_trains_between_stations",
            description="Get list of trains running between two railway stations"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "from_station": {
                    "type": "string",
                    "description": "Source station code (e.g., NDLS)",
                    "pattern": "^[A-Z]{3,5}$"
                },
                "to_station": {
                    "type": "string",
                    "description": "Destination station code (e.g., BCT)",
                    "pattern": "^[A-Z]{3,5}$"
                }
            },
            "required": ["from_station", "to_station"]
        }
    
    async def execute(self, from_station: str, to_station: str, **kwargs) -> str:
        """Execute trains between stations request"""
        try:
            from_station = from_station.upper()
            to_station = to_station.upper()
            endpoint = f"/api/v3/trains/{from_station}/{to_station}"
            result = await self.make_train_request(endpoint)
            
            if "error" in result:
                return f"Error getting trains: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting trains between stations: {str(e)}"


class TrainRouteTool(BaseTrainTool):
    """Get train route by train number"""
    
    def __init__(self):
        super().__init__(
            name="get_train_route",
            description="Get the complete route of a train with all stations"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "train_number": {
                    "type": "string",
                    "description": "Train number (e.g., 12951)",
                    "pattern": "^[0-9]{4,5}$"
                }
            },
            "required": ["train_number"]
        }
    
    async def execute(self, train_number: str, **kwargs) -> str:
        """Execute train route request"""
        try:
            endpoint = f"/api/v3/route/{train_number}"
            result = await self.make_train_request(endpoint)
            
            if "error" in result:
                return f"Error getting train route: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting train route: {str(e)}"


class TrainsOnDateTool(BaseTrainTool):
    """Get trains between stations on specific date"""
    
    def __init__(self):
        super().__init__(
            name="get_trains_on_date",
            description="Get trains between two stations on a specific date"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "from_station": {
                    "type": "string",
                    "description": "Source station code",
                    "pattern": "^[A-Z]{3,5}$"
                },
                "to_station": {
                    "type": "string",
                    "description": "Destination station code", 
                    "pattern": "^[A-Z]{3,5}$"
                },
                "date": {
                    "type": "string",
                    "description": "Travel date in YYYY-MM-DD format",
                    "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
                }
            },
            "required": ["from_station", "to_station", "date"]
        }
    
    async def execute(self, from_station: str, to_station: str, date: str, **kwargs) -> str:
        """Execute trains on date request"""
        try:
            params = {
                "from": from_station.upper(),
                "to": to_station.upper(),
                "date": date
            }
            endpoint = "/api/v3/trains/date"
            result = await self.make_train_request(endpoint, params)
            
            if "error" in result:
                return f"Error getting trains on date: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting trains on date: {str(e)}"


class PNRStatusTool(BaseTrainTool):
    """Get PNR status"""
    
    def __init__(self):
        super().__init__(
            name="get_pnr_status",
            description="Get PNR (Passenger Name Record) status and booking details"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pnr_number": {
                    "type": "string",
                    "description": "10-digit PNR number",
                    "pattern": "^[0-9]{10}$"
                }
            },
            "required": ["pnr_number"]
        }
    
    async def execute(self, pnr_number: str, **kwargs) -> str:
        """Execute PNR status request"""
        try:
            endpoint = f"/api/v3/pnr/{pnr_number}"
            result = await self.make_train_request(endpoint)
            
            if "error" in result:
                return f"Error getting PNR status: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting PNR status: {str(e)}"


class StationSearchTool(BaseTrainTool):
    """Search for railway stations"""
    
    def __init__(self):
        super().__init__(
            name="search_station",
            description="Search for railway stations by name or code"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Station name or partial name to search for"
                }
            },
            "required": ["query"]
        }
    
    async def execute(self, query: str, **kwargs) -> str:
        """Execute station search request"""
        try:
            params = {"search": query}
            endpoint = "/api/v3/station/search"
            result = await self.make_train_request(endpoint, params)
            
            if "error" in result:
                return f"Error searching stations: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error searching stations: {str(e)}"


class SeatAvailabilityTool(BaseTrainTool):
    """Get seat availability for a train"""
    
    def __init__(self):
        super().__init__(
            name="get_seat_availability",
            description="Check seat availability for a train on specific date and class"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "train_number": {
                    "type": "string",
                    "description": "Train number",
                    "pattern": "^[0-9]{4,5}$"
                },
                "from_station": {
                    "type": "string",
                    "description": "Source station code",
                    "pattern": "^[A-Z]{3,5}$"
                },
                "to_station": {
                    "type": "string",
                    "description": "Destination station code",
                    "pattern": "^[A-Z]{3,5}$"
                },
                "date": {
                    "type": "string",
                    "description": "Travel date in YYYY-MM-DD format",
                    "pattern": "^[0-9]{4}-[0-9]{2}-[0-9]{2}$"
                },
                "class_type": {
                    "type": "string",
                    "description": "Class type (SL, 3A, 2A, 1A, CC, EC, etc.)",
                    "default": "SL"
                }
            },
            "required": ["train_number", "from_station", "to_station", "date"]
        }
    
    async def execute(self, train_number: str, from_station: str, to_station: str, 
                     date: str, class_type: str = "SL", **kwargs) -> str:
        """Execute seat availability request"""
        try:
            params = {
                "trainNumber": train_number,
                "fromStationCode": from_station.upper(),
                "toStationCode": to_station.upper(),
                "date": date,
                "class": class_type
            }
            endpoint = "/api/v3/seatAvailability"
            result = await self.make_train_request(endpoint, params)
            
            if "error" in result:
                return f"Error getting seat availability: {result['error']}"
            
            return json.dumps(result, indent=2)
            
        except Exception as e:
            return f"Error getting seat availability: {str(e)}"

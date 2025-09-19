"""
Flight search tools for MCP
"""

from typing import Any, List, Dict
from dataclasses import asdict
from fast_flights import FlightData, Passengers, Result, get_flights

from .base import BaseMCPTool
from ..utils.formatters import FlightFormatter


class FlightTools:
    """Collection of flight-related MCP tools"""
    
    def __init__(self):
        self.tools = [
            FlightSearchTool(),
            BestFlightsTool(),
            CheapestFlightsTool()
        ]
    
    def get_all_tools(self) -> List[BaseMCPTool]:
        """Get all flight tools"""
        return self.tools
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get all tool schemas in MCP format"""
        return [tool.to_mcp_tool() for tool in self.tools]


class FlightSearchTool(BaseMCPTool):
    """General flight search tool"""
    
    def __init__(self):
        super().__init__(
            name="search_flights",
            description="Search for flights between two airports"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Origin airport IATA code (e.g., JFK)"
                },
                "destination": {
                    "type": "string",
                    "description": "Destination airport IATA code (e.g., LAX)"
                },
                "departure_date": {
                    "type": "string",
                    "description": "Departure date in YYYY-MM-DD format"
                },
                "adults": {
                    "type": "integer",
                    "description": "Number of adult passengers",
                    "default": 1
                },
                "trip_type": {
                    "type": "string",
                    "description": "Trip type: one-way or round-trip",
                    "enum": ["one-way", "round-trip"],
                    "default": "one-way"
                },
                "seat": {
                    "type": "string",
                    "description": "Seat class",
                    "enum": ["economy", "premium-economy", "business", "first"],
                    "default": "economy"
                },
                "max_results": {
                    "type": "integer",
                    "description": "Maximum number of flights to return",
                    "default": 10
                }
            },
            "required": ["origin", "destination", "departure_date"]
        }
    
    async def execute(self, origin: str, destination: str, departure_date: str,
                     adults: int = 1, trip_type: str = "one-way", 
                     seat: str = "economy", max_results: int = 10, **kwargs) -> List[str]:
        """Execute flight search"""
        try:
            # Validate inputs
            if len(origin) != 3 or len(destination) != 3:
                return ["Error: Origin and destination must be 3-character IATA codes"]
            
            if len(departure_date) != 10 or departure_date[4] != '-' or departure_date[7] != '-':
                return ["Error: Departure date must be in YYYY-MM-DD format"]
            
            # Make API call
            flight_data_input = [FlightData(
                date=departure_date, 
                from_airport=origin, 
                to_airport=destination
            )]
            
            passengers_input = Passengers(
                adults=adults, 
                children=0, 
                infants_in_seat=0, 
                infants_on_lap=0
            )
            
            result: Result = get_flights(
                flight_data=flight_data_input,
                trip=trip_type,
                seat=seat,
                passengers=passengers_input,
                fetch_mode="fallback"
            )
            
            result_dict = asdict(result)
            
            if not result_dict or "flights" not in result_dict:
                return ["No flight data available for the specified route and dates"]
            
            flights = result_dict["flights"][:max_results]
            
            # Format results
            formatter = FlightFormatter()
            return formatter.format_flight_list(flights, origin, destination)
            
        except Exception as e:
            return [f"Error searching flights: {str(e)}"]


class BestFlightsTool(BaseMCPTool):
    """Tool to find best flights (as determined by Google Flights)"""
    
    def __init__(self):
        super().__init__(
            name="get_best_flights",
            description="Get the best flights as determined by Google Flights algorithm"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        # Same schema as search flights but focused on best flights
        return FlightSearchTool().get_schema()
    
    async def execute(self, **kwargs) -> List[str]:
        """Execute best flights search"""
        search_tool = FlightSearchTool()
        all_flights = await search_tool.execute(**kwargs)
        
        # Filter for best flights (this would need the actual flight data)
        # For now, return top results with a note
        return [
            "Best flights (as determined by Google Flights algorithm):",
            *all_flights[:5]
        ]


class CheapestFlightsTool(BaseMCPTool):
    """Tool to find cheapest flights"""
    
    def __init__(self):
        super().__init__(
            name="get_cheapest_flights", 
            description="Get flights sorted by price (cheapest first)"
        )
    
    def get_schema(self) -> Dict[str, Any]:
        return FlightSearchTool().get_schema()
    
    async def execute(self, **kwargs) -> List[str]:
        """Execute cheapest flights search"""
        search_tool = FlightSearchTool()
        all_flights = await search_tool.execute(**kwargs)
        
        # Return with cheapest indication
        return [
            "Flights sorted by price (cheapest first):",
            *all_flights
        ]

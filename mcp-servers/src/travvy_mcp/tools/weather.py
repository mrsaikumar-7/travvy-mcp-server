"""
Weather tools for MCP
"""

from typing import Any, List, Dict

from .base import HTTPTool
from ..utils.formatters import WeatherFormatter


class WeatherTools:
    """Collection of weather-related MCP tools"""
    
    def __init__(self):
        self.tools = [
            WeatherForecastTool(),
            WeatherAlertsTool()
        ]
    
    def get_all_tools(self) -> List[HTTPTool]:
        """Get all weather tools"""
        return self.tools
    
    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Get all tool schemas in MCP format"""
        return [tool.to_mcp_tool() for tool in self.tools]


class WeatherForecastTool(HTTPTool):
    """Weather forecast tool using National Weather Service API"""
    
    def __init__(self):
        super().__init__(
            name="get_weather_forecast",
            description="Get weather forecast for a location using latitude and longitude"
        )
        self.nws_base = "https://api.weather.gov"
        self.user_agent = "travvy-mcp/1.0"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "latitude": {
                    "type": "number",
                    "description": "Latitude of the location",
                    "minimum": -90,
                    "maximum": 90
                },
                "longitude": {
                    "type": "number", 
                    "description": "Longitude of the location",
                    "minimum": -180,
                    "maximum": 180
                },
                "days": {
                    "type": "integer",
                    "description": "Number of forecast days to return",
                    "minimum": 1,
                    "maximum": 7,
                    "default": 5
                }
            },
            "required": ["latitude", "longitude"]
        }
    
    async def execute(self, latitude: float, longitude: float, days: int = 5, **kwargs) -> str:
        """Execute weather forecast request"""
        try:
            headers = {
                "User-Agent": self.user_agent,
                "Accept": "application/geo+json"
            }
            
            # Get forecast grid endpoint
            points_url = f"{self.nws_base}/points/{latitude},{longitude}"
            points_data = await self.make_request(points_url, headers)
            
            if not points_data:
                return "Unable to fetch forecast data for this location"
            
            # Get forecast
            forecast_url = points_data["properties"]["forecast"]
            forecast_data = await self.make_request(forecast_url, headers)
            
            if not forecast_data:
                return "Unable to fetch detailed forecast"
            
            # Format forecast
            periods = forecast_data["properties"]["periods"][:days * 2]  # Day and night
            formatter = WeatherFormatter()
            return formatter.format_forecast(periods)
            
        except Exception as e:
            return f"Error getting weather forecast: {str(e)}"


class WeatherAlertsTool(HTTPTool):
    """Weather alerts tool for US states"""
    
    def __init__(self):
        super().__init__(
            name="get_weather_alerts",
            description="Get active weather alerts for a US state"
        )
        self.nws_base = "https://api.weather.gov"
        self.user_agent = "travvy-mcp/1.0"
    
    def get_schema(self) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "state": {
                    "type": "string",
                    "description": "Two-letter US state code (e.g., CA, NY, TX)",
                    "pattern": "^[A-Z]{2}$",
                    "minLength": 2,
                    "maxLength": 2
                },
                "max_alerts": {
                    "type": "integer",
                    "description": "Maximum number of alerts to return",
                    "minimum": 1,
                    "maximum": 20,
                    "default": 5
                }
            },
            "required": ["state"]
        }
    
    async def execute(self, state: str, max_alerts: int = 5, **kwargs) -> str:
        """Execute weather alerts request"""
        try:
            state = state.upper()  # Ensure uppercase
            
            headers = {
                "User-Agent": self.user_agent,
                "Accept": "application/geo+json"
            }
            
            url = f"{self.nws_base}/alerts/active/area/{state}"
            data = await self.make_request(url, headers)
            
            if not data.get("features"):
                return f"No active weather alerts for {state}"
            
            alerts = data["features"][:max_alerts]
            formatter = WeatherFormatter()
            return formatter.format_alerts(alerts, state)
            
        except Exception as e:
            return f"Error getting weather alerts: {str(e)}"

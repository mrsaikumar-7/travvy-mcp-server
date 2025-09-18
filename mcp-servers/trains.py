"""
Indian Railways API integration functions.
Provides functions to interact with Indian Railways data and services.
"""

import httpx
import asyncio
from typing import Dict, List, Any, Optional
import logging

logger = logging.getLogger(__name__)

# Base URLs for Indian Railways APIs
IRCTC_BASE_URL = "https://www.indianrail.gov.in"
RTT_API_BASE = "https://rtt-api.herokuapp.com"

async def get_station_live_status(station_code: str) -> Dict[str, Any]:
    """
    Get live status of trains at a station.
    
    Args:
        station_code: Station code (e.g., 'NDLS' for New Delhi)
        
    Returns:
        Dictionary containing live train status
    """
    try:
        async with httpx.AsyncClient() as client:
            # Using a mock response for demonstration
            # In production, replace with actual API call
            response = {
                "station": station_code,
                "trains": [
                    {
                        "train_number": "12951",
                        "train_name": "Mumbai Rajdhani Express",
                        "arrival_time": "06:55",
                        "departure_time": "07:00",
                        "status": "On Time",
                        "platform": "16"
                    }
                ]
            }
            return response
    except Exception as e:
        logger.error(f"Error fetching station status: {e}")
        return {"error": str(e)}

async def get_train_details(train_number: str) -> Dict[str, Any]:
    """
    Get details of a specific train.
    
    Args:
        train_number: Train number (e.g., '12951')
        
    Returns:
        Dictionary containing train details
    """
    try:
        async with httpx.AsyncClient() as client:
            # Mock response - replace with actual API in production
            response = {
                "train_number": train_number,
                "train_name": f"Train {train_number}",
                "source": "New Delhi",
                "destination": "Mumbai Central",
                "departure_time": "17:55",
                "arrival_time": "08:35",
                "duration": "14h 40m",
                "days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
            }
            return response
    except Exception as e:
        logger.error(f"Error fetching train details: {e}")
        return {"error": str(e)}

async def get_trains_between_stations(source: str, destination: str, date: str = None) -> List[Dict[str, Any]]:
    """
    Get trains running between two stations.
    
    Args:
        source: Source station code
        destination: Destination station code
        date: Travel date (optional)
        
    Returns:
        List of trains between stations
    """
    try:
        async with httpx.AsyncClient() as client:
            # Mock response - replace with actual API in production
            trains = [
                {
                    "train_number": "12951",
                    "train_name": "Mumbai Rajdhani Express",
                    "departure_time": "17:55",
                    "arrival_time": "08:35",
                    "duration": "14h 40m",
                    "available_classes": ["1A", "2A", "3A"]
                },
                {
                    "train_number": "12953",
                    "train_name": "August Kranti Rajdhani Express",
                    "departure_time": "17:00",
                    "arrival_time": "08:55",
                    "duration": "15h 55m",
                    "available_classes": ["1A", "2A", "3A"]
                }
            ]
            return trains
    except Exception as e:
        logger.error(f"Error fetching trains between stations: {e}")
        return [{"error": str(e)}]

async def get_train_route(train_number: str) -> List[Dict[str, Any]]:
    """
    Get route/schedule of a train.
    
    Args:
        train_number: Train number
        
    Returns:
        List of stations in the route with timings
    """
    try:
        async with httpx.AsyncClient() as client:
            # Mock response - replace with actual API in production
            route = [
                {
                    "station_code": "NDLS",
                    "station_name": "New Delhi",
                    "arrival_time": None,
                    "departure_time": "17:55",
                    "halt_time": "0m",
                    "distance": 0
                },
                {
                    "station_code": "KOT",
                    "station_name": "Kota",
                    "arrival_time": "23:40",
                    "departure_time": "23:50",
                    "halt_time": "10m",
                    "distance": 465
                },
                {
                    "station_code": "BCTR",
                    "station_name": "Mumbai Central",
                    "arrival_time": "08:35",
                    "departure_time": None,
                    "halt_time": "0m",
                    "distance": 1384
                }
            ]
            return route
    except Exception as e:
        logger.error(f"Error fetching train route: {e}")
        return [{"error": str(e)}]

async def get_trains_on_date(station_code: str, date: str) -> List[Dict[str, Any]]:
    """
    Get trains running on a specific date from a station.
    
    Args:
        station_code: Station code
        date: Date in YYYY-MM-DD format
        
    Returns:
        List of trains on the given date
    """
    try:
        async with httpx.AsyncClient() as client:
            # Mock response - replace with actual API in production
            trains = [
                {
                    "train_number": "12951",
                    "train_name": "Mumbai Rajdhani Express",
                    "departure_time": "17:55",
                    "destination": "Mumbai Central",
                    "available": True
                },
                {
                    "train_number": "12953",
                    "train_name": "August Kranti Rajdhani Express", 
                    "departure_time": "17:00",
                    "destination": "Mumbai Central",
                    "available": True
                }
            ]
            return trains
    except Exception as e:
        logger.error(f"Error fetching trains on date: {e}")
        return [{"error": str(e)}]

# Utility functions for station code lookup
async def get_pnr_status(pnr_number: str) -> Dict[str, Any]:
    """
    Get PNR status for a train ticket.
    
    Args:
        pnr_number: 10-digit PNR number
        
    Returns:
        Dictionary containing PNR status information
    """
    try:
        async with httpx.AsyncClient() as client:
            # Mock response - replace with actual API in production
            response = {
                "pnr_number": pnr_number,
                "train_number": "12951",
                "train_name": "Mumbai Rajdhani Express",
                "boarding_station": "NDLS",
                "destination_station": "CSMT",
                "journey_date": "2024-01-15",
                "passengers": [
                    {
                        "name": "PASSENGER 1",
                        "age": 35,
                        "status": "CNF/B1/25",
                        "coach": "B1",
                        "berth": "25"
                    }
                ],
                "chart_status": "CHART PREPARED"
            }
            return response
    except Exception as e:
        logger.error(f"Error fetching PNR status: {e}")
        return {"error": str(e)}

async def search_station(query: str) -> List[Dict[str, Any]]:
    """
    Search for station by name or code.
    
    Args:
        query: Station name or code to search
        
    Returns:
        List of matching stations
    """
    try:
        # Mock station data - replace with actual API in production
        stations = [
            {"code": "NDLS", "name": "New Delhi", "state": "Delhi"},
            {"code": "CSMT", "name": "Mumbai CST", "state": "Maharashtra"},
            {"code": "SBC", "name": "Bangalore City", "state": "Karnataka"},
            {"code": "MAS", "name": "Chennai Central", "state": "Tamil Nadu"},
            {"code": "HWH", "name": "Howrah", "state": "West Bengal"}
        ]
        
        # Filter stations based on query
        matching_stations = [
            station for station in stations
            if query.upper() in station["code"] or query.lower() in station["name"].lower()
        ]
        
        return matching_stations
    except Exception as e:
        logger.error(f"Error searching stations: {e}")
        return [{"error": str(e)}]

async def get_seat_availability(train_number: str, source: str, destination: str, date: str, quota: str = "GN") -> Dict[str, Any]:
    """
    Get seat availability for a train.
    
    Args:
        train_number: Train number
        source: Source station code
        destination: Destination station code
        date: Travel date in YYYY-MM-DD format
        quota: Quota type (GN, TQ, etc.)
        
    Returns:
        Dictionary containing seat availability information
    """
    try:
        # Mock response - replace with actual API in production
        availability = {
            "train_number": train_number,
            "train_name": f"Train {train_number}",
            "source": source,
            "destination": destination,
            "date": date,
            "quota": quota,
            "classes": {
                "1A": {"available": 5, "status": "AVAILABLE"},
                "2A": {"available": 15, "status": "AVAILABLE"},
                "3A": {"available": 30, "status": "AVAILABLE"},
                "SL": {"available": 120, "status": "AVAILABLE"}
            }
        }
        return availability
    except Exception as e:
        logger.error(f"Error fetching seat availability: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    # Test the functions
    async def test():
        print("Testing train functions...")
        
        # Test station search
        stations = await search_station("delhi")
        print(f"Stations matching 'delhi': {stations}")
        
        # Test train details
        details = await get_train_details("12951")
        print(f"Train details: {details}")
        
        # Test trains between stations
        trains = await get_trains_between_stations("NDLS", "CSMT")
        print(f"Trains between NDLS and CSMT: {trains}")
    
    asyncio.run(test())

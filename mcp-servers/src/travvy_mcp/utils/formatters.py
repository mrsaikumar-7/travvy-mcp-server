"""
Formatters for tool responses
"""

import re
from typing import List, Dict, Any


class FlightFormatter:
    """Formatter for flight data"""
    
    @staticmethod
    def format_flight_list(flights: List[Dict[str, Any]], origin: str, destination: str) -> List[str]:
        """Format a list of flights into readable strings"""
        if not flights:
            return ["No flights found for the specified route and dates"]
        
        formatted_flights = []
        for i, flight in enumerate(flights, 1):
            formatted = FlightFormatter.format_single_flight(flight, origin, destination, i)
            formatted_flights.append(formatted)
        
        return formatted_flights
    
    @staticmethod
    def format_single_flight(flight: Dict[str, Any], origin: str, destination: str, index: int = None) -> str:
        """Format a single flight into a readable string"""
        try:
            # Basic flight info
            airline = flight.get('name', 'Unknown Airline')
            price = flight.get('price', 'Price not available')
            departure = flight.get('departure', 'Departure time not available')
            arrival = flight.get('arrival', 'Arrival time not available')
            duration = flight.get('duration', 'Duration not available')
            stops = flight.get('stops', 0)
            
            # Format stops
            stops_text = "non-stop" if stops == 0 else f"{stops} stop{'s' if stops != 1 else ''}"
            
            # Format best flight indicator
            is_best = flight.get('is_best', False)
            best_indicator = " ⭐ (Best option)" if is_best else ""
            
            # Build formatted string
            prefix = f"Flight {index}: " if index else ""
            
            formatted = (
                f"{prefix}{airline} - {price}{best_indicator}\n"
                f"  Route: {origin} → {destination}\n" 
                f"  Departure: {departure}\n"
                f"  Arrival: {arrival}\n"
                f"  Duration: {duration} ({stops_text})"
            )
            
            return formatted
            
        except Exception as e:
            return f"Error formatting flight data: {str(e)}"
    
    @staticmethod
    def format_duration(duration_str: str) -> str:
        """Format duration string to be more readable"""
        try:
            parts = duration_str.split()
            if len(parts) == 4:  # "5 h 30 m" format
                return f"{parts[0]} hours and {parts[2]} minutes"
            return duration_str
        except:
            return duration_str


class WeatherFormatter:
    """Formatter for weather data"""
    
    @staticmethod
    def format_forecast(periods: List[Dict[str, Any]]) -> str:
        """Format weather forecast periods"""
        if not periods:
            return "No forecast data available"
        
        formatted_periods = []
        for period in periods:
            try:
                name = period.get('name', 'Unknown period')
                temp = period.get('temperature', 'N/A')
                temp_unit = period.get('temperatureUnit', 'F')
                wind_speed = period.get('windSpeed', 'N/A')
                wind_direction = period.get('windDirection', 'N/A')
                short_forecast = period.get('shortForecast', 'No description')
                detailed_forecast = period.get('detailedForecast', '')
                
                # Use detailed forecast if available and reasonably short
                description = detailed_forecast if len(detailed_forecast) < 200 else short_forecast
                
                formatted = (
                    f"{name}:\n"
                    f"  Temperature: {temp}°{temp_unit}\n"
                    f"  Wind: {wind_speed} {wind_direction}\n"
                    f"  Conditions: {description}"
                )
                
                formatted_periods.append(formatted)
                
            except Exception as e:
                formatted_periods.append(f"Error formatting period data: {str(e)}")
        
        return "\n\n".join(formatted_periods)
    
    @staticmethod
    def format_alerts(alerts: List[Dict[str, Any]], state: str) -> str:
        """Format weather alerts"""
        if not alerts:
            return f"No active weather alerts for {state}"
        
        formatted_alerts = []
        formatted_alerts.append(f"Active Weather Alerts for {state}:")
        formatted_alerts.append("=" * 40)
        
        for i, alert in enumerate(alerts, 1):
            try:
                props = alert.get('properties', {})
                event = props.get('event', 'Unknown Event')
                area = props.get('areaDesc', 'Unknown Area')
                severity = props.get('severity', 'Unknown')
                urgency = props.get('urgency', 'Unknown')
                description = props.get('description', 'No description available')
                
                # Truncate long descriptions
                if len(description) > 300:
                    description = description[:297] + "..."
                
                formatted = (
                    f"{i}. {event}\n"
                    f"   Area: {area}\n"
                    f"   Severity: {severity} | Urgency: {urgency}\n"
                    f"   Description: {description}"
                )
                
                formatted_alerts.append(formatted)
                
            except Exception as e:
                formatted_alerts.append(f"Error formatting alert {i}: {str(e)}")
        
        return "\n\n".join(formatted_alerts)


class AccommodationFormatter:
    """Formatter for accommodation/hotel data"""
    
    @staticmethod
    def format_destinations(result: Dict[str, Any], query: str) -> str:
        """Format destination search results"""
        if "error" in result:
            return f"Error fetching destinations: {result['error']}"
        
        if "data" not in result or not isinstance(result["data"], list):
            return "Unexpected response format from the API."
        
        destinations = result["data"]
        if not destinations:
            return "No destinations found matching your query."
        
        formatted_results = []
        for destination in destinations:
            dest_info = (
                f"Name: {destination.get('name', 'Unknown')}\n"
                f"Type: {destination.get('dest_type', 'Unknown')}\n"
                f"City ID: {destination.get('city_ufi', 'N/A')}\n"
                f"Region: {destination.get('region', 'Unknown')}\n"
                f"Country: {destination.get('country', 'Unknown')}\n"
                f"Coordinates: {destination.get('latitude', 'N/A')}, {destination.get('longitude', 'N/A')}"
            )
            formatted_results.append(dest_info)
        
        return f"Found {len(destinations)} destinations for '{query}':\n\n" + "\n---\n".join(formatted_results)
    
    @staticmethod
    def format_hotels(result: Dict[str, Any], destination_id: str, max_results: int = 10) -> str:
        """Format hotel search results"""
        if "error" in result:
            return f"Error fetching hotels: {result['error']}"
        
        if "data" not in result or "hotels" not in result["data"]:
            return "Unexpected response format from the API."
        
        hotels = result["data"]["hotels"]
        if not hotels:
            return "No hotels found for this destination and dates."
        
        # Limit results
        hotels = hotels[:max_results]
        formatted_results = []
        
        for i, hotel_entry in enumerate(hotels, 1):
            if "property" not in hotel_entry:
                formatted_results.append(f"Hotel {i}: Information not available")
                continue
            
            property_data = hotel_entry["property"]
            
            # Parse room info from accessibility label
            room_info = "Not available"
            accessibility_label = hotel_entry.get("accessibilityLabel", "")
            if accessibility_label:
                room_match = re.search(r'(Hotel room|Entire villa|Private suite|Private room)[^\.]*', accessibility_label)
                if room_match:
                    room_info = room_match.group(0).strip()
            
            # Build hotel info
            hotel_info = f"Hotel {i}: {property_data.get('name', 'Unknown')}\n"
            hotel_info += f"  Location: {property_data.get('wishlistName', 'Unknown')}\n"
            hotel_info += f"  Rating: {property_data.get('reviewScore', 'N/A')}/10"
            
            review_count = property_data.get('reviewCount', 'N/A')
            review_word = property_data.get('reviewScoreWord', 'N/A')
            if review_count != 'N/A' and review_word != 'N/A':
                hotel_info += f" ({review_count} reviews - {review_word})\n"
            else:
                hotel_info += "\n"
            
            hotel_info += f"  Room: {room_info}\n"
            
            # Price information
            if "priceBreakdown" in property_data and "grossPrice" in property_data["priceBreakdown"]:
                price_data = property_data["priceBreakdown"]["grossPrice"]
                currency = price_data.get('currency', '$')
                value = price_data.get('value', 'N/A')
                hotel_info += f"  Price: {currency}{value}\n"
                
                # Discount info
                if "strikethroughPrice" in property_data["priceBreakdown"]:
                    original_price = property_data["priceBreakdown"]["strikethroughPrice"].get("value")
                    if original_price:
                        try:
                            current = float(value)
                            original = float(original_price)
                            if original > current:
                                discount_pct = round((1 - current/original) * 100)
                                hotel_info += f"  Discount: {discount_pct}% off\n"
                        except (ValueError, TypeError):
                            pass
            else:
                hotel_info += "  Price: Not available\n"
            
            # Additional info
            if property_data.get('propertyClass'):
                hotel_info += f"  Stars: {property_data['propertyClass']}\n"
            
            if property_data.get('latitude') and property_data.get('longitude'):
                hotel_info += f"  Coordinates: {property_data['latitude']}, {property_data['longitude']}\n"
            
            # Check-in/out times
            checkin = property_data.get('checkin', {})
            checkout = property_data.get('checkout', {})
            if checkin:
                hotel_info += f"  Check-in: {checkin.get('fromTime', 'N/A')}-{checkin.get('untilTime', 'N/A')}\n"
            if checkout:
                hotel_info += f"  Check-out: by {checkout.get('untilTime', 'N/A')}\n"
            
            # Photo URL
            if property_data.get('photoUrls') and property_data['photoUrls']:
                hotel_info += f"  Photo: {property_data['photoUrls'][0]}"
            
            formatted_results.append(hotel_info.rstrip())
        
        return f"Found {len(hotels)} hotels for destination {destination_id}:\n\n" + "\n\n".join(formatted_results)

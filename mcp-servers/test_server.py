#!/usr/bin/env python3
"""
Test script for the modular Travvy MCP Server
"""

import sys
import os
import json
import asyncio

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

async def test_server():
    """Test the modular server functionality"""
    try:
        # Test imports
        print("🧪 Testing imports...")
        from travvy_mcp import TravvyMCPServer
        from travvy_mcp.tools import FlightTools, WeatherTools
        from travvy_mcp.utils import FlightFormatter, WeatherFormatter
        print("✅ All imports successful")
        
        # Test server initialization
        print("\n🏗️ Testing server initialization...")
        server = TravvyMCPServer(title="Test Travvy MCP Server", version="1.0.0")
        print(f"✅ Server initialized with {len(server.all_tools)} tools")
        
        # Test tool schemas
        print("\n📋 Testing tool schemas...")
        flight_tools = FlightTools()
        weather_tools = WeatherTools()
        
        flight_schemas = flight_tools.get_tool_schemas()
        weather_schemas = weather_tools.get_tool_schemas()
        
        print(f"✅ Flight tools: {len(flight_schemas)} schemas")
        for schema in flight_schemas:
            print(f"   - {schema['name']}: {schema['description']}")
        
        print(f"✅ Weather tools: {len(weather_schemas)} schemas")
        for schema in weather_schemas:
            print(f"   - {schema['name']}: {schema['description']}")
        
        # Test MCP protocol handlers
        print("\n🔌 Testing MCP protocol...")
        
        # Test initialize
        init_params = {"clientInfo": {"name": "test-client", "version": "1.0.0"}}
        init_result = await server._handle_initialize(init_params)
        print(f"✅ Initialize: {init_result['protocolVersion']}")
        
        # Test tools/list
        tools_result = await server._handle_tools_list()
        print(f"✅ Tools list: {len(tools_result['tools'])} tools available")
        
        # Test formatters
        print("\n🎨 Testing formatters...")
        formatter = FlightFormatter()
        test_flight = {
            'name': 'Test Airlines',
            'price': '$299',
            'departure': '9:00 AM PST, Mon, Dec 25',
            'arrival': '12:00 PM EST, Mon, Dec 25', 
            'duration': '5 h 30 m',
            'stops': 0,
            'is_best': True
        }
        
        formatted = formatter.format_single_flight(test_flight, "JFK", "LAX")
        print("✅ Flight formatter working")
        
        # Test all tool collections
        print("\n🛠️ Testing tool collections...")
        from travvy_mcp.tools import TrainTools, AccommodationTools
        
        train_tools = TrainTools()
        accommodation_tools = AccommodationTools()
        
        print(f"✅ Train tools: {len(train_tools.get_all_tools())} tools")
        for tool in train_tools.get_all_tools():
            print(f"   - {tool.name}")
            
        print(f"✅ Accommodation tools: {len(accommodation_tools.get_all_tools())} tools")
        for tool in accommodation_tools.get_all_tools():
            print(f"   - {tool.name}")
        
        print("\n🎉 All tests passed! The modular server with ALL tools is working correctly.")
        
        # Print summary
        print(f"\n📊 Server Summary:")
        print(f"   - Server: {server.title} v{server.version}")
        print(f"   - Protocol: MCP {server.protocol_version}")
        print(f"   - Total Tools: {len(server.all_tools)}")
        print(f"   - Flight Tools: {len(flight_tools.get_all_tools())}")
        print(f"   - Weather Tools: {len(weather_tools.get_all_tools())}")
        print(f"   - Train Tools: {len(train_tools.get_all_tools())}")
        print(f"   - Accommodation Tools: {len(accommodation_tools.get_all_tools())}")
        print(f"\n🏷️ All Tool Names:")
        for i, tool in enumerate(server.all_tools, 1):
            print(f"   {i:2d}. {tool.name} - {tool.description}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_server())
    exit(0 if success else 1)

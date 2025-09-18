#!/usr/bin/env python3
"""
Test script to verify all MCP servers can be imported and initialized without errors.
"""

import sys
import importlib
import traceback

def test_server_imports():
    """Test that all server modules can be imported successfully."""
    servers = [
        'weather_server',
        'maps_server', 
        'flights',
        'accomadation',
        'train_server'
    ]
    
    results = {}
    
    for server in servers:
        try:
            print(f"Testing {server}...")
            
            # Try to import the module
            module = importlib.import_module(server)
            
            # Check if it has the expected MCP server instance
            if hasattr(module, 'mcp'):
                print(f"✅ {server}: Import successful, MCP server found (mcp)")
                results[server] = "SUCCESS"
            elif hasattr(module, 'maps_server'):
                print(f"✅ {server}: Import successful, MCP server found (maps_server)")
                results[server] = "SUCCESS"
            elif hasattr(module, 'server'):
                print(f"✅ {server}: Import successful, MCP server found (server)")
                results[server] = "SUCCESS"
            else:
                print(f"⚠️  {server}: Import successful, but no MCP server instance found")
                results[server] = "PARTIAL"
                
        except ImportError as e:
            print(f"❌ {server}: Import failed - {e}")
            results[server] = f"IMPORT_ERROR: {e}"
        except Exception as e:
            print(f"❌ {server}: Unexpected error - {e}")
            results[server] = f"ERROR: {e}"
            traceback.print_exc()
    
    return results

def test_trains_module():
    """Test the trains module separately since it's imported by train_server."""
    try:
        print("\nTesting trains module...")
        import trains
        print("✅ trains: Import successful")
        return True
    except ImportError as e:
        print(f"❌ trains: Import failed - {e}")
        return False
    except Exception as e:
        print(f"❌ trains: Unexpected error - {e}")
        return False

def main():
    print("🧪 Testing MCP Servers Import Status\n")
    
    # Test trains module first
    trains_ok = test_trains_module()
    
    # Test server imports
    results = test_server_imports()
    
    # Summary
    print("\n" + "="*50)
    print("📊 SUMMARY")
    print("="*50)
    
    success_count = sum(1 for v in results.values() if v == "SUCCESS")
    total_count = len(results)
    
    print(f"Trains module: {'✅ OK' if trains_ok else '❌ FAILED'}")
    print(f"Server modules: {success_count}/{total_count} successful")
    
    for server, status in results.items():
        status_emoji = "✅" if status == "SUCCESS" else "⚠️" if status == "PARTIAL" else "❌"
        print(f"  {status_emoji} {server}: {status}")
    
    if success_count == total_count and trains_ok:
        print("\n🎉 All servers are ready to run!")
        return 0
    else:
        print(f"\n⚠️  {total_count - success_count} servers need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())

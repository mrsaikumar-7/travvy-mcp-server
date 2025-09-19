"""
Travvy MCP Server - Travel Assistant Model Context Protocol Implementation
"""

__version__ = "1.0.0"
__author__ = "Travvy Team"

# Import server only when needed to avoid dependency issues
def get_server():
    """Get the TravvyMCPServer class (imports dependencies only when needed)"""
    from .server import TravvyMCPServer
    return TravvyMCPServer

__all__ = ["get_server"]

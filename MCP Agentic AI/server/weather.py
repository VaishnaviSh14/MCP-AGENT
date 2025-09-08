from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP  

#initializing the MCP server
mcp=FastMCP("Weather")

#constants
NWS_API_Base = "https://api.weather.gov" #open api for weather data
USER_AGENT = "weather-app/1.0"  #specify the user agent

#make a request to the NWS API
async def make_nws_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/geo+json"
    
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Error making request: {e}")
            return None

def format_alert(feature: dict) -> str:
    props = feature["properties"]
    return f"""

        Event Name: {props.get("event", "Unknown")}
        Area Description: {props.get("areaDesc", "Unknown")}
        Severity: {props.get("severity", "Unknown")}
        Description: {props.get("description", "Unknown")}
        Instructions: {props.get("instruction", "Unknown")}
        """

@mcp.tool()
async def get_weather_alerts(state: str) -> str:
    """Get active weather alerts for a given state.

    Args:
        state (str): The two-letter state code (e.g., "CA", "NY")
    """

    url = f"{NWS_API_Base}/alerts/active/area/{state}"
    data = await make_nws_request(url)

    if not data or "features" not in data:
        return "No alerts found for the state."

    if not data["features"]:
        return "No active alerts found for the state."

    alerts = [format_alert(feature) for feature in data["features"]]
    return "\n\n".join(alerts)

@mcp.resource("config://app")
def get_app_config() -> str:
        """Static configuration data."""
        return "This is the application configuration."

        
        # Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
            """Get a personalized greeting"""
            return f"Hello, {name}!"
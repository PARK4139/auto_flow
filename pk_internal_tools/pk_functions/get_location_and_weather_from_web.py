# Orchestrator for weather-related functions

from pk_internal_tools.pk_functions.get_weather_from_naver import get_weather_from_naver
from pk_internal_tools.pk_functions.to_vilage_grid import to_vilage_grid
from pk_internal_tools.pk_functions.kma_get_ultra_now import kma_get_ultra_now
from pk_internal_tools.pk_functions.get_location_from_ip_api import get_location_from_ip_api
from pk_internal_tools.pk_functions.get_weather_from_openweathermap import get_weather_from_openweathermap
from pk_internal_tools.pk_functions.get_weather_from_kma import get_weather_from_kma
from pk_internal_tools.pk_functions.get_weather_from_nws import get_weather_from_nws
from pk_internal_tools.pk_functions.get_weather_from_open_meteo import get_weather_from_open_meteo
from pk_internal_tools.pk_functions.get_current_location_info import get_current_location_info
from pk_internal_tools.pk_functions.get_current_weather_info import get_current_weather_info
from pk_internal_tools.pk_functions.get_historical_weather_from_meteostat import get_historical_weather_from_meteostat

# Re-export main functions for convenience
def get_location_and_weather_from_web():
    location_info = get_current_location_info()
    if location_info:
        weather_info = get_current_weather_info(location_info=location_info)
        return location_info, weather_info
    return None, None

# Re-export main functions for convenience
__all__ = [
    "get_weather_from_naver",
    "to_vilage_grid",
    "kma_get_ultra_now",
    "get_location_from_ip_api",
    "get_weather_from_openweathermap",
    "get_weather_from_kma",
    "get_weather_from_nws",
    "get_weather_from_open_meteo",
    "get_current_location_info",
    "get_current_weather_info",
    "get_historical_weather_from_meteostat",
    "get_location_and_weather_from_web", # Add this line
]

# Module-level constants (defined once here)
from datetime import timedelta, timezone
KMA_SERVICE_KEY_ID = "KMA_SERVICE_KEY"
OPENWEATHER_API_KEY_ID = "OPENWEATHER_API"
KST = timezone(timedelta(hours=9))
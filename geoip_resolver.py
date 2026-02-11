"""
GeoIP Resolver Module
=====================
Resolves IP addresses to geographic locations (country, city, latitude, longitude).

Uses MaxMind's GeoLite2-City database when available.
For private/localhost IPs (common in development), provides realistic
simulated locations so the threat map always has data for demos.

Setup for real GeoIP resolution:
  1. Sign up at https://dev.maxmind.com/geoip/geolite2-free-geolocation-data
  2. Download GeoLite2-City.mmdb
  3. Place it in this directory (same folder as this file)
  4. pip install geoip2
"""

import hashlib
import ipaddress
import os

# =========================================================================
# TRY TO LOAD GEOIP2 (optional dependency)
# =========================================================================
try:
    import geoip2.database
    GEOIP2_AVAILABLE = True
except ImportError:
    GEOIP2_AVAILABLE = False
    print("[GeoIP] geoip2 not installed. Using simulated locations only.")
    print("[GeoIP] To enable real GeoIP: pip install geoip2")

# Path to the GeoLite2 database file (place it in the project root)
GEOIP_DB_PATH = os.path.join(os.path.dirname(__file__), "GeoLite2-City.mmdb")

# =========================================================================
# SIMULATED DEMO LOCATIONS
# =========================================================================
# Realistic attacker locations from around the world.
# Used when IPs are private/localhost (can't be resolved by GeoLite2).
# This ensures the threat map always looks impressive during faculty demos.

# Special mapping for localhost — set to YOUR actual location (India)
# This ensures when YOU connect locally, the map shows your real country
LOCALHOST_LOCATION = {"country": "India", "city": "Hyderabad", "latitude": 17.3850, "longitude": 78.4867}

DEMO_LOCATIONS = [
    {"country": "Russia",       "city": "Moscow",         "latitude": 55.7558,  "longitude": 37.6173},
    {"country": "China",        "city": "Beijing",        "latitude": 39.9042,  "longitude": 116.4074},
    {"country": "China",        "city": "Shanghai",       "latitude": 31.2304,  "longitude": 121.4737},
    {"country": "Brazil",       "city": "São Paulo",      "latitude": -23.5505, "longitude": -46.6333},
    {"country": "Nigeria",      "city": "Lagos",          "latitude": 6.5244,   "longitude": 3.3792},
    {"country": "India",        "city": "Mumbai",         "latitude": 19.0760,  "longitude": 72.8777},
    {"country": "Iran",         "city": "Tehran",         "latitude": 35.6892,  "longitude": 51.3890},
    {"country": "North Korea",  "city": "Pyongyang",      "latitude": 39.0392,  "longitude": 125.7625},
    {"country": "Vietnam",      "city": "Hanoi",          "latitude": 21.0285,  "longitude": 105.8542},
    {"country": "Indonesia",    "city": "Jakarta",        "latitude": -6.2088,  "longitude": 106.8456},
    {"country": "Ukraine",      "city": "Kyiv",           "latitude": 50.4501,  "longitude": 30.5234},
    {"country": "Romania",      "city": "Bucharest",      "latitude": 44.4268,  "longitude": 26.1025},
    {"country": "Turkey",       "city": "Istanbul",       "latitude": 41.0082,  "longitude": 28.9784},
    {"country": "South Africa", "city": "Johannesburg",   "latitude": -26.2041, "longitude": 28.0473},
    {"country": "Argentina",    "city": "Buenos Aires",   "latitude": -34.6037, "longitude": -58.3816},
    {"country": "Germany",      "city": "Berlin",         "latitude": 52.5200,  "longitude": 13.4050},
    {"country": "Netherlands",  "city": "Amsterdam",      "latitude": 52.3676,  "longitude": 4.9041},
    {"country": "Pakistan",     "city": "Karachi",        "latitude": 24.8607,  "longitude": 67.0011},
    {"country": "Bangladesh",   "city": "Dhaka",          "latitude": 23.8103,  "longitude": 90.4125},
    {"country": "Thailand",     "city": "Bangkok",        "latitude": 13.7563,  "longitude": 100.5018},
]


def is_private_ip(ip_str):
    """
    Check if an IP address is private, localhost, or otherwise non-routable.
    These IPs cannot be resolved by GeoLite2.

    Private ranges: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
    Localhost: 127.0.0.0/8
    Link-local: 169.254.0.0/16
    """
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip.is_private or ip.is_loopback or ip.is_link_local
    except ValueError:
        return True  # Invalid IPs treated as private


def get_demo_location(ip_str):
    """
    Get a deterministic simulated location for a private IP.

    Uses a hash of the IP so the same IP always maps to the same city.
    This makes the demo consistent — 127.0.0.1 always shows as the same location.
    """
    # Hash the IP to get a consistent index
    ip_hash = int(hashlib.md5(ip_str.encode()).hexdigest(), 16)
    index = ip_hash % len(DEMO_LOCATIONS)
    return DEMO_LOCATIONS[index].copy()


def resolve_ip(ip_str):
    """
    Resolve an IP address to geographic location.

    Returns dict with: country, city, latitude, longitude
    Falls back to demo data for private IPs or when GeoLite2 is unavailable.

    Args:
        ip_str (str): The IP address to resolve

    Returns:
        dict: { country, city, latitude, longitude }
    """
    # --- Localhost IPs → map to YOUR real location (India) ---
    try:
        ip_obj = ipaddress.ip_address(ip_str)
        if ip_obj.is_loopback:
            location = LOCALHOST_LOCATION.copy()
            location["source"] = "localhost"
            return location
    except ValueError:
        pass

    # --- Other private IPs → use demo data for global variety ---
    if is_private_ip(ip_str):
        location = get_demo_location(ip_str)
        location["source"] = "simulated"
        return location

    # --- Try GeoLite2 real resolution ---
    if GEOIP2_AVAILABLE and os.path.exists(GEOIP_DB_PATH):
        try:
            with geoip2.database.Reader(GEOIP_DB_PATH) as reader:
                response = reader.city(ip_str)
                return {
                    "country": response.country.name or "Unknown",
                    "city": response.city.name or "Unknown",
                    "latitude": response.location.latitude or 0.0,
                    "longitude": response.location.longitude or 0.0,
                    "source": "geoip2"
                }
        except Exception as e:
            print(f"[GeoIP] Error resolving {ip_str}: {e}")

    # --- Fallback: use demo data even for public IPs ---
    location = get_demo_location(ip_str)
    location["source"] = "simulated"
    return location


# =========================================================================
# QUICK TEST (run this file directly to verify it works)
# =========================================================================
if __name__ == "__main__":
    test_ips = ["127.0.0.1", "192.168.1.100", "1.2.3.4", "8.8.8.8", "203.0.113.50"]

    print("=" * 70)
    print("GeoIP Resolver Test")
    print("=" * 70)

    for ip in test_ips:
        result = resolve_ip(ip)
        private = "PRIVATE" if is_private_ip(ip) else "PUBLIC"
        print(f"\n  {ip} ({private})")
        print(f"    → {result['city']}, {result['country']}")
        print(f"    → Lat: {result['latitude']}, Lng: {result['longitude']}")
        print(f"    → Source: {result['source']}")

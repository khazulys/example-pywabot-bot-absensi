import re
import math
import json
import httpx
from fake_useragent import UserAgent

def load_config():
    with open("config/config.json", "r") as f:
        return json.load(f)

async def get_coordinate(url):
    ua = UserAgent()
    latlon_pattern = re.compile(r"@(-?\d+\.\d+),(-?\d+\.\d+)", re.IGNORECASE)

    async with httpx.AsyncClient(follow_redirects=True, timeout=30.0) as client:
        for _ in range(50):
            try:
                resp = await client.get(url, headers={"User-Agent": ua.chrome})
                resp.raise_for_status()
                match = latlon_pattern.search(resp.text)
                if match:
                    lat, lon = match.groups()
                    return float(lat), float(lon)
            except httpx.RequestError:
                continue
    return None, None

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

# scripts/utils.py
import time
from math import radians, sin, cos, sqrt, atan2
# from geopy.geocoders import Nominatim # Would be used in a real implementation
# from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

# --- Placeholder for Geocoding Logic ---
def geocode_address(address_str: str, cep: str = None):
    """
    Conceptual function to geocode an address string or CEP.
    In a real implementation, this would use a service like Nominatim via geopy.
    Requires proper error handling, API keys (for some services), and adherence to usage policies.

    :param address_str: Full address string (e.g., "Rua Exemplo, 123, Cidade, Estado")
    :param cep: Postal code (e.g., "01000-000")
    :return: A dict {'latitude': float, 'longitude': float} or None if geocoding fails.
    """
    print(f"[INFO] Conceptual geocoding for: {address_str} (CEP: {cep})")
    
    # In a real scenario:
    # user_agent = "HetaProject/1.0 (https://github.com/user/repo)" # Replace with actual repo/contact
    # geolocator = Nominatim(user_agent=user_agent)
    # try:
    #   location = geolocator.geocode(f"{address_str}, {cep}", timeout=10)
    #   time.sleep(1) # Adhere to usage policy (e.g., 1 req/sec for Nominatim)
    #   if location:
    #     return {"latitude": location.latitude, "longitude": location.longitude}
    #   else:
    #     print(f"[WARN] Geocoding failed for: {address_str}")
    #     return None
    # except GeocoderTimedOut:
    #   print(f"[ERROR] Geocoding service timed out for: {address_str}")
    #   return None
    # except GeocoderUnavailable:
    #   print(f"[ERROR] Geocoding service unavailable for: {address_str}")
    #   return None
    # except Exception as e:
    #   print(f"[ERROR] An unexpected error occurred during geocoding: {e}")
    #   return None

    # --- Placeholder Data based on sample _data/entidades.json ---
    # This is purely for allowing other scripts to run without live API calls.
    # A real implementation MUST use a geocoding service.
    if "Rua da Mooca, 1000" in address_str or "03001-000" == cep:
        return {"latitude": -23.5563, "longitude": -46.6082}
    elif "Av. Rio Branco, 100" in address_str or "20040-004" == cep:
        return {"latitude": -22.9035, "longitude": -43.1764}
    elif "Av. Afonso Pena, 500" in address_str or "30110-000" == cep:
        return {"latitude": -19.9191, "longitude": -43.9386}
    # --- Placeholder for school location from a hypothetical escolas.json ---
    elif "Escola Modelo 1" in address_str: # Assuming school name is part of address_str for this mock
        return {"latitude": -23.5500, "longitude": -46.6300} # São Paulo (example)
    elif "Escola Modelo 2" in address_str:
        return {"latitude": -22.9000, "longitude": -43.1700} # Rio de Janeiro (example)

    print(f"[WARN] No placeholder geocoding match for: {address_str} (CEP: {cep}). Returning None.")
    return None


# --- Haversine Formula for Distance Calculation ---
def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    R = 6371  # Radius of the earth in km

    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

if __name__ == '__main__':
    # Example Usage (Conceptual)
    addr = "Av. Paulista, 1578, Bela Vista, São Paulo, SP"
    postal_code = "01310-200"
    coords = geocode_address(addr, postal_code)
    if coords:
        print(f"Coordinates for {addr}: {coords['latitude']}, {coords['longitude']}")
    else:
        print(f"Could not geocode {addr}")

    # Example distance calculation
    # São Paulo to Rio (example coordinates)
    sp_lat, sp_lon = -23.5505, -46.6333
    rj_lat, rj_lon = -22.9068, -43.1729
    dist = calculate_distance(sp_lat, sp_lon, rj_lat, rj_lon)
    print(f"Distance between SP and RJ: {dist:.2f} km")
    
    # Test with placeholder data from the geocode_address function
    entidade1_coords = geocode_address("Rua da Mooca, 1000", "03001-000")
    escola1_coords = geocode_address("Escola Modelo 1", "") # School name as address for mock
    if entidade1_coords and escola1_coords:
        dist_test = calculate_distance(entidade1_coords['latitude'], entidade1_coords['longitude'],
                                       escola1_coords['latitude'], escola1_coords['longitude'])
        print(f"Distance between Entidade Mooca and Escola Modelo 1: {dist_test:.2f} km")

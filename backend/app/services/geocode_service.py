from opencage.geocoder import OpenCageGeocode
import os

def get_location(address):
    api_key = os.getenv("OPENCAGE_API_KEY")
    if not api_key:
        print("No OpenCage API key found.")
        return {"latitude": None, "longitude": None}
    geocoder = OpenCageGeocode(api_key)
    try:
        result = geocoder.geocode(address)
        if result:
            return {
                "latitude": result[0]['geometry']['lat'],
                "longitude": result[0]['geometry']['lng']
            }
        return {"latitude": None, "longitude": None}
    except Exception as e:
        print("Geocoding error:", e)
        return {"latitude": None, "longitude": None}

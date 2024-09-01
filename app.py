import streamlit as st
import requests
from geopy.geocoders import Nominatim

# Title for the app
st.title("User's Geolocation")

# Function to get location from coordinates
def get_location_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="MyGeoApp/1.0")
    try:
        location_data = geolocator.reverse(f"{lat}, {lon}", language="en")
        if location_data:
            return location_data.raw['display_name']
        else:
            return "Location not found"
    except Exception as e:
        st.error(f"Nominatim Error: {str(e)}")
        return f"Error: {str(e)}"

# Alternative function using OpenStreetMap API directly
def get_location_from_osm(lat, lon):
    url = f"https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={lat}&lon={lon}"
    try:
        response = requests.get(url)
        data = response.json()
        if 'display_name' in data:
            return data['display_name']
        else:
            return "Address not found in OSM response"
    except Exception as e:
        st.error(f"OSM API Error: {str(e)}")
        return f"Error: {str(e)}"

# JavaScript to get the user's location and update URL
get_location_script = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        document.getElementById("location").innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    document.getElementById("location").innerHTML = `Latitude: ${lat}, Longitude: ${lon}`;
    
    // Update the URL with latitude and longitude
    const url = new URL(window.location.href);
    url.searchParams.set('lat', lat);
    url.searchParams.set('lon', lon);
    window.history.replaceState({}, '', url);
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("location").innerHTML = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("location").innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById("location").innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("location").innerHTML = "An unknown error occurred.";
            break;
    }
}
</script>
<button onclick="getLocation()">Get Location</button>
<p id="location"></p>
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

# Retrieve latitude and longitude from query parameters
query_params = st.experimental_get_query_params()
lat = query_params.get("lat", [None])[0]
lon = query_params.get("lon", [None])[0]

if lat and lon:
    lat = float(lat)
    lon = float(lon)
    st.write(f"**Latitude:** {lat}")
    st.write(f"**Longitude:** {lon}")
    
    address_nominatim = get_location_from_coordinates(lat, lon)
    address_osm = get_location_from_osm(lat, lon)
    st.write(f"**Address (Nominatim):** {address_nominatim}")
    st.write(f"**Address (OSM API):** {address_osm}")
else:
    st.write("Waiting for location...")

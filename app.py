import streamlit as st
import time
from geopy.geocoders import Nominatim
import requests

# Title for the app
st.title("User's Geolocation")

# Function to get location from coordinates
def get_location_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="MyGeoApp/1.0")
    try:
        location_data = geolocator.reverse(f"{lat}, {lon}", language="en")
        if location_data:
            st.write("Raw location data:", location_data.raw)
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
        st.write("OSM API response:", data)
        if 'display_name' in data:
            return data['display_name']
        else:
            return "Address not found in OSM response"
    except Exception as e:
        st.error(f"OSM API Error: {str(e)}")
        return f"Error: {str(e)}"

# Step 1: Ask the user to enable location services
st.write("Please enable location services in your browser.")

# Step 2: HTML and JavaScript to get the user's location
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
    // Send the coordinates to Streamlit
    fetch(`/get_address?lat=${lat}&lon=${lon}`)
        .then(response => response.text())
        .then(data => {
            document.getElementById("address").innerHTML = `Address: ${data}`;
        });
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
<p id="address"></p>
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

# Step 3: Handle the request to get the address
def get_address():
    lat = st.experimental_get_query_params().get("lat", [None])[0]
    lon = st.experimental_get_query_params().get("lon", [None])[0]
    if lat and lon:
        st.write(f"Received coordinates: Lat {lat}, Lon {lon}")
        address_nominatim = get_location_from_coordinates(float(lat), float(lon))
        address_osm = get_location_from_osm(float(lat), float(lon))
        return f"Nominatim: {address_nominatim}\nOSM API: {address_osm}"
    return "Coordinates not provided"

# Use Streamlit's server-side code to handle the request
if 'lat' in st.experimental_get_query_params() and 'lon' in st.experimental_get_query_params():
    address = get_address()
    st.write(f"Address: {address}")

# Add a delay before making the next request
time.sleep(1)

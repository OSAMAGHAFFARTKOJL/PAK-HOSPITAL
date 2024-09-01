import streamlit as st
import time
from geopy.geocoders import Nominatim

# Title for the app
st.title("User's Geolocation")

# Function to get location from coordinates
def get_location_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="MyGeoApp/1.0")
    location_data = geolocator.reverse(f"{lat}, {lon}")
    if location_data:
        return location_data.address
    else:
        return "Location not found"

# Step 1: Ask the user to enable location services
st.write("Please enable location services in your browser.")

# Step 2: HTML and JavaScript to get the user's location
get_location_script = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition);
    } else {
        alert("Geolocation is not supported by this browser.");
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
        address = get_location_from_coordinates(float(lat), float(lon))
        return address
    return "Coordinates not provided"

# Use Streamlit's server-side code to handle the request
address = get_address()
if address != "Coordinates not provided":
    st.write(f"Address: {address}")

# Add a delay before making the next request
time.sleep(1)

import streamlit as st
from geopy.geocoders import Nominatim
import json

# Function to get location from latitude and longitude
def get_location_from_coordinates(lat, lon):
    geolocator = Nominatim(user_agent="MyGeoApp/1.0")
    location_data = geolocator.reverse(f"{lat}, {lon}")
    if location_data:
        return location_data.address
    else:
        return "Location not found"

# Title for the app
st.title("User's Geolocation")

# Step 1: Ask the user to enable location services
st.write("Please enable location services in your browser.")

# JavaScript to get the user's location and send it to the Streamlit app
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
        
        // Send the location to Streamlit
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/update_location", true);
        xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        xhr.send(JSON.stringify({latitude: lat, longitude: lon}));
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <p id="location"></p>
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

# Handle the data sent from JavaScript
if st.experimental_get_query_params().get("latitude") and st.experimental_get_query_params().get("longitude"):
    latitude = float(st.experimental_get_query_params().get("latitude")[0])
    longitude = float(st.experimental_get_query_params().get("longitude")[0])
    
    address = get_location_from_coordinates(latitude, longitude)
    st.write(f"**Latitude:** {latitude}")
    st.write(f"**Longitude:** {longitude}")
    st.write(f"**Address:** {address}")
else:
    st.write("Waiting for location...")

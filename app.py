import streamlit as st
import time
from geopy.geocoders import Nominatim

# Title for the app
st.title("User's Geolocation")

# Step 1: Ask the user to enable location services
st.write("Please enable location services in your browser.")

# Step 2: HTML and JavaScript to get the user's location after they enable it
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
        document.getElementById("location_input").value = `${lat}, ${lon}`;
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <p id="location"></p>
    <input type="hidden" id="location_input" />
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

# Step 3: Get the location from the hidden input field
location_input = st.text_input("Location", key="location_input")

# Step 4: Reverse geocode the location
if location_input:
    lat, lon = location_input.split(", ")
    def get_location_from_coordinates(lat, lon):
        # Create a geolocator object
        geolocator = Nominatim(user_agent="MyGeoApp/1.0")
        
        # Perform reverse geocoding
        location_data = geolocator.reverse(f"{lat}, {lon}")
        
        if location_data:
            return location_data.address
        else:
            return "Location not found"

    address = get_location_from_coordinates(lat, lon)
    st.write(f"**Address:** {address}")
else:
    st.write("Waiting for location...")

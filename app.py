import streamlit as st

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
        document.getElementById("lat").value = lat;
        document.getElementById("lon").value = lon;
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <p id="location"></p>
    <input type="hidden" id="lat" />
    <input type="hidden" id="lon" />
"""

# Display the HTML/JS code in the Streamlit app
result = st.components.v1.html(get_location_script, height=200)

# Step 3: Get the location from the hidden input fields
lat = result[0].script_result.getElementById("lat").value
lon = result[0].script_result.getElementById("lon").value

# Display the latitude and longitude
st.write(f"**Latitudesss:** {lat}")
st.write(f"**Longitude:** {lon}")

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
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <p id="location"></p>
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

import streamlit as st

# Title for the app
st.title("User's Geolocation")

# Step 1: Ask the user to enable location services
st.write("Please enable location services in your browser.")

# JavaScript to get the user's location and send it to Streamlit
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
        
        // Update Streamlit with location data
        const inputField = document.getElementById("location_input");
        inputField.value = `${lat},${lon}`;
        inputField.dispatchEvent(new Event('input', { bubbles: true }));
        
        // Save the coordinates in session storage to retrieve it in Python
        sessionStorage.setItem('lat', lat);
        sessionStorage.setItem('lon', lon);
    }
    
    window.onload = function() {
        const lat = sessionStorage.getItem('lat');
        const lon = sessionStorage.getItem('lon');
        if (lat && lon) {
            document.getElementById("location").innerHTML = `Latitude: ${lat}, Longitude: ${lon}`;
            document.getElementById("location_input").value = `${lat},${lon}`;
            document.getElementById("location_input").dispatchEvent(new Event('input', { bubbles: true }));
        }
    };
    </script>
    <button onclick="getLocation()">Get Location</button>
    <p id="location"></p>
    <input type="hidden" id="location_input" />
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

# Retrieve the location from the hidden input field
if 'lat_lon' in st.session_state:
    lat, lon = st.session_state.lat_lon.split(",")
    st.write(f"**Latitudessss:** {lat.strip()}")
    st.write(f"**Longitude:** {lon.strip()}")
else:
    st.write("Waiting for location...")

# Save the location to session state
def update_location(location):
    st.session_state.lat_lon = location

# Call the function to update location
if st.session_state.get('lat_lon'):
    update_location(st.session_state.lat_lon)

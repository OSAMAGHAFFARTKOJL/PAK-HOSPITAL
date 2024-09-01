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
        document.getElementById("location_input").value = lat + "," + lon;
        document.getElementById("location_input").dispatchEvent(new Event("input"));
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <input type="hidden" id="location_input" />
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script)

# Step 3: Retrieve the location from the hidden input field
location = st.text_input("Location", key="location_input")

# Step 4: Display the location if it was retrieved
if location:
    lat, lon = location.split(",")
    st.write(f"**Latitude:** {lat.strip()}")
    st.write(f"**Longitude:** {lon.strip()}")
else:
    st.write("Waiting for location...")


import streamlit as st

# Title for the app
st.title("Get User's Geolocation")

# HTML and JavaScript code to get user's geolocation
location_html = """
    <script>
    function getLocation() {
        navigator.geolocation.getCurrentPosition(showPosition);
    }
    function showPosition(position) {
        const lat = position.coords.latitude;
        const lon = position.coords.longitude;
        document.getElementById("location_input").value = lat + "," + lon;
        document.getElementById("location_input").dispatchEvent(new Event("input"));
    }
    getLocation();
    </script>
    <input type="hidden" id="location_input" />
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(location_html)

# Retrieve the location from the hidden input field
location = st.text_input("Location", key="location_input")

# Display the location if it was retrieved
if location:
    lat, lon = location.split(",")
    st.write(f"**Latitude:** {lat.strip()}")
    st.write(f"**Longitude:** {lon.strip()}")
else:
    st.write("Waiting for location...")

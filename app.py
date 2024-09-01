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
        window.parent.postMessage({ lat: lat, lon: lon }, "*");
    }
    </script>
    <button onclick="getLocation()">Get Location</button>
    <p id="location"></p>
"""

# Display the HTML/JS code in the Streamlit app
st.components.v1.html(get_location_script, height=200)

# Step 3: Get the location from the JavaScript post message
if "lat" not in st.session_state:
    st.session_state.lat = None
    st.session_state.lon = None

if st.session_state.lat is None:
    st.write("Waiting for location...")
else:
    st.write(f"**Latitude:** {st.session_state.lat}")
    st.write(f"**Longitude:** {st.session_state.lon}")

# Handle the JavaScript post message
if "message" in st.experimental_get_query_params():
    lat = st.experimental_get_query_params()["message"][0]["lat"]
    lon = st.experimental_get_query_params()["message"][0]["lon"]
    st.session_state.lat = lat
    st.session_state.lon = lon

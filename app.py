import streamlit as st

# Title for the app
st.title("Get User's Geolocation")

# Placeholder for JavaScript injection and output display
location_placeholder = st.empty()

# JavaScript to get user's location and pass it to a hidden Streamlit text input
st.markdown("""
    <script>
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            const locationInput = document.getElementById("location_input");
            locationInput.value = `${latitude}, ${longitude}`;
            locationInput.dispatchEvent(new Event('change'));
        });
    </script>
    <input type="hidden" id="location_input" name="location_input" />
""", unsafe_allow_html=True)

# Text input to capture the location from JavaScript
location = st.text_input("Location", key="location_input")

# Display the location if it was retrieved
if location:
    lat, lon = location.split(", ")
    st.write(f"**Latitude:** {lat}")
    st.write(f"**Longitude:** {lon}")
else:
    st.write("Waiting for location...")


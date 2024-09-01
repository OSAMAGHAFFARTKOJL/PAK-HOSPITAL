import streamlit as st

# Streamlit app title
st.title("Get Your Current Location")

# Add a button that triggers the JavaScript to get the geolocation


if st.button("Get Location"):
    # Use Streamlit to run JavaScript and get the user's geolocation
    st.write(
        """
        <script>
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                document.getElementById('latitude').value = latitude;
                document.getElementById('longitude').value = longitude;
                document.getElementById('location-form').submit();
            },
            (error) => {
                console.error('Error Code = ' + error.code + ' - ' + error.message);
                document.getElementById('error-msg').textContent = 'Error: Unable to get location. Please allow location access in your browser.';
            }
        );
        </script>
        <form id="location-form" method="post">
            <input type="hidden" id="latitude" name="latitude">
            <input type="hidden" id="longitude" name="longitude">
        </form>
        <p id="error-msg" style="color: red;"></p>
        """,
        unsafe_allow_html=True,
    )

    # Handle the received data
    if "latitude" in st.experimental_get_query_params():
        latitude = float(st.experimental_get_query_params()["latitude"][0])
        longitude = float(st.experimental_get_query_params()["longitude"][0])

        # Display the retrieved location
        st.success("Location retrieved successfully!")
        st.write(f"**Latitude:** {latitude}")
        st.write(f"**Longitude:** {longitude}")

        # You can also use a geocoding service to get the city, state, and country from the coordinates.
        # Example using geopy library (optional):
        # from geopy.geocoders import Nominatim
        # geolocator = Nominatim(user_agent="geoapiExercises")
        # location = geolocator.reverse(f"{latitude}, {longitude}")
        # st.write(f"**Address:** {location.address}")

    else:
        st.warning("Click the button to get your location.")

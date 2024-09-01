import streamlit as st
import geocoder

# Set up the Streamlit app title
st.title("Get Your Current Location")

# Button to fetch the location
if st.button("Get Location"):
    # Get the current location of the user based on IP address
    location = geocoder.ip('me')
    
    # Check if the location retrieval was successful
    if location.ok:
        st.success("Location retrieved successfully!")
        st.write(f"**Latitude:** {location.latlng[0]}")
        st.write(f"**Longitude:** {location.latlng[1]}")
        st.write(f"**City:** {location.city}")
        st.write(f"**State:** {location.state}")
        st.write(f"**Country:** {location.country}")
    else:
        st.error("Unable to determine the location.")

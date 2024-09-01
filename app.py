import streamlit as st
import requests

# Function to get user's location based on IP
def get_user_location():
    response = requests.get('http://ip-api.com/json')
    data = response.json()
    return data['lat'], data['lon'], data['city'], data['region'], data['country']

# Streamlit app title
st.title("Find Your Location")

# Button to fetch the location
if st.button("Get Location"):
    location = get_user_location()
    
    if location:
        st.success("Location retrieved successfully!")
        st.write(f"**Latitude:** {location[0]}")
        st.write(f"**Longitude:** {location[1]}")
        st.write(f"**City:** {location[2]}")
        st.write(f"**Region:** {location[3]}")
        st.write(f"**Country:** {location[4]}")
    else:
        st.error("Unable to retrieve location.")



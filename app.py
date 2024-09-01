import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable

def get_location_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_streamlit_map_application")
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except (GeocoderTimedOut, GeocoderUnavailable):
        st.error("Error: The geocoding service is unavailable. Please try again later.")
        return None

def create_map(latitude, longitude, zoom=12):
    m = folium.Map(location=[latitude, longitude], zoom_start=zoom)
    folium.Marker([latitude, longitude]).add_to(m)
    return m

def main():
    st.title("Location Map Viewer")
    
    location_name = st.text_input("Enter a location (e.g., 'New York City' or 'Eiffel Tower, Paris'): ")
    
    if st.button("Show Map"):
        if location_name:
            coordinates = get_location_coordinates(location_name)
            if coordinates:
                latitude, longitude = coordinates
                st.success(f"Coordinates: {latitude}, {longitude}")
                
                map = create_map(latitude, longitude)
                folium_static(map)
            else:
                st.warning("Location not found. Please try a different location.")
        else:
            st.warning("Please enter a location.")

if __name__ == "__main__":
    main()

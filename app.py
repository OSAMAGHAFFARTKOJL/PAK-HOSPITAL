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

def create_map_with_route(start_lat, start_lon, end_lat, end_lon, zoom=12):
    # Create a folium map centered at the midpoint
    m = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=zoom)
    
    # Add markers for the start and end points
    folium.Marker([start_lat, start_lon], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([end_lat, end_lon], popup="End", icon=folium.Icon(color='red')).add_to(m)
    
    # Add a path between the start and end points
    folium.PolyLine(locations=[[start_lat, start_lon], [end_lat, end_lon]], color='blue').add_to(m)
    
    return m

def main():
    st.title("Path Between Locations")

    start_location_name = st.text_input("Enter the start location:")
    end_location_name = st.text_input("Enter the end location:")
    
    if st.button("Show Path"):
        if start_location_name and end_location_name:
            start_coordinates = get_location_coordinates(start_location_name)
            end_coordinates = get_location_coordinates(end_location_name)
            
            if start_coordinates and end_coordinates:
                start_lat, start_lon = start_coordinates
                end_lat, end_lon = end_coordinates
                
                st.success(f"Start Coordinates: {start_lat}, {start_lon}")
                st.success(f"End Coordinates: {end_lat}, {end_lon}")
                
                map = create_map_with_route(start_lat, start_lon, end_lat, end_lon)
                folium_static(map)
            else:
                st.warning("One or both locations not found. Please try different locations.")
        else:
            st.warning("Please enter both start and end locations.")

if __name__ == "__main__":
    main()

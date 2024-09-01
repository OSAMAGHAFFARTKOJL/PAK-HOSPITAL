import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
from openrouteservice import Client
import polyline

def get_location_coordinates(location_name):
    geolocator = Nominatim(user_agent="my_streamlit_map_application")
    try:
        location = geolocator.geocode(location_name)
        if location:
            return location.latitude, location.longitude
        else:
            return None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

def create_map_with_route(start_lat, start_lon, end_lat, end_lon, api_key):
    client = Client(key=api_key)
    
    # Get the route
    try:
        route = client.directions(
            coordinates=[[start_lon, start_lat], [end_lon, end_lat]],
            profile='driving-car',
            format='geojson'
        )
    except Exception as e:
        st.error(f"Error fetching route: {str(e)}")
        return None
    
    # Create map centered around the route
    m = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=12)
    
    # Add markers for start and end
    folium.Marker([start_lat, start_lon], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([end_lat, end_lon], popup="End", icon=folium.Icon(color='red')).add_to(m)
    
    # Add the route to the map
    try:
        route_coordinates = route['features'][0]['geometry']['coordinates']
        decoded_coordinates = polyline.decode(route_coordinates)
        folium.PolyLine(locations=decoded_coordinates, color='blue').add_to(m)
    except Exception as e:
        st.error(f"Error decoding polyline: {str(e)}")
    
    return m

def main():
    st.title("Route Path Between Locations")

    # OpenRouteService API Key
    api_key = st.text_input("Enter your OpenRouteService API Key:", type="password")

    start_location_name = st.text_input("Enter the start location:")
    end_location_name = st.text_input("Enter the end location:")
    
    if st.button("Show Route"):
        if start_location_name and end_location_name:
            start_coordinates = get_location_coordinates(start_location_name)
            end_coordinates = get_location_coordinates(end_location_name)
            
            if start_coordinates and end_coordinates:
                start_lat, start_lon = start_coordinates
                end_lat, end_lon = end_coordinates
                
                if api_key:
                    st.success(f"Start Coordinates: {start_lat}, {start_lon}")
                    st.success(f"End Coordinates: {end_lat}, {end_lon}")
                    
                    map = create_map_with_route(start_lat, start_lon, end_lat, end_lon, api_key)
                    if map:
                        folium_static(map)
                else:
                    st.warning("Please enter your OpenRouteService API Key.")
            else:
                st.warning("One or both locations not found. Please try different locations.")
        else:
            st.warning("Please enter both start and end locations.")

if __name__ == "__main__":
    main()

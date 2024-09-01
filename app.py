import streamlit as st
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import requests
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

def get_route(start_lon, start_lat, end_lon, end_lat):
    url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=polyline"
    response = requests.get(url)
    if response.status_code == 200:
        route_data = response.json()
        if route_data["code"] == "Ok":
            return route_data["routes"][0]["geometry"]
    return None

def create_map_with_route(start_lat, start_lon, end_lat, end_lon):
    # Create map centered around the route
    m = folium.Map(location=[(start_lat + end_lat) / 2, (start_lon + end_lon) / 2], zoom_start=10)
    
    # Add markers for start and end
    folium.Marker([start_lat, start_lon], popup="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker([end_lat, end_lon], popup="End", icon=folium.Icon(color='red')).add_to(m)
    
    # Get the route
    route_polyline = get_route(start_lon, start_lat, end_lon, end_lat)
    
    if route_polyline:
        # Decode the polyline
        route_coords = polyline.decode(route_polyline)
        
        # Add the route to the map
        folium.PolyLine(locations=route_coords, color='blue', weight=5, opacity=0.8).add_to(m)
        
        # Fit the map to the route
        southwest = min(route_coords, key=lambda coord: (coord[0], coord[1]))
        northeast = max(route_coords, key=lambda coord: (coord[0], coord[1]))
        m.fit_bounds([southwest, northeast])
    else:
        st.warning("Unable to find a route between the given locations.")
    
    return m

def main():
    st.title("Route Path Between Locations")
    
    start_location_name = st.text_input("Enter the start location:")
    end_location_name = st.text_input("Enter the end location:")
    
    if st.button("Show Route"):
        if start_location_name and end_location_name:
            start_coordinates = get_location_coordinates(start_location_name)
            end_coordinates = get_location_coordinates(end_location_name)
            
            if start_coordinates and end_coordinates:
                start_lat, start_lon = start_coordinates
                end_lat, end_lon = end_coordinates
                
                st.success(f"Start Coordinates: {start_lat}, {start_lon}")
                st.success(f"End Coordinates: {end_lat}, {end_lon}")
                
                map = create_map_with_route(start_lat, start_lon, end_lat, end_lon)
                if map:
                    folium_static(map)
            else:
                st.warning("One or both locations not found. Please try different locations.")
        else:
            st.warning("Please enter both start and end locations.")

if __name__ == "__main__":
    main()

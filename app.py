import streamlit as st

st.set_page_config(page_title="GPS Location App")

st.title("GPS Location App")

st.write("Click the button below to get your GPS location.")

# JavaScript to get user's location
location_button = st.button("Get My Location")

# HTML and JavaScript for getting location
location_html = """
<div id="location-data"></div>

<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        document.getElementById("location-data").innerHTML = "Geolocation is not supported by this browser.";
    }
}

function showPosition(position) {
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    document.getElementById("location-data").innerHTML = "Latitude: " + lat + "<br>Longitude: " + lon;
    
    // Send data to Streamlit
    fetch(`http://localhost:8501/?lat=${lat}&lon=${lon}`)
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            document.getElementById("location-data").innerHTML = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            document.getElementById("location-data").innerHTML = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            document.getElementById("location-data").innerHTML = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            document.getElementById("location-data").innerHTML = "An unknown error occurred.";
            break;
    }
}

if (%(pressed)s) {
    getLocation();
}
</script>
""" % {"pressed": str(location_button).lower()}

st.components.v1.html(location_html, height=100)

# Display the location data
lat = st.experimental_get_query_params().get("lat", [None])[0]
lon = st.experimental_get_query_params().get("lon", [None])[0]

if lat and lon:
    st.write(f"Your location: Latitude {lat}, Longitude {lon}")

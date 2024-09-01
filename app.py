import streamlit as st
from streamlit_js_eval import streamlit_js_eval, JsCode

# Title for the app
st.title("Get User's Geolocation")

# JavaScript code to get user's location
js_code = JsCode("""
    navigator.geolocation.getCurrentPosition(
        (position) => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            streamlit.setComponentValue(`${latitude},${longitude}`);
        }
    );
""")

# Run the JavaScript and get the result
location = streamlit_js_eval(js_code, key="get_location")

# Display the location if it was retrieved
if location:
    lat, lon = location.split(",")
    st.write(f"**Latitude:** {lat.strip()}")
    st.write(f"**Longitude:** {lon.strip()}")
else:
    st.write("Waiting for location...")


import streamlit as st

st.markdown("""
    <script>
        navigator.geolocation.getCurrentPosition(position => {
            const latitude = position.coords.latitude;
            const longitude = position.coords.longitude;
            document.querySelector("input").value = `${latitude}, ${longitude}`;
        });
    </script>
    <input id="location" type="text" />
""", unsafe_allow_html=True)

location = st.session_state.location
st.write(f"User location: {location}")


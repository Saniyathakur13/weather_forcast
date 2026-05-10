import streamlit as st
import requests
from datetime import datetime

# Page Setup
st.set_page_config(page_title="Weather App", page_icon="🌦️")

# Simple Pink Styling to match your theme
st.markdown("""
    <style>
    .stApp { background-color: #F994DC; }
    .stButton>button { background-color: #FF69B4; color: white; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌡️ Weather Forecast")

# API Setup
api_key = "79a6d79722323f1c1988fde75011c51b"
base_url = "http://openweathermap.org?"

# UI Components
city = st.text_input("Enter City Name", placeholder="e.g. Mumbai")
units = st.radio("Choose Units", ["Celsius", "Fahrenheit"], horizontal=True)

unit_code = "metric" if units == "Celsius" else "imperial"
unit_sym = "°C" if units == "Celsius" else "°F"

if st.button("Get Weather"):
    if city:
        query = f"{base_url}q={city}&appid={api_key}&units={unit_code}"
        try:
            response = requests.get(query)
            data = response.json()

            if data["cod"] == 200:
                st.success(f"Weather for {data['name']}, {data['sys']['country']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature", f"{data['main']['temp']}{unit_sym}")
                    st.write(f"**Condition:** {data['weather'][0]['description'].title()}")
                with col2:
                    st.write(f"**Humidity:** {data['main']['humidity']}%")
                    st.write(f"**Wind:** {data['wind']['speed']} {'m/s' if units == 'Celsius' else 'mph'}")
                
                st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                st.error(f"Error: {data['message']}")
        except:
            st.error("Could not connect to the weather service.")
    else:
        st.warning("Please enter a city name.")

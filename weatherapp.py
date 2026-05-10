import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Weather Forecast App", page_icon="🌤️")

# Custom CSS for that pink vibe you had
st.markdown("""
    <style>
    .stApp { background-color: #F994DC; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌡️ Weather Forecast App")

# API Setup
api_key = "79a6d79722323f1c1988fde75011c51b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"

# Input UI
col1, col2 = st.columns(2)
with col1:
    city = st.text_input("City", placeholder="e.g. London")
with col2:
    country = st.text_input("Country Code (Optional)", placeholder="e.g. UK")

units = st.radio("Units", ["Celsius", "Fahrenheit"], horizontal=True)
unit_code = "metric" if units == "Celsius" else "imperial"

if st.button("Get Weather"):
    if not city:
        st.error("Please enter a city name")
    else:
        query = f"{base_url}q={city}"
        if country:
            query += f",{country}"
        query += f"&appid={api_key}&units={unit_code}"
        
        try:
            response = requests.get(query)
            data = response.json()
            
            if data["cod"] != 200:
                st.error(f"Error: {data['message']}")
            else:
                # Display Results
                st.subheader(f"{data['name']}, {data['sys']['country']}")
                temp_symbol = "°C" if unit_code == "metric" else "°F"
                
                st.metric("Temperature", f"{data['main']['temp']}{temp_symbol}")
                st.write(f"**Condition:** {data['weather'][0]['description'].title()}")
                st.write(f"**Humidity:** {data['main']['humidity']}%")
                st.write(f"**Wind Speed:** {data['wind']['speed']} {'m/s' if unit_code == 'metric' else 'mph'}")
                
                st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
        except Exception as e:
            st.error("Connection Error. Please try again later.")

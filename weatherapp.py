import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="Weather App", page_icon="🌦️")

# Styling
st.markdown("""
    <style>
    .stApp { background-color: #F994DC; }
    .stButton>button { background-color: #FF69B4; color: white; width: 100%; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌡️ Weather Forecast")

api_key = "79a6d79722323f1c1988fde75011c51b"
base_url = "http://openweathermap.org?"

city = st.text_input("Enter City Name", placeholder="e.g. Atpadi")
units = st.radio("Choose Units", ["Celsius", "Fahrenheit"], horizontal=True)

unit_code = "metric" if units == "Celsius" else "imperial"
unit_sym = "°C" if units == "Celsius" else "°F"

if st.button("Get Weather"):
    if city:
        # Correctly formatted URL
        query = f"{base_url}q={city}&appid={api_key}&units={unit_code}"
        
        try:
            response = requests.get(query)
            data = response.json()

            if data["cod"] == 200:
                st.success(f"Weather for {data['name']}, {data['sys']['country']}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Temperature", f"{data['main']['temp']}{unit_sym}")
                    # FIXED: weather is a list, so we need index [0]
                    desc = data['weather'][0]['description'].title()
                    st.write(f"**Condition:** {desc}")
                with col2:
                    st.write(f"**Humidity:** {data['main']['humidity']}%")
                    wind_speed = data['wind']['speed']
                    st.write(f"**Wind:** {wind_speed} {'m/s' if units == 'Celsius' else 'mph'}")
                
                st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                # This will tell you if the City is wrong or API key is dead
                st.error(f"API Error: {data.get('message', 'Unknown Error')}")
        except Exception as e:
            st.error(f"Connection Error: {e}")
    else:
        st.warning("Please enter a city name.")

import tkinter as tk
from tkinter import messagebox, ttk
import requests
from datetime import datetime
class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Forecast App")
        self.root.geometry("800x400")
        self.root.resizable(False, False)
        self.root.configure(bg="#F994DC")  # Light pink background
        
        # Add this line to ensure child widgets don't override the background
        ttk.Frame(self.root, style='TFrame').pack(fill='both', expand=True)
        
        # Configure style to use the same background
        self.style = ttk.Style()
        self.style.configure('TFrame', background="#F994DC")
        self.style.configure('TLabel', background="#F994DC")
        self.style.configure('TButton', background="#FF69B4", foreground="black")
        
        # API key - replace with your own from OpenWeatherMap
        self.api_key = "79a6d79722323f1c1988fde75011c51b"
        self.base_url = "http://api.openweathermap.org/data/2.5/weather?"
        
        # Create GUI elements
        self.create_widgets()
    
    def create_widgets(self):
        # Styling
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        
        # Frame for input
        input_frame = ttk.Frame(self.root, padding="10")
        input_frame.pack(fill=tk.X)
        
        # City entry
        ttk.Label(input_frame, text="City:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.city_entry = ttk.Entry(input_frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)
        self.city_entry.focus()
        
        # Country code (optional)
        ttk.Label(input_frame, text="Country Code (optional):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.country_entry = ttk.Entry(input_frame, width=10)
        self.country_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Unit selection
        ttk.Label(input_frame, text="Units:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.unit_var = tk.StringVar(value="metric")
        ttk.Radiobutton(input_frame, text="Celsius", variable=self.unit_var, value="metric").grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Radiobutton(input_frame, text="Fahrenheit", variable=self.unit_var, value="imperial").grid(row=2, column=1, padx=5, pady=5, sticky=tk.E)
        
        # Search button
        search_button = ttk.Button(input_frame, text="Get Weather", command=self.get_weather)
        search_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Frame for results
        self.result_frame = ttk.Frame(self.root, padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True)
        
        # Weather info labels (will be populated when data is received)
        self.city_label = ttk.Label(self.result_frame, font=('Arial', 14, 'bold'))
        self.city_label.pack(pady=(0, 10))
        
        self.temp_label = ttk.Label(self.result_frame, font=('Arial', 24))
        self.temp_label.pack()
        
        self.weather_label = ttk.Label(self.result_frame, font=('Arial', 12))
        self.weather_label.pack()
        
        self.details_label = ttk.Label(self.result_frame, font=('Arial', 10))
        self.details_label.pack(pady=(20, 0))
        
        self.time_label = ttk.Label(self.result_frame, font=('Arial', 8))
        self.time_label.pack(side=tk.BOTTOM, pady=10)
    
    def get_weather(self):
        city = self.city_entry.get().strip()
        country = self.country_entry.get().strip()
        units = self.unit_var.get()
        
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        # Build query URL
        query = f"{self.base_url}q={city}"
        if country:
            query += f",{country}"
        query += f"&appid={self.api_key}&units={units}"
        
        try:
            response = requests.get(query)
            data = response.json()
            
            if data["cod"] != 200:
                messagebox.showerror("Error", data["message"])
                return
            
            # Update UI with weather data
            self.display_weather(data, units)
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", "Unable to connect to weather service")
        except Exception as e:
            messagebox.showerror("Error", "An error occurred while processing weather data")
    
    def display_weather(self, data, units):
        # Extract relevant data
        city = data["name"]
        country = data["sys"]["country"]
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        weather_desc = data["weather"][0]["description"].title()
        icon_code = data["weather"][0]["icon"]
        
        # Set unit symbols
        temp_unit = "°C" if units == "metric" else "°F"
        speed_unit = "m/s" if units == "metric" else "mph"
        
        # Update labels
        self.city_label.config(text=f"{city}, {country}")
        self.temp_label.config(text=f"{temp:.1f}{temp_unit}")
        self.weather_label.config(text=weather_desc)
        
        details_text = (f"Feels like: {feels_like:.1f}{temp_unit}\n"
                       f"Humidity: {humidity}%\n"
                       f"Wind: {wind_speed} {speed_unit}")
        self.details_label.config(text=details_text)
        
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=f"Last updated: {current_time}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

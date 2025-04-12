from flask import Flask, request, jsonify
import requests
import os
import json
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def get_weather():
    # Get latitude and longitude from request parameters
    latitude = request.args.get('latitude')
    longitude = request.args.get('longitude')
    
    # Validate input parameters
    if not latitude or not longitude:
        return jsonify({"error": "Latitude and longitude parameters are required"}), 400
    
    try:
        # Call the Open-Meteo API
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "apparent_temperature", 
                       "precipitation", "wind_speed_10m", "wind_direction_10m", 
                       "cloud_cover", "weather_code"],
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", 
                      "sunrise", "sunset", "precipitation_probability_max", 
                      "wind_speed_10m_max", "weather_code"],
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        
        weather_data = weather_response.json()
        
        # Get location name using reverse geocoding if possible
        try:
            geo_url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
            geo_response = requests.get(geo_url, headers={"User-Agent": "WeatherAPI/1.0"})
            location_data = geo_response.json()
            location_name = location_data.get('address', {}).get('city') or location_data.get('address', {}).get('town') or f"coordinates {latitude}, {longitude}"
        except:
            location_name = f"coordinates {latitude}, {longitude}"
        
        # Generate weather report using OpenAI with enhanced prompting
        system_message = """
You are providing friendly, conversational weather information in a natural, casual tone. Create a weather description that:

1. Sounds like how a friend would describe the weather to another friend
2. Uses everyday language rather than formal meteorological terminology
3. Focuses on practical implications of the weather (how it will feel, what to wear, activities impacted)
4. Avoids TV presenter phrases or formal structures
5. Includes relatable context (like "perfect sweater weather" or "you might want to reschedule that picnic")

Your description should feel like a text message or casual conversation about the weather, not a formal report.
"""
        user_prompt = f"""
        Create a weather report for {location_name} based on this meteorological data:
        
        CURRENT CONDITIONS:
        - Temperature: {weather_data.get("current", {}).get("temperature_2m")}°C
        - Feels like: {weather_data.get("current", {}).get("apparent_temperature")}°C
        - Humidity: {weather_data.get("current", {}).get("relative_humidity_2m")}%
        - Wind: {weather_data.get("current", {}).get("wind_speed_10m")} km/h, direction {weather_data.get("current", {}).get("wind_direction_10m")}°
        - Cloud cover: {weather_data.get("current", {}).get("cloud_cover")}%
        - Precipitation: {weather_data.get("current", {}).get("precipitation")} mm
        - Weather code: {weather_data.get("current", {}).get("weather_code")}
        
        DAILY FORECAST:
        - Today's high: {weather_data.get("daily", {}).get("temperature_2m_max", [])[0] if weather_data.get("daily", {}).get("temperature_2m_max") else 'N/A'}°C
        - Today's low: {weather_data.get("daily", {}).get("temperature_2m_min", [])[0] if weather_data.get("daily", {}).get("temperature_2m_min") else 'N/A'}°C
        - Precipitation: {weather_data.get("daily", {}).get("precipitation_sum", [])[0] if weather_data.get("daily", {}).get("precipitation_sum") else 'N/A'} mm
        - Precipitation probability: {weather_data.get("daily", {}).get("precipitation_probability_max", [])[0] if weather_data.get("daily", {}).get("precipitation_probability_max") else 'N/A'}%
        - Sunrise: {weather_data.get("daily", {}).get("sunrise", [])[0] if weather_data.get("daily", {}).get("sunrise") else 'N/A'}
        - Sunset: {weather_data.get("daily", {}).get("sunset", [])[0] if weather_data.get("daily", {}).get("sunset") else 'N/A'}
        
       Describe these weather conditions in a casual, friendly way as if you're texting a friend about the weather. 
Include practical advice about clothing or activities, but keep everything conversational and natural.
"""
        
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        weather_report = response.choices[0].message.content
        
        # Return the data and report
        return jsonify({
            "location": location_name,
            "temperature": weather_data.get("current", {}).get("temperature_2m"),
            "report": weather_report
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
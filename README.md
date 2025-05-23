This repository contains a Flask-based API that provides weather information in hman understandable natural language generated by OpenAI's GPT-4o model.

## Prerequisites

- Docker installed on your system
- OpenAI API key

## Setup and Installation

### 1. Clone the repository (or extract the ZIP file)

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Add your OpenAI API key

Edit the `.env` file and add your OpenAI API key:

```
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Build the Docker image

```bash
docker build -t weather-api .
```

### 4. Run the Docker container

```bash
docker run -p 5000:5000 --env-file .env weather-api
```

This will start the application and make it available at http://localhost:5000

## Testing the API

You can test the API using curl or a web browser. Here's a sample curl command:

```bash
curl "http://localhost:5000/weather?latitude=40.7128&longitude=-74.0060"
```

This will return a JSON response with the weather information for New York City:

```json
{
  "location": "New York",
  "temperature": 23.5,
  "report": "Hey! Just checked the weather in New York and it's a pretty nice 23.5°C right now, though it actually feels like 25°C with the humidity. There's about 40% cloud cover and barely any chance of rain today (only 10% probability). It's a tiny bit breezy with winds at 12 km/h. The sun's already up and won't set until around 8 PM, so you've got plenty of daylight left! Perfect weather for that walk you were talking about, but maybe bring a light jacket for later when it drops to about 18°C tonight. Enjoy your day!"
}
```

## API Endpoint

### GET /weather

Returns weather information and a natural language description for a specified location.

**Query Parameters:**
- `latitude` (required): Latitude of the location
- `longitude` (required): Longitude of the location

**Example Response:**
```json
{
  "location": "Paris",
  "temperature": 18.2,
  "report": "Hey! It's a comfortable 18.2°C in Paris right now, though it actually feels like 17°C. The sky is partly cloudy with about 40% cloud cover. There's a light breeze coming from the southwest at 15 km/h. No need for an umbrella today - precipitation chances are really low. It'll cool down to about 14°C tonight, so maybe grab a light jacket if you're out late. Perfect weather for strolling along the Seine or sitting at a café terrace! Enjoy your day in the City of Light!"
}
```

## Notes

- The API uses the Open-Meteo API for weather data and OpenStreetMap for reverse geocoding
- Weather descriptions are generated using OpenAI's GPT-4o model in a conversational style
- The Docker container exposes port 5000

If you encounter any issues or have questions, please contact khule.tanmay.dev@gmail.com.

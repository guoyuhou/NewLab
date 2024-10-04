# modules/external_services.py

import requests

def get_weather(city):
    api_key = "YOUR_API_KEY"  # 替换为您的OpenWeatherMap API密钥
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    
    response = requests.get(base_url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"]
        }
    else:
        return None

def get_weather_recommendation(weather_data):
    if weather_data["temperature"] > 30:
        return "注意：当前温度较高，请确保实验室空调正常工作，以维持理想的实验环境。"
    elif weather_data["temperature"] < 10:
        return "注意：当前温度较低，请注意保持实验室温度，某些实验可能需要额外的保温措施。"
    elif weather_data["humidity"] > 70:
        return "注意：当前湿度较高，某些湿度敏感的实验可能需要额外的除湿措施。"
    elif weather_data["humidity"] < 30:
        return "注意：当前湿度较低，某些实验可能需要使用加湿器来维持适当的湿度。"
    else:
        return "当前天气条件适合大多数实验，请继续保持良好的实验环境。"
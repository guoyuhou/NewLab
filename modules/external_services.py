# modules/external_services.py
"""
此模块提供了与外部服务交互的功能，主要用于获取天气信息和生成相应的实验室建议。

主要功能:
1. 从OpenWeatherMap API获取天气数据
2. 根据天气数据生成实验室环境建议
"""

import requests

def get_weather(city):
    """
    获取指定城市的天气信息。

    参数:
    city (str): 要查询天气的城市名称

    返回:
    dict: 包含温度、湿度和天气描述的字典，如果请求失败则返回None
    """
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
    """
    根据天气数据生成实验室环境建议。

    参数:
    weather_data (dict): 包含温度和湿度信息的字典

    返回:
    str: 根据天气条件给出的实验室环境建议
    """
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
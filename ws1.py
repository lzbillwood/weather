import streamlit as st
import requests
import pandas as pd

# 和风天气 API 密钥
API_KEY = '87f7f6f141654973bdb1b962f8862930'

# 默认显示的城市列表
DEFAULT_CITIES = ['兰州', '北京', '重庆', '乌鲁木齐', '南京', '台北']

def get_city_id(city_name):
    # 构建 API 请求 URL 获取城市 ID
    url = f'https://geoapi.qweather.com/v2/city/lookup?location={city_name}&key={API_KEY}'
    
    try:
        # 发送 HTTP 请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        
        # 检查返回数据是否有效
        if data['code'] == '200' and data['location']:
            return data['location'][0]['id']
        else:
            st.error(f"Error: {data['code']} - {data['refer']['sources'][0]}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def get_weather(city_id):
    # 构建 API 请求 URL 获取天气数据
    url = f'https://devapi.qweather.com/v7/weather/now?location={city_id}&key={API_KEY}'
    
    try:
        # 发送 HTTP 请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()
        
        # 检查返回数据是否有效
        if data['code'] == '200':
            return data['now']
        else:
            st.error(f"Error: {data['code']} - {data['refer']['sources'][0]}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Error: {e}")
        return None

def main():
    st.title("多城市天气查询 Web 应用")
    
    # 获取用户输入的城市名称
    city_names = st.multiselect("请选择城市名称:", DEFAULT_CITIES, default=DEFAULT_CITIES)
    
    if st.button("查询"):
        if city_names:
            weather_data_list = []
            
            for city_name in city_names:
                # 获取城市 ID
                city_id = get_city_id(city_name)
                
                if city_id:
                    # 获取天气数据
                    weather_data = get_weather(city_id)
                    
                    if weather_data:
                        # 提取天气信息
                        temperature = weather_data['temp']
                        feels_like = weather_data['feelsLike']
                        humidity = weather_data['humidity']
                        description = weather_data['text']
                        wind_speed = weather_data['windSpeed']
                        
                        # 将天气数据添加到列表中
                        weather_data_list.append({
                            '城市': city_name,
                            '温度 (°C)': temperature,
                            '体感温度 (°C)': feels_like,
                            '湿度 (%)': humidity,
                            '天气描述': description,
                            '风速 (m/s)': wind_speed
                        })
                    else:
                        st.error(f"无法获取 {city_name} 的天气信息。")
                else:
                    st.error(f"无法获取 {city_name} 的城市信息。")
            
            # 将天气数据转换为 DataFrame
            df = pd.DataFrame(weather_data_list)
            
            # 显示表格
            st.write(df)
        else:
            st.warning("请选择城市名称。")

if __name__ == "__main__":
    main()
import requests
from dataclasses import dataclass
import datetime

api_key = 'd88132699d8735f587671aea92d282a7'

@dataclass
class WeatherData:
    main: str
    description: str
    icon: str
    temperature: float
    temperature_night: float
    dow: str
def get_lan_lon(city_name):
    url_geocode = f'https://geocode.maps.co/search?q={city_name}'
    response_geocode = requests.get(url_geocode).json()
    lat = response_geocode[0]['lat']
    lon = response_geocode[0]['lon']
    return lat,lon

def get_weather(lat,lon):
    url_weather = f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&cnt={72//3}&units=metric&appid={api_key}'
    response_weather = requests.get(url_weather).json()


    temp_1 = response_weather.get('list')[0]['dt_txt'].split(' ')[0].split('-')
    temp_2 = response_weather.get('list')[10]['dt_txt'].split(' ')[0].split('-')
    temp_3 = response_weather.get('list')[18]['dt_txt'].split(' ')[0].split('-')

    def get_dow(number):
        dict = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
        return dict.get(number)
    data_1 = WeatherData(main = response_weather.get('list')[0].get('weather')[0].get('main'),
                       description = response_weather.get('list')[0].get('weather')[0].get('description'),
                       icon = response_weather.get('list')[0].get('weather')[0].get('icon'),
                       temperature = (float) ((response_weather.get('list')[0].get('main').get('temp')*10.0)/10),
                       temperature_night = (float) ((response_weather.get('list')[2].get('main').get('temp')*10.0)/10),
                       dow =  get_dow(datetime.datetime(int(temp_1[0]), int(temp_1[1]), int(temp_1[2])).weekday())
                       )

    data_2 = WeatherData(main=response_weather.get('list')[8].get('weather')[0].get('main'),
                       description=response_weather.get('list')[8].get('weather')[0].get('description'),
                       icon=response_weather.get('list')[8].get('weather')[0].get('icon'),
                       temperature=(float)((response_weather.get('list')[0].get('main').get('temp') * 10.0) / 10),
                       temperature_night = (float)((response_weather.get('list')[2].get('main').get('temp') * 10.0) / 10),
                         dow = get_dow(datetime.datetime(int(temp_2[0]), int(temp_2[1]), int(temp_2[2])).weekday())
                       )
    data_3 = WeatherData(main=response_weather.get('list')[16].get('weather')[0].get('main'),
                       description=response_weather.get('list')[16].get('weather')[0].get('description'),
                       icon=response_weather.get('list')[16].get('weather')[0].get('icon'),
                       temperature=(float)((response_weather.get('list')[0].get('main').get('temp') * 10.0) / 10),
                       temperature_night=(float)((response_weather.get('list')[2].get('main').get('temp') * 10.0) / 10),
                         dow=get_dow(datetime.datetime(int(temp_3[0]), int(temp_3[1]), int(temp_3[2])).weekday())
                       )
    return data_1,data_2,data_3

def main(city_name):
    lat, lon = get_lan_lon(city_name)
    weather_data = (get_weather(lat, lon))
    return weather_data




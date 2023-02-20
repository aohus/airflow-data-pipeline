import requests
import json
from datetime import datetime

lat=37.5642135
lon=127.0016985
part='hourly,minutely'
weather_api_url=f'https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude={part}&appid={API_key}&units=metric'

f = requests.get(weather_api_url).json()
l=[]
for day in f['daily']:
	l.append(tuple([datetime.fromtimestamp(day['dt']).strftime('%Y-%m-%d'), day['temp']['day'], day['temp']['min'], day['temp']['max']]))
print(l)
#query='''INSERT INTO dbtnghk528.weather_forcast VALUES ('Andrew', 'Male');'''

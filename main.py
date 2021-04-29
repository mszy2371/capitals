import json
import requests

from flask import Flask, render_template
import wikipedia


app = Flask(__name__)
app.static_folder = 'static'

wikipedia.set_lang('pl')

places = ['europa', 'berlin', 'bruksela', 'budapeszt', 'londyn', 'moskwa', 'paryż', 'rzym', 'sztokholm', 'warszawa', 'wiedeń']
translation = {'europa': 'europe', 'berlin': 'berlin', 'bruksela': 'brussels', 'budapeszt': 'budapest', 'londyn': 'london', 'moskwa': 'moscov',
               'paryż': 'paris', 'rzym': 'roma', 'sztokholm': 'stockholm', 'warszawa': 'warsaw', 'wiedeń': 'vienna'}
polish_pron = {'europa':'europie', 'berlin': 'berlinie', 'bruksela': 'brukseli', 'budapeszt': 'budapeszcie', 'londyn': 'londynie', 'moskwa': 'moskwie',
               'paryż': 'paryżu', 'rzym': 'rzymie', 'sztokholm': 'sztokholmie', 'warszawa': 'warszawie', 'wiedeń': 'wiedniu'}

with open('places.json', 'r', encoding='utf-8') as file:
    details = json.load(file)

@app.route('/')
@app.route('/<string:city>')
def index(city='europa'):
    api_key = '49be9a12dedd4d8d91e184129212804'
    url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={translation.get(city, {})}&aqi=no&lang=pl'
    response = requests.request('GET', url)
    resp = response.json()
    weather = (' (czas lokalny): ', resp.get('location', {}).get('localtime', {}), 'temp: ' ,
               resp.get('current', {}).get('temp_c', {}),'odczuwalna: ',  resp.get('current', {}).get('feelslike_c', {}), resp.get('current', {}).get('condition', {}).get('text', {}))
    icon = resp.get('current', {}).get('condition', {}).get('icon', {})
    picture = f'static/{city}.jpg'
    if city in places:
        return render_template('city.html', city=city, places=places, translation=translation, details=details,
                           picture=picture, weather=weather, icon=icon, polish_pron=polish_pron)
    else:
        return "<h1>Tego miejsca nie ma na naszej liście. Wybierz inne miasto.<h1>"


if __name__ == "__main__":
    app.run(debug=True)

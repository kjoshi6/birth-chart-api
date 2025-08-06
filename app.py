from flask import Flask, request, jsonify
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos

app = Flask(__name__)

@app.route('/calculate_chart', methods=['POST'])
def calculate_chart():
    data = request.get_json()
    date = data.get('birth_date')        # Format: YYYY-MM-DD
    time = data.get('birth_time')        # Format: HH:MM
    lat = data.get('latitude')           # Decimal degrees
    lon = data.get('longitude')          # Decimal degrees
    
    if not all([date, time, lat, lon]):
        return jsonify({'error': 'Missing required parameters'}), 400

    dt = Datetime(f'{date} {time}', 'UTC')
    pos = GeoPos(lat, lon)
    
    chart = Chart(dt, pos)

    planets = ['SUN', 'MOON', 'MERCURY', 'VENUS', 'MARS', 'JUPITER', 'SATURN', 'URANUS', 'NEPTUNE', 'PLUTO']
    result = {planet.lower(): chart.get(planet).sign for planet in planets}
    result['ascendant'] = chart.get('ASC').sign

    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

from flask import Flask, jsonify, send_from_directory, request
from pathlib import Path
from dotenv import load_dotenv
import os, json, threading, webbrowser, socket, time

from services.weather import get_current_weather, get_weather_forecast
from services.lst import load_neighborhoods_with_stats, ensure_data_ready

load_dotenv()
APP_ROOT = Path(__file__).parent.resolve()
DATA_DIR = APP_ROOT / "data"
STATIC_DIR = APP_ROOT / "static"

app = Flask(__name__, static_folder=str(STATIC_DIR))

ensure_data_ready(DATA_DIR)

@app.route('/')
def index():
    return send_from_directory(str(STATIC_DIR), 'index.html')

@app.route('/api/neighborhoods')
def neighborhoods():
    gdf = load_neighborhoods_with_stats(DATA_DIR / 'neighborhoods.geojson')
    return jsonify(json.loads(gdf.to_json()))

@app.route('/api/weather')
def weather():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    if lat is None or lon is None:
        return jsonify({'error': 'lat and lon are required'}), 400
    return jsonify(get_current_weather(lat, lon))

@app.route('/api/forecast')
def forecast():
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    days = request.args.get('days', default=5, type=int)
    if lat is None or lon is None:
        return jsonify({'error': 'lat and lon are required'}), 400
    try:
        data = get_weather_forecast(lat, lon, days)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'forecast_failed', 'detail': str(e)}), 502

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory(str(STATIC_DIR), path)

def find_free_port(preferred=5000):
    for p in (preferred, 5050, 8080):
        try:
            s = socket.socket(); s.bind(('127.0.0.1', p)); s.close(); return p
        except OSError:
            continue
    return preferred

def open_browser_when_ready(url):
    time.sleep(1.2)
    try: webbrowser.open(url)
    except Exception: pass

if __name__ == '__main__':
    host = os.getenv('HOST', '127.0.0.1')
    port = int(os.getenv('PORT', find_free_port()))
    url = f'http://{host}:{port}'
    threading.Thread(target=open_browser_when_ready, args=(url,), daemon=True).start()
    print(f'Opening {url} …')
    app.run(host=host, port=port, debug=False)

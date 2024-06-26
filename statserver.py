# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:59:16 2024

@author: alankar
"""

import requests
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from functools import wraps
import pickle
import shutil
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# List of allowed IPs
localhost = '127.0.0.1' 
iisc_ip = '10.0.0.20'
ALLOWED_IPS = [localhost, iisc_ip ] #'192.168.1.1'  # Example IP addresses
block_unknown_client = False

database_loc  = '.' # '/home/alankardutta/mysite'
database_name = 'database-coords.pickle'
database_ips = 'database-ips.pickle'

def check_ip(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.remote_addr
        if client_ip not in ALLOWED_IPS and block_unknown_client:
            print(f'{client_ip} not allowed to communicate!')
            abort(403, {'message': f'IP {client_ip} not allowed to communicate!'})  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/coordinates', methods=['GET'])
@check_ip
def get_coordinates():
    try:
       with open(f'{database_loc}/{database_name}', 'rb') as handle:
           visitorCoordinates = pickle.load(handle)
    except:
        visitorCoordinates = []
    # Return the coordinates as a JSON response
    return jsonify(visitorCoordinates)

@app.route('/api/coordinates', methods=['POST'])
@check_ip
def receive_coordinates():
    data = request.get_json()  # Parse the JSON from the request body
    coordinates = data.get('coordinates')
    ip_addr = data.get('ip')
    org = data.get('org')
    city = data.get('city')
    if coordinates is None:
        return jsonify({'status': 'error', 'message': 'No coordinates provided'}), 400
    if ip_addr is None:
        return jsonify({'status': 'error', 'message': 'No IP provided'}), 400

    print("Received coordinates:", coordinates)
    print("Received ip:", ip_addr)
    try:
       with open(f'{database_loc}/{database_name}', 'rb') as handle:
           visitorCoordinates = pickle.load(handle)
    except:
        visitorCoordinates = []
    try:
       with open(f'{database_loc}/{database_ips}', 'rb') as handle:
           ip_info = pickle.load(handle)
    except:
        ip_info = []
    print("Starting with:", ip_info)
    all_ips = [ip[0] for ip in ip_info]
    if ip_addr not in all_ips:
        visitorCoordinates.append(coordinates)
        ip_info.append([ip_addr, org, city])
        if os.path.exists(f'{database_loc}/backup_{database_name}'):
            os.remove(f'{database_loc}/backup_{database_name}')
        if os.path.exists(f'{database_loc}/{database_name}'):
            shutil.copyfile(f'{database_loc}/{database_name}', f'{database_loc}/backup_{database_name}')
        with open(f'{database_loc}/{database_name}', 'wb') as handle:
            pickle.dump(visitorCoordinates, handle, protocol=pickle.HIGHEST_PROTOCOL)
        if os.path.exists(f'{database_loc}/backup_{database_ips}'):
            os.remove(f'{database_loc}/backup_{database_ips}')
        if os.path.exists(f'{database_loc}/{database_ips}'):
            shutil.copyfile(f'{database_loc}/{database_ips}', f'{database_loc}/backup_{database_ips}')
        with open(f'{database_loc}/{database_ips}', 'wb') as handle:
            pickle.dump(ip_info, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return jsonify({'status': 'success', 'message': f'Coordinates {coordinates} with IP {ip_addr} received by server successfully'}), 200

@app.route('/api/geo-location', methods=['POST'])
@check_ip
def receive_geo_info():
    data = request.get_json()  # Parse the JSON from the request body
    ip_addr = data.get('ip')
    if ip_addr == '' or ip_addr is None:
        return jsonify({'status': 'error', 'message': 'No ip sent to query geo-location'}), 400
    reply = requests.get(f'http://ip-api.com/json/{ip_addr}').json()
    if reply is None:
        return jsonify({'status': 'error', 'message': 'No coordinates provided'}), 400
    print("Received coordinates:", reply)

    return jsonify({'status': reply['status'], 
                    'lat': reply['lat'],
                    'lon': reply['lon'],
                    'ip':  reply['query'],
                    'org': reply['org'],
                    'city': reply['city']}), 200

@app.route('/api/get-stats', methods=['GET'])
@check_ip
def send_visitor_info():
    try:
       with open(f'{database_loc}/{database_name}', 'rb') as handle:
           visitorCoordinates = pickle.load(handle)
    except:
        visitorCoordinates = []
    try:
       with open(f'{database_loc}/{database_ips}', 'rb') as handle:
           ip_info = pickle.load(handle)
    except:
        ip_info = []

    return jsonify({'ips': ip_info,
                    'visitor coordinates': visitorCoordinates,}), 200

@app.route('/')
def info():
    return 'Website visitor stat server!'

production = False
port = 5000
if __name__ == "__main__":
    if production:
        from waitress import serve
        serve(app, host=localhost, port=port)
    else:
        app.run(debug=False, port=port)

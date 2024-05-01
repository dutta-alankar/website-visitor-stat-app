# -*- coding: utf-8 -*-
"""
Created on Wed May  1 11:59:16 2024

@author: alankar
"""

from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from functools import wraps
import pickle

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes

# List of allowed IPs
localhost = '127.0.0.1' 
iisc_ip = '10.0.0.20'
ALLOWED_IPS = [localhost, iisc_ip ] #'192.168.1.1'  # Example IP addresses
block_unknown_client = True

database_loc  = '/home/alankardutta/mysite'
database_name = 'database-coords.pickle'

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
    if coordinates is None:
        return jsonify({'status': 'error', 'message': 'No coordinates provided'}), 400

    print("Received coordinates:", coordinates)
    try:
       with open(f'{database_loc}/{database_name}', 'rb') as handle:
           visitorCoordinates = pickle.load(handle)
    except:
        visitorCoordinates = []
    if coordinates not in visitorCoordinates:
        visitorCoordinates.append(coordinates)
        with open(f'{database_loc}/{database_name}', 'wb') as handle:
            pickle.dump(visitorCoordinates, handle, protocol=pickle.HIGHEST_PROTOCOL)

    return jsonify({'status': 'success', 'message': f'Coordinates {coordinates} received by server successfully'}), 200

@app.route('/')
def info():
    return 'Website visitor stat server!'

if __name__ == '__main__':
    app.run(debug=False) #, port=5000)

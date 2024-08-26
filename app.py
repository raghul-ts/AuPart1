from flask import Flask, request, jsonify, send_from_directory
import os
import random
from flask_cors import CORS

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes

# Serve the index.html file for the homepage
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Function to predict parameters based on casting temperature
def calculate_parameters(casting_temp):
    predicted_values = {
        'cooling_water_temp': calculate_cooling_water_temp(casting_temp),
        'casting_speed': calculate_casting_speed(casting_temp),
        'chemical_composition': calculate_chemical_composition(casting_temp),
        'ambient_humidity': calculate_ambient_humidity(casting_temp),
        'energy_consumption': calculate_energy_consumption(casting_temp),
        'grain_size': calculate_grain_size(casting_temp),
        'uts': calculate_uts(casting_temp),
        'elongation': calculate_elongation(casting_temp),
        'conductivity': calculate_conductivity(casting_temp),
    }
    return predicted_values

# Functions to calculate based on the given formulas
def calculate_cooling_water_temp(casting_temp):
    return 0.5 * casting_temp + 2

def calculate_casting_speed(casting_temp):
    return 0.8 * casting_temp + 1000

def calculate_chemical_composition(casting_temp):
    return 0.01 * casting_temp + 0.5

def calculate_ambient_humidity(casting_temp):
    return 0.2 * casting_temp + 60

def calculate_energy_consumption(casting_temp):
    return 0.3 * casting_temp + 50

def calculate_grain_size(casting_temp):
    return 0.005 * casting_temp + 0.1

def calculate_uts(casting_temp):
    return 0.7 * casting_temp + 200

def calculate_elongation(casting_temp):
    return 0.1 * casting_temp + 5

def calculate_conductivity(casting_temp):
    return 0.4 * casting_temp + 60

# Optimum ranges for each parameter
optimum_ranges = {
    'cooling_water_temp': (20, 35),
    'casting_speed': (6, 12),
    'chemical_composition': (0.99, 1.01),
    'ambient_humidity': (60, 70),
    'energy_consumption': (60, 80),
    'grain_size': (0.2, 0.8),
    'uts': (300, 500),
    'elongation': (7, 15),
    'conductivity': (85, 100),
}

# Generate a random value within the optimum range
def generate_random_optimum_value(param):
    min_val, max_val = optimum_ranges.get(param, (None, None))
    if min_val is not None and max_val is not None:
        return random.uniform(min_val, max_val)
    return None

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    casting_temp = data.get('casting_temp', 0)

    # Convert casting_temp to float
    try:
        casting_temp = float(casting_temp)
    except ValueError:
        return jsonify({'error': 'Invalid casting temperature value'}), 400

    # Predict parameter values based on casting temperature
    predicted_values = calculate_parameters(casting_temp)

    prediction_info = {}
    total_optimum_before = 0
    total_optimum_after = 0

    for param, predicted_value in predicted_values.items():
        # Check if the predicted value is within the optimum range
        min_val, max_val = optimum_ranges.get(param, (None, None))
        is_optimum = min_val <= predicted_value <= max_val if min_val is not None and max_val is not None else False
        
        # Generate a random adjusted value within the optimum range
        adjusted_value = generate_random_optimum_value(param)
        is_adjusted_optimum = min_val <= adjusted_value <= max_val if min_val is not None and max_val is not None else False

        # Count optimum values
        if is_optimum:
            total_optimum_before += 1
        if is_adjusted_optimum:
            total_optimum_after += 1

        # Store prediction info for this parameter
        prediction_info[param] = {
            'predicted_value': predicted_value,
            'status_predicted': 'Optimum' if is_optimum else 'Not Optimum',
            'adjusted_value': adjusted_value,
            'status_adjusted': 'Optimum' if is_adjusted_optimum else 'Not Optimum',
        }

    # Calculate the percentage of parameters within the optimum range
    percentage_optimum_predicted = (total_optimum_before / len(predicted_values)) * 100
    percentage_optimum_adjusted = (total_optimum_after / len(predicted_values)) * 100

    return jsonify({
        'prediction_info': prediction_info,
        'percentage_optimum_predicted': percentage_optimum_predicted,
        'percentage_optimum_adjusted': percentage_optimum_adjusted,
    })

if __name__ == '__main__':
    app.run(debug=True)

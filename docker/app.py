from flask import Flask, jsonify, request, json

import pandas as pd
import logging
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

app = Flask(__name__)


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/')
def home():
    return jsonify(message="ITBA, Implementación de Aplicaciones de Aprendizaje Automático en la Nube.")



@app.route('/min_stock', methods=['GET'])
def minStock():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)

    # Calculate the minimum stock based on 'desgaste(%)'
    min_stock = df['desgaste(%)'].min()

    # Log the minimum stock
    logging.info("Minimum stock based on desgaste(%%): %f", min_stock)

    # Return the response.
    return jsonify(message="Minimum stock based on desgaste(%%): %f" % min_stock)



@app.route('/maintenance_frequency', methods=['GET'])
def maintenanceFrequency():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)

    # Define a threshold for maintenance.
    threshold = 0.03

    # Calculate maintenance frequency.
    maintenance_count = df[df['desgaste(%)'] > threshold].shape[0]

    # Log the maintenance frequency.
    logging.info("Maintenance frequency (number of times desgaste(%%) > %f): %d", threshold, maintenance_count)

    return jsonify(message="Maintenance frequency (number of times desgaste(%%) > %f): %d" % (threshold, maintenance_count))



@app.route('/number_of_coaches', methods=['GET'])
def numberOfCoaches():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)

    # Define a threshold for carga[ton]
    threshold_carga = 100

    # Calculate the number of coaches that meet the condition
    coaches_in_use = df[df['carga[ton]'] > threshold_carga].shape[0]

    # Log the number of coaches in use
    logging.info("Number of coaches in use (carga[ton] > %d): %d", threshold_carga, coaches_in_use)

    return jsonify(message="Number of coaches in use (carga[ton] > %d): %d" % (threshold_carga, coaches_in_use))



@app.route('/wheel_wear', methods=['GET'])
def wheelWear():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)

    # Calculate wear per kilometer
    df['wear_per_km'] = df['desgaste(%)'] / df['distancia[km]']

    # Calculate wear per ton
    df['wear_per_ton'] = df['desgaste(%)'] / df['carga[ton]']

    # Convert results to string
    wear_per_km_str = df[['distancia[km]', 'wear_per_km']].to_string(index=False)
    wear_per_ton_str = df[['carga[ton]', 'wear_per_ton']].to_string(index=False)

    # Combine results into a single string
    result_str = f"Wear per kilometer:\n{wear_per_km_str}\n\nWear per ton:\n{wear_per_ton_str}"

    # Log the results
    logging.info(result_str)

    return jsonify(message=result_str)



@app.route('/average_wheel_life', methods=['GET'])
def averageWheelLife():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)

    # Calculate wear per kilometer
    df['wear_per_km'] = df['desgaste(%)'] / df['distancia[km]']

    # Filter by material 'ruedas'
    ruedas_df = df[df['MATERIAL'] == 'ruedas']

    # Calculate the average wear per kilometer
    average_wear_per_km = ruedas_df['wear_per_km'].mean()

    # Log the result
    logging.info("Average wear per kilometer for 'ruedas': %f", average_wear_per_km)

    # Return the result as a string
    result_str = f"Average wear per kilometer for 'ruedas': {average_wear_per_km}"

    return jsonify(message=result_str)



@app.route('/wheelsByKilometers', methods=['GET'])
def wheelsByKilometers():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)
    
    # Filter the dataset to include only rows where MATERIAL is 'ruedas'
    df_ruedas = df[df['MATERIAL'] == 'ruedas']

    # Prepare the data for machine learning
    X = df_ruedas[['desgaste(%)', 'carga[ton]']]
    y = df_ruedas['distancia[km]']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Function to predict the number of wheels needed for a given distance
    def predict_wheels_needed(N):
        # Predict the desgaste for the given distance
        desgaste_pred = model.predict([[0, 0]])[0] / N
        # Calculate the number of wheels needed
        avg_desgaste = df_ruedas['desgaste(%)'].mean()
        wheels_needed = desgaste_pred / avg_desgaste
        return wheels_needed

    # Example usage
    logging.info(request.args.get('km'))
    N = int(request.args.get('km'))   # Distance in kilometers
    wheels_needed = predict_wheels_needed(N)
    
    return jsonify(message=f"Number of wheels needed for {N} kilometers: {wheels_needed}")



@app.route('/wheelsByKilometersAndTons', methods=['GET'])
def wheelsByKilometersAndTons():
    
    # Loading the DS.
    logging.info("Loading Data Set...")
    df = pd.read_csv('data.csv')

    # Convert 'desgaste(%)' to numeric, replacing commas with dots
    df['desgaste(%)'] = df['desgaste(%)'].str.replace(',', '.').astype(float)
    
    # Filter the dataset to include only rows where MATERIAL is 'ruedas'
    df_ruedas = df[df['MATERIAL'] == 'ruedas']

    # Prepare the data for machine learning
    X = df_ruedas[['distancia[km]', 'carga[ton]']]
    y = df_ruedas['desgaste(%)']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train a Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Function to predict the number of wheels needed for a given distance and load
    def predict_wheels_needed(N, load):
        # Predict the desgaste for the given distance and load
        desgaste_pred = model.predict([[N, load]])[0]
        # Calculate the number of wheels needed
        avg_desgaste = df_ruedas['desgaste(%)'].mean()
        wheels_needed = desgaste_pred / avg_desgaste
        return wheels_needed

    # Get parameters from request
    N = float(request.args.get('km'))       # Distance in kilometers
    load = float(request.args.get('tons'))  # Load in tons

    # Predict the number of wheels needed
    wheels_needed = predict_wheels_needed(N, load)
    
    return jsonify(message=f"Number of wheels needed for {N} kilometers and {load} tons: {wheels_needed}")
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58080)
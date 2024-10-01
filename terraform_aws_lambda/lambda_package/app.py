from flask import Flask, jsonify, request, json

import pandas as pd
import logging

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



@app.route('/numberOfCoaches', methods=['GET'])
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



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=58080)
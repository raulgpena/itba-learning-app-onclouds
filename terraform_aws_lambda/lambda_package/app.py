from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify(message="ITBA, Implementación de Aplicaciones de Aprendizaje Automático en la Nube.")

if __name__ == "__main__":
    app.run(debug=True)
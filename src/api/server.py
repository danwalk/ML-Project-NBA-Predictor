"""

Crea una API flask con un solo endpoint que muestre por pantalla el json 'googleplaystore.json'
de la carpeta /data. En resumen, el endpoint tiene que leer el fichero 'googleplaystore.json' y retornarlo.

Además, este fichero contiene otra función que está fuera de la funcionalidad de la API flask

"""

import os, sys
import pandas as pd
from flask import Flask
import json

dir = os.path.dirname
sep = os.sep
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)

project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)

app = Flask(__name__)

""" 1: No es una función de flask"""
def mi_funcion():
    from utils.flask_functions import funcion_flask_1
    
    """
    TODO - Esta función ha de llamar a la función 'funcion_flask_1' que está en /utils/flask_functions.py y
    mostrar por pantalla lo que retorne esa función.
    """
    return funcion_flask_1()

@app.route("/") 
def home():
    mensaje = " <h1> DWALK_ML_PROJECT <h3>"
    return mensaje

@app.route('/home', methods=['GET'])
def googleplaystore():
    playstore_json = project_path + sep + 'data' + sep + 'googleplaystore.json'
    json_playstore_readed = pd.read_json(playstore_json)
    return json_playstore_readed.to_json()

def main():
    # Get the settings fullpath
    settings_file = project_path + sep + 'config' + sep + 'flask_settings.json'
    # Load json from file 
    with open(settings_file, "r") as json_file_readed:
        json_readed = json.load(json_file_readed)

    # Load variables from jsons
    SERVER_RUNNING = json_readed["server_running"]

    if SERVER_RUNNING:
        DEBUG = json_readed["debug"]
        HOST = json_readed["host"]
        PORT_NUM = json_readed["port"]
        app.run(debug=DEBUG, host=HOST, port=PORT_NUM)
    else:
        print("Server settings.json doesn't allow to start server. " + "Please, allow it to run it.")
        

if __name__ == "__main__":
    main()
import os, sys
import pandas as pd
from flask import Flask
import json
import argparse
from flask import Flask, request, Response, render_template


dir = os.path.dirname
SEP = os.sep
src = dir(dir(os.path.abspath(__file__)))
sys.path.append(src)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)


from src.utils.sql_tb import getfullnbatablefromsql
from src.utils.folders_tb import read_json_to_dict

parser = argparse.ArgumentParser()
parser.add_argument("-x", type=int, help="the password")
args = vars(parser.parse_args())

if args["x"] == "daniel":
    print("Wrong password")
else:
    app = Flask(__name__)

    @app.route("/")  # @ --> esto representa el decorador de la función
    def home():
        """ Default path """
        return app.send_static_file('greet.html')
        return "Great, this is working!"

    @app.route("/greet")
    def greet():
        username = request.args.get('name')
        return render_template('index.html', name=username)

    @app.route("/nbadata", methods=['GET'])
    def create_json():
        S = request.args['token_id']
        if S == "X9808164K":
            df = getfullnbatablefromsql()
            return Response(df.to_json(orient="records"))
        else:
            return "That token ID is not correct"

    def main():
        # Get the settings fullpath
        settings_file = project_path + SEP + "src" + SEP + "utils" + SEP + 'flask_settings.json'

        # Load json from file 
        with open(settings_file, "r") as json_file_readed:
            json_readed = json.load(json_file_readed)


        json_readed = read_json_to_dict(settings_file)
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
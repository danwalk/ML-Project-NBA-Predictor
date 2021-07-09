import streamlit as st
from PIL import Image
import os, sys
import pandas as pd
import json
from src.utils.dataframes import shortversionofresults
from src.utils.models import gamepredictor
#from utils.stream_config import draw_map
#from utils.dataframes import load_csv

# Haz que se pueda importar correctamente estas funciones que están en la carpeta utils/
dir = os.path.dirname
SEP = os.sep
src_path = dir(dir(os.path.abspath(__file__)))
sys.path.append(src_path)
project_path = dir(dir(dir(os.path.abspath(__file__))))
sys.path.append(project_path)


menu = st.sidebar.selectbox('Menu:',
            options=["Welcome", "Visualization", "Model Prediction", "Team Stats", "Game Predictor", "API"])

if menu == "Welcome":
    # Pon el título del proyecto que está en el archivo "config.json" en /config

    config_json_path = project_path + SEP + "src" + SEP + "utils" + SEP + 'config.json'

    with open(config_json_path, "r") as config_json_readed:
        json_config = json.load(config_json_readed)

    st.header(json_config['Title'])
    st.subheader(json_config['Description'])
    st.write("Win, Lose or Draw, this is entertainment, with numbers and statistics!")
    st.write("Project created by Daniel Jonathan Walker")
    st.write("https://github.com/danwalk/ML-Project-NBA-Predictor")
    st.write("https://www.linkedin.com/in/daniel-jonathan-walker-2a5a461b5")
    image1 = project_path + SEP + 'data' + SEP + 'img' + SEP + 'NBA logo.jpg'
    image = Image.open(image1)
    st.image (image, use_column_width=False)
    st.write("Bookies stats, results and original predictions collected from:")
    st.write("https://masseyratings.com/nba/games")
    image2 = project_path + SEP + 'data' + SEP + 'img' + SEP + 'Massey Rating logo.jpg'
    image2 = Image.open(image2)
    st.image (image2,use_column_width=False)
    st.write("https://www.oddsportal.com/")
    image3 = project_path + SEP + 'data' + SEP + 'img' + SEP + 'OddsPortal logo.jpg'
    image3 = Image.open(image3)
    st.image (image3,use_column_width=False)
    
if menu == "Visualization":
    teamlist = ["Select", "All Teams", "Atlanta Hawks", "Charlotte Hornets", "Denver Nuggets", "Golden State Warriors", "Indiana Pacers",
        "Los Angeles Lakers", "Miami Heat","Milwaukee Bucks", "Phoenix Suns", "Utah Jazz"]
    reglist = ["Select", "BayesianRidge", "DecisionTreeRegressor", "GaussianProcessRegressor", "GradientBoostingRegressor",
    "KNeighborsRegressor", "LinearRegression", "RadiusNeighborsRegressor", "RandomForestRegressor", "RidgeCV", "SVR"]
    team = st.selectbox('Select', teamlist)
    regressor = st.selectbox('Select', reglist)
    imagepath = project_path + SEP + 'resources' + SEP + team + "_" + regressor + ".jpg"
    image2path = project_path + SEP + 'resources' + SEP + team + "_betdonut_" + regressor + ".jpg"
    if team != "Select" and regressor != "Select":
        image = Image.open(imagepath)
        st.image (image,use_column_width=False)
        image2 = Image.open(image2path)
        st.image (image2,use_column_width=False)
        if team == "All Teams":
            teamcsv = project_path + SEP + 'data' + SEP + team + "_" + regressor + "_.csv"
            teamcsv1 = pd.read_csv(teamcsv)
            shortdf = shortversionofresults(teamcsv1)
            st.table(shortdf)


if menu == "Model Prediction":
    teamlist = ["Select", "Atlanta Hawks", "Charlotte Hornets", "Denver Nuggets", "Golden State Warriors", "Indiana Pacers",
        "Los Angeles Lakers", "Miami Heat","Milwaukee Bucks", "Phoenix Suns", "Utah Jazz"]
    reglist = ["Select", "BayesianRidge", "DecisionTreeRegressor", "GaussianProcessRegressor", "GradientBoostingRegressor",
        "KNeighborsRegressor", "LinearRegression", "RadiusNeighborsRegressor", "RandomForestRegressor", "RidgeCV", "SVR"]
    team = st.selectbox('Choose Team', teamlist)
    regressor = st.selectbox('Choose Regressor', reglist)
    if regressor == "DecisionTreeRegressor":
        eon = st.selectbox('Choose Team', ["mse", "mae", "poisson", "friedman_mse"])
    elif regressor == "RandomForestRegressor":
        eon = st.slider("Select Estimators", min_value=50, max_value=200)
    elif regressor == "SVR":
        eon = st.slider("Select epsilon", min_value=0.1, max_value=0.25)
    else:
        eon = 5
    Gamenumber = st.slider(f'Select {team} game to predict with regressor {regressor}', min_value=10, max_value=72)
    if team != "Select" and regressor != "Select" and Gamenumber != 9 :
        gamepredictor(team, Gamenumber, regressor, eon)

if menu == "Json API-Flask":
    # Accede al único endpoint de tu API flask y lo muestra por pantalla como tabla/dataframe
    st.title('Dataset')
    dataframe_nba = pd.read_json('http://localhost:6060/nbaclean')
    st.table(dataframe_nba)


if menu == "Australia Fire":
    """6"""
    st.title("Fire Table")
    

    # 1. Conecta a la BBDD
    # 2. Obtén, a partir de sentencias SQL (no pandas), la información de las tablas que empiezan por 'fire_archive*' (join)
    # 3. Entrena tres modelos de ML diferentes siendo el target la columna 'fire_type'. Utiliza un pipeline que preprocese los datos con PCA. Usa Gridsearch.  
    # 4. Añade una entrada en la tabla 'student_findings' por cada uno de los tres modelos. 'student_id' es EL-ID-DE-TU-GRUPO.
    # 5. Obtén la información de la tabla 'fire_nrt_M6_96619' y utiliza el mejor modelo para predecir la columna target de esos datos. 
    # 6. Usando SQL (no pandas) añade una columna nueva en la tabla 'fire_nrt_M6_96619' con el nombre 'fire_type_EL-ID-DE-TU-GRUPO'
    # 7. Muestra por pantalla en Streamlit la tabla completa (X e y)
    


